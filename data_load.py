

import os
import sys
import config
import sqlite3
import requests
import numpy as np
import pandas as pd

from zipfile import ZipFile
from datatable import dt, f
from tqdm import tqdm
from secret import API_KEY


def compose_request(
		query,
		token = API_KEY,
		fetch_size = 1000,
	):

	return {
		"token": {"token": token},
		"sql": {"sql": {
			"query": query,
			"fetch_size": fetch_size}}}


def sql_query(
		query,
		url = config.URL_API,
	):
	
	return requests.post(
		os.path.join(
			url,'sql_query'),
			json = compose_request(query))


def json_to_df(resp):
	resp = resp.json()
	try:
		columns = [col['name'] for col in resp['columns']]
		values = resp['rows']
		df = pd.DataFrame(values, columns=columns)
	except Exception as E:
		df = pd.DataFrame()
		print(E)
		print(resp)
	return df


def df_query(query):
	return json_to_df(sql_query(query))


def create_connection(
		db_file = None,
	):

	db_file = (db_file
		if db_file else config.PATH_DB)

	try: conn = sqlite3.connect(db_file)
	except sqlite3.Error as e: print(e)

	return conn


def sql_execute(
		con,
		sql
	):

	cur = con.cursor()
	cur.executescript(sql) # execute | executescript
	con.commit()
	cur.close()


def filter_dataset(
		dataset,
		cols,
		years,
		cod_partos = list(config.PARTO),
	):
	
	df = dataset[
		(
			(f['PROC_REA'] == cod_partos[0])
			|
			(f['PROC_REA'] == cod_partos[1])
		) & (
			f['res_RSAUDCOD'] != 0
		) & (
			f['res_SIGLA_UF'] != 'DF'
		) & (
			f['IDADE'] >= 10
		),
		list(cols)
	]
	years_col = df['ano_internacao'].to_list()[0]
	df = df[
		[y in years for y in years_col], :
	].to_pandas().rename(columns=cols)

	return df


def get_criticidade_col(
		df,
		levels = [[0, 3], [1, 2]],
		places = ['cod_municipio', 'regiao_saude'], # 'regiao', 'uf', 
	):
	
	d = dict()
	for place in places:
		resid = df[f'res_{place}']
		inter = df[f'int_{place}']
		d[place] = (resid != inter).astype(int)
	criticidade = [
		levels[i][j] for i, j in zip(
			d[places[0]], d[places[1]])]
	
	return criticidade


def adjust_dataset(
		dataset,
		cols,
		years=list(np.arange(*config.YEAR_RANGE)),
	):

	df = filter_dataset(dataset, cols, years)
	df['criticidade'] = get_criticidade_col(df)
	# df = df[df['criticidade'] != 3]
	df['parto'] = df['parto'].map(config.PARTO)
	df['momento'] = df['ano'].map(
		config.PERIODS).fillna(config.PERIODS['outros'])
	
	return df


def register_location(
		df,
		places,
		locations=set(),
	):
	
	for _, row in df.iterrows():
		for ref in ['res', 'int']:
			t = tuple(row[f'{ref}_{p}'] for p in places)
			locations.add(t)
	infos = [col for col in df.columns if(
		col[:3] != 'res' and col[:3] != 'int')]
	for ref in ['res', 'int']:
		infos.append(f'{ref}_cod_municipio')
	
	return df[infos], locations


def load_health_regions(
		csv_name = 'health_regions',
	):
	
	csv_path = f'{config.PATH_DATA}consult/{csv_name}.csv'
	
	return pd.read_csv(csv_path)


def get_col_names_of_places(
		cols
	):

	return [col[4:]
		for col in cols.values() if (
			col[:3] == 'res')]


def get_namelist_in_zip(
		path_zip,
		ignore_dict = True
	):
	
	namelist = list()
	files = ZipFile(path_zip).namelist()
	for fname in files:
		if ignore_dict and 'dict' in fname:
			continue
		namelist.append(fname)
	
	return namelist


def append_table_to_con(
		df,
		con,
		table = 'partos',
	):

	try:
		df.to_sql(
			name = table,
			con = con,
			if_exists = 'append', # append | replace
			index = False,
		)
	except Exception as excep:
		print(excep)
		print(df.columns)


def df_places_from_locations(
		places,
		locations
	):
	
	regions = load_health_regions()
	df = pd.DataFrame(
		locations, columns=places)
	df['grupo'] = df.merge(
		regions,
		how='left',
		left_on='cod_municipio',
		right_on='Cód IBGE',
	)['Grupo']
	
	return df.drop_duplicates()


def get_df_locations_from_fname(
		path_name,
		cols,
		places,
		locations=set(),
	):
	
	df = dt.fread(path_name)
	df = adjust_dataset(df, cols)
	df, locations = register_location(
		df, places, locations)
	
	return df, locations


def zip_to_sqlite(
		path_zip,
		conn,
		cols = config.COLUMNS,
	):
	
	dfs, locations = list(), set()
	places = get_col_names_of_places(cols)
	files = get_namelist_in_zip(path_zip)
	for fname in tqdm(files):
		df, locations = get_df_locations_from_fname(
			f'{path_zip}/{fname}', cols, places, locations)
		dfs.append(df)
		if len(dfs) > 100:
			append_table_to_con(pd.concat(dfs),conn)
			dfs = list()
	append_table_to_con(pd.concat(dfs),conn)
	df_places = df_places_from_locations(
		places, locations)
	append_table_to_con(df_places, conn, 'places')


def main(
		argv,
		arc
  ):

	path_zip = (
		config.PATH_DATABASE_ZIP
		if arc == 1 else argv[1])

	conn = create_connection()
	with conn:
		zip_to_sqlite(path_zip, conn)


if __name__ == '__main__':
	main(sys.argv, len(sys.argv))

