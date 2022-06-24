
import os
import config

from functools import reduce
from datatable import f
from operator import and_, or_, xor, eq


def name_to_dict(
        file_name,
        col_names = config.FNAME_COLS,
    ):
    
    name = (file_name
        .split('.')[1]
        .split('_')
    )
    
    return {
        col_names[0] : file_name,
        col_names[1] : name[1],
        col_names[2] : int(name[2]),
        col_names[3] : int(name[3]),
    }


def get_path(
        file_name,
        path_db = config.PATH_DB,
        col_names = config.FNAME_COLS,
    ):

    d = name_to_dict(file_name)
    data_dir = path_db.split('/')[0]

    path_list = [
        data_dir,
        'sihsus', 
        f'{d[col_names[1]]}',
        f'{d[col_names[2]]}',
        f'{d[col_names[3]]:02d}',
    ]

    path_dir = '/'.join(path_list) + '/'
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    
    file_path = (
        path_dir + '_'.join(path_list[1:])
    )

    return file_path


def isin(column, sequence_of_labels):
    func = lambda x: f[column] == x
    return reduce(or_, map(func, sequence_of_labels))