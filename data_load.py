

import pandas as pd
import config
import utils

from os.path import isfile, exists
from gdown import download
from datatable import dt, f
from tqdm.notebook import tqdm


def download_database(
		url = config.URL_DB,
		path_db = config.PATH_DB,
	):

	if not isfile(path_db):
		download(
			url,
			path_db,
			quiet = False,
		)
		print(''.join(
			'Downloaded at:',
			path_db,
		))
	
	return path_db


def get_datasets_info(
		path_db = download_database(),
		col_names = config.FNAME_COLS[1:4],
	):

	return (
		pd.DataFrame([
			utils.name_to_dict(fname)
				for fname in (
					utils.get_filenames_from_zip(path_db)
				) if (
					'dict' not in fname.lower()
				)
		])
		.sort_values(
			by = col_names,
			ignore_index = True,
		)
	)


def datasets_to_jay(
		datasets = get_datasets_info(),
		path_db = config.PATH_DB,
		path_jay = config.PATH_JAY,
	):

	if exists(path_jay):
		return path_jay

	for _, row in tqdm(
			datasets.iterrows(),
			total = datasets.shape[0],
		):

		dataset_path = f'{path_db}/{row["Arquivo"]}'
		df = dt.fread(dataset_path)
		jay_dir = utils.get_jay_dir(
			row["Arquivo"],
			path_jay
		)
		
		for cod, parto in (
				config.RENAME['PROC_REA'].items()
			):
			
			df_parto = df[
				f['PROC_REA'] == cod,
				df.names,
			]
			jay_name = '_'.join([
				str(row['UF']),
				str(row['Ano']),
				str(row['Mês']).zfill(2),
				str(parto),
				str(df_parto.nrows),
				str(df_parto.ncols),
			])
			df_parto.to_jay(
				f'{jay_dir}/{jay_name}.jay'
			)
	
	return path_jay


def get_jay_info(
		path_jay = datasets_to_jay(),
		col_names = config.FNAME_COLS[:7],
	):
	
	values = [
		([file] + (
			file
			.split('.')
			[0]
			.split('_')
		)) for file in (
			utils.get_jay_files(path_jay)
		)
	]

	datasets = (
		pd.DataFrame(
			values,
			columns = col_names,
		)
		.sort_values(
			col_names[0],
		)
	)

	for idx in [2, 3, 5, 6]:
		datasets[col_names[idx]] = (
			datasets
			[col_names[idx]]
			.astype(int)
		)
	
	return datasets


def open_jay_dataset(
		file_name,
		path_jay = config.PATH_JAY,
	):

	return dt.fread(
		utils.get_jay_path(
			file_name,
			path_jay,
		)
	)


def open_dict(
		file_name = 'dict_SIH.csv',
		path_db = config.PATH_DB,
	):

	return dt.fread(
		f'{path_db}/{file_name}',
		sep = ';',
	)


def load_sihsus():

	return open_dict(), get_jay_info()


#############################################
# Main

def main():
	
	load_sihsus()[1].to_csv(
		'data/info/tabelas.csv',
		index = False)


__name__ == '__main__' and main()

