
import pandas as pd
import config
import utils

from os.path import isfile
from gdown import download
from zipfile import ZipFile
from datatable import dt, f


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
            by = config.FNAME_COLS[1:],
            ignore_index = True,
        )
    )


def dump_data(
        tabelas = get_datasets(),
        path_db = config.PATH_DB,
    ):

    new_tables = list()

    for row in tabelas.iterows():
        arquivo = row['Arquivo']
        current_path = f'{path_db}/{arquivo}'
        procs = config.RENAME['PROC_REA'].items()
        output = utils.get_path(arquivo, path_db)
        print(output, '\n', current_path)
        
        df = dt.fread(current_path)
        for cod, proc_name in procs:
            new_path =  f'{output}_{proc_name}.jay'
            df_proc = df[
                f['PROC_REA'] == cod,
                df.names,
            ]
            new_tables.append({
                'Arquivo' : f'{output.split("/")[-1]}_{proc_name}.jay',
                'UF' : row['UF'],
                'Ano' : row['Ano'],
                'Mês' : row['Mês'],
                'Parto' : proc_name,
                'Linhas' : df_proc.nrows,
                'Colunas' : df_proc.ncols,
            })
            df_proc.to_jay(new_path)
    
    return pd.DataFrame(new_tables)


def load_sihsus(
        url = config.URL_DB,
        path_db = config.PATH_DB,
    ):
    
    download_database(url, path_db)
    tabelas = get_datasets(path_db)
    tabelas = dump_data(tabelas)

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
    
    return dump_data()


__name__ == '__main__' and main()

