

import os
import sqlite3
import numpy as np
import pandas as pd
import config


from tqdm import tqdm
from sklearn.preprocessing import normalize
from sklearn.linear_model import LinearRegression


CONX = sqlite3.connect(config.PATH_DB)


def save_queries_result():
  for query in tqdm(os.listdir(config.PATH_QUERIES)):
    with open(f'{config.PATH_QUERIES}/{query}') as f:
      q = f.read()
      df = pd.read_sql(q, con=CONX)
      df = df.pivot(*['ano', 'res_uf', 'partos'])
      df = df.sort_values(by='ano', ascending=False)
      csv_name = query.replace('sql', 'csv.xz')
      df.to_csv(f'{config.PATH_DATA}/{csv_name}')
    

def aggregate_matrix_pairs(cs=range(6)):
  for i in cs:
    ambos = list()
    for tipo in ['normal', 'cesariano']:
      ambos.append(pd.read_csv(
        f'data/xz/uf_ano_{tipo}_c{i}.csv.xz',
        index_col=0))
    nor, ces = ambos
    ambos = pd.DataFrame(
      nor.values + ces.values,
      columns=nor.columns,
      index=nor.index)
    ambos.to_csv(
      f'data/xz/uf_ano_ambos_c{i}.csv.xz',
    )
    # pd.read_csv(
    #   f'data/xz/uf_ano_ambos_c{i}.csv.xz',
    #   index_col=0)


def get_linreg_params(x, y):
	reg = LinearRegression().fit(x, y)
	angle = reg.coef_[0][0]
	intercept = reg.intercept_[0]
	return angle, intercept


def get_ano_partos(df, uf=None):
  cols = [uf] if uf else df.columns
  df = pd.DataFrame(
    df[cols].sum(axis=1)[1:-1],
    columns=['partos']
  ).reset_index(level=0)
  ano = np.linspace(
    0, 1, 2 + len(df['ano'])
  ).reshape(-1, 1)[1:-1][::-1]
  partos = normalize(
    df['partos'].array.reshape(-1, 1),
    norm='max',
    axis=0)
  return ano, partos


def get_params_per_uf(df):
  inputs = list()
  ufs = np.append(df.columns, [None])
  for uf in ufs:
    ano, partos = get_ano_partos(df, uf)
    d = {'uf' : uf if uf else 'BR'}
    d['regiao'] = config.UF_REGIAO[d['uf']]
    d['angle'], d['intercept'] = (
      get_linreg_params(ano, partos))
    inputs.append(d)
  return pd.DataFrame(inputs)


def main():
	return save_queries_result()


__name__ == '__main__' and main()

