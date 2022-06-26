

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
		path_db = None,
		col_names = config.FNAME_COLS[1:4],
	):

	path_db = (
		download_database()
		if path_db is None
		else path_db
	)

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
		datasets = None,
		path_db = config.PATH_DB,
		path_jay = config.PATH_JAY,
	):

	datasets = (
		get_datasets_info()
		if datasets is None
		else datasets
	)

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
		path_jay = None,
		col_names = config.FNAME_COLS[:7],
	):
	
	path_jay = (
		datasets_to_jay()
		if path_jay is None
		else path_jay
	)

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

#############################################

def prefix_same_pair(
        arqv,
        pair = ['res', 'int'],
		col_names = config.FNAME_COLS[-2:],
    ):

    df = open_jay_dataset(arqv)

    pair_names = {n[len(p)+1:]
        for p in pair
            for n in df.names if (
                n[:len(p)] == p
            ) 
    }

    diffs = list()
    for col in pair_names:
        pair_a = f'{pair[0]}_{col}'
        pair_b = f'{pair[1]}_{col}'
        diff = df[
            f[pair_a] != f[pair_b],
            [pair_a, pair_b]
        ].shape[0]
        diffs.append({
            col_names[0] : col,
            col_names[1] : diff,
        })

    return pd.DataFrame(diffs)


def get_columns_info(
		datasets = None,
		col_names = config.FNAME_COLS,
	):
	
	datasets = (
		get_jay_info()
		if datasets is None
		else datasets
	)

	new_dts = list()
	for _, row in tqdm(
			datasets.iterrows(),
			total = datasets.shape[0],
		):
		df = prefix_same_pair(row[col_names[0]])
		for col in col_names[:-2]:
			df[col] = row[col]
		new_dts.append(df)
	df = pd.concat(new_dts)[col_names]

	return df.sort_values(
		by = [col_names[0], col_names[-1]],
		ascending = [True, False],
	)


def open_dict(
		file_name = 'dict_SIH.csv',
		path_db = config.PATH_DB,
	):

	return (
		dt.fread(
			f'{path_db}/{file_name}',
			sep = ';',
		)
		.to_pandas()
	)


def load_sihsus(
		sihsus_path = config.LOCAL_SIHSUS,
		dict_path = config.LOCAL_DICT,
	):

	if isfile(sihsus_path):
		sihsus = pd.read_pickle(sihsus_path)
	else:
		sihsus = get_columns_info()
		sihsus.to_pickle(sihsus_path)
	
	if isfile(dict_path):
		dicio = pd.read_pickle(dict_path)
	else:
		dicio = open_dict()
		dicio.to_pickle(dict_path)

	return sihsus, dicio


#############################################
# Main

def main():
	
	load_sihsus()[1].to_csv(
		'data/info/tabelas.csv',
		index = False
	)


__name__ == '__main__' and main()

