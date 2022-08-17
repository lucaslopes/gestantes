

import os
import re
import sys
import config
import sqlite3
import requests
import numpy as np
import pandas as pd
import elasticsearch

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
	if 'RequestError' in resp or 'columns' not in resp:
		df = pd.DataFrame()
		print(resp)
	else:
		columns = [col['name'] for col in resp['columns']]
		values = resp['rows']
		df = pd.DataFrame(values, columns=columns)
	return df


def df_query(query):
	return json_to_df(sql_query(query))


def create_connection(
		db_file=None,
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


def adjust_dataset(
		dataset,
		cols,
		years=np.arange(*config.YEAR_RANGE),
		places=['municipio', 'regiao_saude'], # 'regiao', 'uf', 
	):

	cod_partos = list(config.PARTO)
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
			f['IDADE'] > 10
		),
		list(cols)
	]
	years_col = df['ano_internacao'].to_list()[0]
	df = df[
		[y in years for y in years_col], :
	].to_pandas().rename(columns=cols)
	for place in places:
		resid = df[f'res_{place}']
		inter = df[f'int_{place}']
		df[f'mov_{place}'] = resid != inter
	df['parto'] = df['parto'].map(config.PARTO)
	df['period'] = df['ano'].map(
		config.PERIODS).fillna('other')
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


def zip_to_sqlite(
		path_zip,
		conn,
		cols = config.COLUMNS,
	):
	
	regions = pd.read_csv('data/consult/health_regions.csv')
	locations = set()
	places = [col[4:]
		for col in config.COLUMNS.values() if (
			col[:3] == 'res')]
	files = ZipFile(path_zip).namelist()
	for fname in tqdm(files):
		if 'dict' in fname: continue
		df = dt.fread(f'{path_zip}/{fname}')
		df = adjust_dataset(df, cols)
		df, locations = register_location(
			df, places, locations)
		df.to_sql(
			name='partos',
			con=conn,
			if_exists='append', # append | replace
			index=False)
	df_places = pd.DataFrame(
		locations, columns=places)
	df_places['grupo'] = df_places.merge(
		regions,
		left_on='cod_municipio',
		right_on='Cód IBGE'
	)['Grupo']
	print(df_places['grupo'].value_counts())
	df_places.to_sql(
			name='places',
			con=conn,
			if_exists='append', # append | replace
			index=False)


def main(
		argv,
		arc
  ):

	path_zip = (
		config.PATH_SIHSUS_ZIP
		if arc == 1 else argv[1])

	conn = create_connection()
	with conn:
		zip_to_sqlite(path_zip, conn)


if __name__ == '__main__':
	main(sys.argv, len(sys.argv))

