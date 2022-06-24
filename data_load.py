
import pandas as pd
import config
import utils

from os.path import isfile, exists
from gdown import download
from zipfile import ZipFile
from datatable import dt, f
from tqdm.notebook import tqdm


def download_database(
        url = config.URL_DB,
        path_db = config.PATH_DB,
    ):

    if not isfile(path_db):
        download(url, path_db, quiet=False)
    print(f'Downloaded at: {path_db}')


def get_datasets(
        path_db = config.PATH_DB,
    ):
    
    return (
        pd.DataFrame([
            utils.name_to_dict(fname)
                for fname in (
                    ZipFile(path_db)
                    .namelist()
                ) if fname[0] == 'E'
        ])
        .sort_values(
            by = config.FNAME_COLS[1:4],
            ignore_index = True,
        )
    )


def dump_data(
        tabelas = get_datasets(),
        path_db = config.PATH_DB,
        col_names = config.FNAME_COLS,
    ):

    new_tables = list()

    for _, row in tqdm(tabelas.iterrows(), total=tabelas.shape[0]):
        arquivo = row['Arquivo']
        current_path = f'{path_db}/{arquivo}'
        procs = config.RENAME['PROC_REA'].items()
        output = utils.get_path(arquivo, path_db)
        
        df = dt.fread(current_path)
        for cod, proc_name in procs:
            df_proc = df[
                f['PROC_REA'] == cod,
                df.names,
            ]
            sufix = f'{proc_name}_{df_proc.nrows}_{df_proc.ncols}'
            extention = f'{sufix}.jay'
            new_path =  f'{output}_{extention}'
            new_tables.append({
                col_names[0] : f'{output.split("/")[-1]}_{extention}',
                col_names[1] : row['UF'],
                col_names[2] : row['Ano'],
                col_names[3] : row['Mês'],
                col_names[4] : proc_name,
                col_names[5] : df_proc.nrows,
                col_names[6] : df_proc.ncols,
            })
            df_proc.to_jay(new_path)
    
    return pd.DataFrame(new_tables)


def load_sihsus(
        url = config.URL_DB,
        path_db = config.PATH_DB,
    ):

    download_database(url, path_db)

    data_dir = f'{path_db.split("/")[0]}/sihsus'
    if exists(data_dir):
        files = utils.get_files()
        tabelas = pd.DataFrame([
            (
                [file] + (
                    file
                    .split('.')[0]
                    .split('_')
                )
            ) for file in files
            ],
            columns = config.FNAME_COLS,
        ).sort_values(config.FNAME_COLS[0])
        month = config.FNAME_COLS[3]
        tabelas[month] = tabelas[month].astype(int)
    else:
        tabelas = dump_data(
            get_datasets(path_db)
        )

    return tabelas


def get_dict(
        path_db = config.PATH_DB,
        file_name = 'dict_SIH.csv'
    ):

    return dt.fread(
        f'{path_db}/{file_name}',
        sep = ';',
    )


def get_dict_zf(
        path_db = config.PATH_DB,
        file_name = 'dict_SIH.csv'
    ):

    return (
        pd.read_csv(
            (
                ZipFile(path_db)
                .open(
                    file_name,
                )
            ),
            sep = ';',
        )
    )


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


# Main

def main():
    
    load_sihsus().to_csv(
        'data/info/tabelas.csv',
        index = False)


__name__ == '__main__' and main()

