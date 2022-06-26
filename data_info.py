

import pandas as pd
import config, data_load

from collections import Counter


#############################################


def compare_prefix_pair(
        arqv,
        pair = ['res', 'int'],
    ):

    c = Counter()
    df = data_load.open_jay_dataset(arqv)
    
    for n in df.names:
        c.update([
            n.split('_')[0]
        ])
    
    df_prefix = pd.DataFrame(
        c.most_common(),
        columns=['prefix', 'columns']
    )
    
    idxs = list()
    for pref in pair:
        idxs.append(
            df_prefix[
                df_prefix['prefix'] == pref
            ].index[0]
        )
    
    return (
        df_prefix['columns'][idxs[0]]
        ==
        df_prefix['columns'][idxs[1]]
    )


def prefix_same_pair(
        arqv,
        pair = ['res', 'int'],
    ):

    df = data_load.open_jay_dataset(arqv)    
    pair_names = [n[len(p)+1:]
        for p in pair
            for n in df.names if (
                n[:len(p)] == p
            ) 
    ]
    c = Counter(pair_names)
    
    return (
        sum(c.values())
        ==
        2 * len(c)  # 2 * 20
    )


#############################################


def groupby_uf_year_month(
        tabelas,
        col_names = config.FNAME_COLS,
    ):
    
    return (
        tabelas
        .groupby(
            by = col_names[1:4],
            as_index = False,
        )
        .count()
        [col_names[1:4]]
    )


def groupby_uf_year(
        tabelas,
        col_names = config.FNAME_COLS,
    ):
    
    return pd.DataFrame((
        tabelas
        .groupby(
            by = col_names[1:3],
            as_index = False,
        )
        .count()
    ))


def months_per_year_uf(
        tabelas,
    ):
    
    if 'Parto' in tabelas.columns:
        tabelas = groupby_uf_year_month(tabelas)
    tabelas = groupby_uf_year(tabelas)

    return (
        tabelas
        .pivot(
            *['Ano', 'UF', 'Mês']
        )
        .sort_values(
            by = 'Ano',
            ascending = False,
        )
    )


def dict_type_count(
        df
    ):
    
    df = df.to_pandas()

    return (
        df
        .groupby(
            by = 'Tipo',
            as_index = False,
        )
        .count()
        [['Tipo', 'Coluna']]
    )