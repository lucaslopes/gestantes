

import os
import sqlite3
import pandas as pd
import config


from tqdm import tqdm


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
    

def main():
	return save_queries_result()


__name__ == '__main__' and main()

