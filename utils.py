

import os
import re

import config

from zipfile import ZipFile

from datatable import f
from functools import reduce
from operator import and_, or_, xor, eq


def get_filenames_from_zip(
		path_zip = config.PATH_DB
	):

	return (
		ZipFile(path_zip)
		.namelist()
	)


def name_to_dict(
		file_name,
		pattern = config.FNAME_PAT,
		col_names = config.FNAME_COLS[:4],
	):

	name = (re
		.search(pattern, file_name)
		.group(1)
		.split('_')
	)

	return {
		col_names[0] : file_name,
		col_names[1] : name[0],
		col_names[2] : int(name[1]),
		col_names[3] : int(name[2]),
	}


def get_jay_dir(
		file_name,
		path_jay = config.PATH_JAY,
		col_names = config.FNAME_COLS[1:4],
	):

	d = name_to_dict(file_name)

	jay_dir = os.path.join(*[
		path_jay,
		d[col_names[0]],
		str(d[col_names[1]]),
		str(d[col_names[2]]).zfill(2),
	])
	if not os.path.exists(jay_dir):
		os.makedirs(jay_dir)

	return jay_dir


def get_jay_files(
		path_jay = config.PATH_JAY,
	):

	return [f
		for (_, _, filenames) in (
			os.walk(path_jay)
		) for f in (
			filenames
		)
	]


def get_jay_path(
		file_name,
		path_jay = config.PATH_JAY,
	):

	values = (
		file_name
		.split('_')
		[:3]
	)

	values[2] = values[2].zfill(2)
	path_dir = '/'.join(values)

	return f'{path_jay}/{path_dir}/{file_name}'


def get_columns(
		file_name = 'dict_SIH.csv',
		path_db = config.PATH_DB,
	):

	return (
		(
			ZipFile(path_db)
			.open(
				file_name,
			)
		)
		.readline()
		.decode('utf-8')
		.strip()
		.split(',')
	)

#############################################

def isin(
		column,
		sequence_of_labels,
	):

	func = lambda x: f[column] == x

	return reduce(or_, map(func, sequence_of_labels))

#############################################
# Main

def main():

	fs = get_filenames_from_zip()
	print(fs[:12*2])


__name__ == '__main__' and main()

