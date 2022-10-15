import os
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from zipfile import ZipFile
from datatable import dt, f, by
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from plotly import express as px, io as pio

pd.options.plotting.backend = 'plotly'
pio.renderers.default = 'plotly_mimetype+notebook_connected'

# Retornar o caminho do arquivo
def get_path(dir_name, file_name):
  return f'{Path.home()}/Databases/{dir_name}/{file_name}'

# Listar arquivos no ZIP
def get_zip_namelist(zip_path):
  files = ZipFile(zip_path).namelist()
  files = [f'{zip_path}/{f}'
    for f in files if 'dict' not in f]
  return files

# Abrir uma tabela
def read_table(table_path, columns):
  cols_order = list(columns.values())
  columns[...] = None
  df = dt.fread(table_path, columns=columns)
  return df

# Carregar tabelas do ZIP
def data_load(zip_path, cols, filter_func):
  files = get_zip_namelist(zip_path)
  dfs = list()
  for file_path in tqdm(files):
    df = read_table(file_path, cols)
    df = filter_func(df, cols)
    dfs.append(df)
  df = dt.rbind(*dfs)
  return df

# Agrupar por colunas
def group_cols(df_base, cols):
  df = df_base[:, cols]
  df['count'] = 1
  df = df[:, dt.sum(f.count), by(cols)]
  return df