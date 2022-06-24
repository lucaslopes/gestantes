URL_DB = 'https://drive.google.com/uc?id=149l5K6rEXWZ6MhIfSsatSN_Q5Esum7x1'
PATH_DB = 'data/SIHSUS.zip'
PATH_SIHSUS = 'data/sihsus'
PATH_DICT = 'data/info/dict_cols.csv'
FNAME_COLS = ['Arquivo', 'UF', 'Ano', 'Mês', 'Parto', 'Linhas', 'Colunas']


FILTERS = {
    'PROC_REA' : [
        310010039,
        411010034,
    ],
}


RENAME = {
  'PROC_REA' : {
    310010039 : 'nat',
    411010034 : 'cir',
  },
}

