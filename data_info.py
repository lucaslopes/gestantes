

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
	slope = reg.coef_[0][0]
	intercept = reg.intercept_[0]
	return slope, intercept


def get_ano_partos(df, uf=None):
  cols = [uf] if uf else df.columns
  df = pd.DataFrame(
    df[cols].sum(axis=1), # [1:-1] TODO: remove 2007 and 2021
    columns=['partos']
  ).reset_index(level=0)
  ano = np.linspace(
    0, 1, 2 + len(df['ano'])
  ).reshape(-1, 1)[1:-1][::-1]
  mean = df['partos'].mean()
  partos = df['partos'].array.reshape(-1, 1)
  partos = normalize(partos, norm='max', axis=0)
  return ano, partos, mean


def get_params_per_uf(df):
  inputs = list()
  ufs = df.columns # np.append(df.columns, [None])
  for uf in ufs:
    ano, partos, mean = get_ano_partos(df, uf)
    d = {'uf' : uf if uf else 'BR'}
    d['regiao'] = config.UF_REGIAO[d['uf']]
    d['mean'] = mean
    d['slope'], d['intercept'] = (
      get_linreg_params(ano, partos))
    inputs.append(d)
  return pd.DataFrame(inputs)


def generate_plots(fnames):
  d = dict()
  for fname in fnames:
    df = pd.read_csv(
			f'data/xz/{fname}.csv.xz',
			index_col=0)
    if fname[-2] == 'c':
      base = pd.read_csv(
				f'data/xz/{fname[:-2]}.csv.xz',
				index_col=0)[df.columns]
      df = pd.DataFrame(
				df.values / base.values,
				columns=base.columns,
				index=base.index)
    label = fname.split('_')[-2]
    d[label] = (
      get_params_per_uf(df))
  return d


def get_data_matrix(fnames):
  d = dict()
  r_labels = ['todos', 'mun diff', 'reg sau diff']
  c_labels = ['ambos', 'normal', 'cesaria']
  for r_label, df_names in zip(r_labels, fnames):
    d[r_label] = dict()
    for c_label, df_name in zip(c_labels, df_names):
      df = pd.read_csv(
        f'data/xz/{df_name}.csv.xz',
        index_col=0)
      if df_name[-2] == 'c':
        base = pd.read_csv(
          f'data/xz/{df_name[:-2]}.csv.xz',
          index_col=0)[df.columns]
        df = pd.DataFrame(
          df.values / base.values,
          columns=base.columns,
          index=base.index)
      d[r_label][c_label] = get_params_per_uf(df)
  return d


def get_data_matrix(fnames):
  data = dict()
  partos = set()
  critic_labels = {
    '': 'todos', 'c1': 'mun diff', 'c3': 'reg sau diff'}
  divisors = [
    ['mun diff', 'todos'],
    ['reg sau diff', 'mun diff']]
  for fname in fnames:
    infos = fname.split('_')
    parto, critic = infos[-2], critic_labels[infos[-1]]
    if critic not in data: data[critic] = dict()
    partos.add(parto)
    df = pd.read_csv(
      f'data/xz/{fname}.csv.xz',
      index_col=0)
    data[critic][parto] = df
  for parto in partos:
    for num, div in divisors:
      df = data[num][parto]
      base = data[div][parto][df.columns]
      data[num][parto] = pd.DataFrame(
        df.values / base.values,
        columns=base.columns,
        index=base.index)
  for critic in critic_labels.values():
    for parto in partos:
      data[critic][parto] = get_params_per_uf(
        data[critic][parto])
  return data


def get_files_path(folder):
  return [f'{dir}/{dt}'
    for dir, _, datasets in os.walk(folder)
      for dt in datasets if (
        dt.endswith('csv.xz'))]


def dict_data_to_matrix(dict_data):
  matrix = [[None for _ in range(3)]
		for _ in range(3)]
  col = {'ambos':0, 'normal':1, 'cesariano':2}
  row = {'':0, 'municipio':1, 'regsau':2}
  for name, data in dict_data.items():
    infos = name.split('.')[0].split('_')
    parto, local = infos[-2], infos[-1]
    matrix[row[local]][col[parto]] = data
  return matrix


def matrix_fraction(m):
	dens = [2, 1]
	for den in dens:
		for i in range(3):
			m[den][i] = m[den][i] / m[den-1][i]
	for j in dens:
		m[0][j] = m[0][j] / m[0][0]
	br = pd.DataFrame(index=m[0][0].index)
	brasil = m[0][0].sum(axis=1)
	for uf in m[0][0].columns:
		br[uf] = brasil
	m[0][0] = m[0][0] / br
	return m


def matrix_info(m):
  for row, dfs in enumerate(m):
    for col, df in enumerate(dfs):
      m[row][col] = get_params_per_uf(df)
  return m


def get_matrix_data(data):
  return (
    matrix_info(
      matrix_fraction(
        dict_data_to_matrix(data))))


def distance(x1, y1, x2, y2):
  dx = (x2 - x1) ** 2
  dy = (y2 - y1) ** 2
  return np.sqrt(dx + dy)


def get_rank(df, dist_asc=True):
  mean, slope = df['mean'], df['slope']
  df['dist'] = distance(slope, mean, 1, 1)
  rank = df.sort_values(
    by='dist', ascending=dist_asc
  )['uf'].values
  return rank


def matrix_rank(matrix, ys):
  states = set()
  asc = [
    [True,True,True],
    [False,False,False],
    [False,False,False]]
  df = pd.DataFrame(index=range(1,28))
  df.index.name = 'rank'
  for i in range(3):
    for j in range(3):
      label = ys[i][j]
      data = matrix[i][j]
      dist_asc = asc[i][j]
      rank = get_rank(data, dist_asc)
      states.update(set(rank))
      missing = states - set(rank)
      if len(missing) > 0:
        rank = np.append(rank, list(missing))
      df[label] = rank
  return df


def group_years_by_period(df, years=None):
  years = (
		[y for years in config.PERIODS for y in years]
		if years is None
		else years)
  df_cut = df.loc[years,:]
  groups = list()
  for years in config.PERIODS:
    p = df_cut.loc[years,:]
    groups.append(p.sum(axis=0))
  dfs = list()
  for i, g in enumerate(groups):
    df = pd.DataFrame(g).transpose()
    df.index = [i + 1]
    dfs.append(df)
  df = pd.concat(dfs)
  df.index.names = ['ano']
  return df


def main():
	return save_queries_result()


__name__ == '__main__' and main()

