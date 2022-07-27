

import sys
import config
import sqlite3

from zipfile import ZipFile
from datatable import dt, f
from tqdm import tqdm


def zip_csv_to_sqlite(
		path_zip = None,
		conn = None,
		partos = config.PARTO,
		escolaridade = config.ESCOLARIDADE,
		etnia = config.ETNIA,
		cols = config.COLUMNS,
	):

	path_zip = (
		config.PATH_SIHSUS_ZIP
		if len(sys.argv) == 1
		else path_zip
	)

	conn = (
		sqlite3.connect(config.PATH_DB)
		if conn is None
		else conn
	)

	files = ZipFile(path_zip).namelist()
	for fname in tqdm(files):
		if 'dict' in fname:
			continue
		cod_partos = list(partos)
		dataset_path = f'{path_zip}/{fname}'
		df = dt.fread(dataset_path)
		df = df[
			(
				(f['PROC_REA'] == cod_partos[0])
				|
				(f['PROC_REA'] == cod_partos[1])
			),
			list(cols)
		]
		df = df.to_pandas()
		df['PROC_REA'] = df['PROC_REA'].map(partos)
		df['INSTRU'] = df['INSTRU'].map(escolaridade)
		df['RACA_COR'] = df['RACA_COR'].map(etnia)
		df = df.rename(columns=cols)
		
		df.to_sql(
			name='partos',
			con=conn,
			if_exists='append', # append replace
			index=False,
		)


def main():
	zip_csv_to_sqlite()


__name__ == '__main__' and main()

