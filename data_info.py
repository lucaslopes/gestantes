

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


#############################################


def ncols_per_year_uf(
        df,
        cols = ['UF', 'Ano', 'Colunas']
    ):
    
    return (
        df
        [cols]
        .groupby(
            cols,
            as_index = False,
        )
        .count()
        .pivot(
            *[cols[1], cols[0], cols[-1]]
        )
        .sort_values(
            by = cols[1],
            ascending = False,
        )
    )


def nrows_per_year_uf(
        df,
        cols = ['UF', 'Ano', 'Mês', 'Parto', 'Linhas']
    ):

    colunas = (
        df
        [cols]
        .groupby(
            cols,
            as_index=False
        )
        .count()
        [[cols[0], cols[1], cols[-1]]]
        .groupby(
            cols[:2],
            as_index = False,
        )
        .sum()
    )
    ufs_order = (
        colunas
        [[cols[0], cols[-1]]]
        .groupby(cols[0])
        .sum()
        .sort_values(
            cols[-1],
            ascending = False,
        )
        .index
    )
    return (
        colunas
        .pivot(
            *[cols[1], cols[0], cols[-1]]
        )
        .sort_values(
            by = cols[1],
            ascending = False,
        )
        [ufs_order]
    )


def calc_prop(
        df,
        cols = ['UF', 'Ano', 'Mês', 'Parto', 'Linhas']
    ):
    
    columns = (
        df
        [cols]
        .groupby(
            cols,
            as_index = False,
        )
        .count()
        [[cols[0], cols[1], cols[-2], cols[-1]]]
        .groupby(
            [cols[0], cols[1], cols[-2]],
            as_index = False,
        )
        .sum()
    )
    nor = columns[columns['Parto'] == 'NORMAL']['Linhas'].values
    ces = columns[columns['Parto'] == 'CESARIANO']['Linhas'].values
    nor_prop = nor / (nor + ces)
    cls = (
        columns
        [cols[:2]]
        .groupby(
            cols[:2],
            as_index = False,
        )
        .count()
    )
    cols.append('Prop')
    cls[cols[-1]] = nor_prop
    ufs_order = (
        cls
        [[cols[0], cols[-1]]]
        .groupby(
            by = cols[0],
        )
        .sum()
        .sort_values(
            by = cols[-1],
            ascending = False,
        )
        .index
    )
    
    return (
        cls
        .pivot(
            *[cols[1], cols[0], cols[-1]]
        )
        .sort_values(
            by = cols[1],
            ascending = False,
        )
        [ufs_order]
    )


def var_diff_per_year_uf(
        df,
        var,
        cols = None,
    ):
    
    cols = ['UF', 'Ano', 'Linhas', 'Variável', 'Diferentes'] if cols is None else cols

    res = (
        df
        [cols[-2:]]
        .groupby(
            by = cols[-2],
            as_index = False,
        )
        .sum()
        .sort_values(
            by = cols[-1],
            ascending = False,
        )
    )
    rel = pd.DataFrame(
        config.RES_INT_VARS,
        columns = cols[-2:]
    )
    variaveis = (
        res
        [res[cols[-2]].isin(rel[cols[-2]])]
    )
    variaveis.merge(
        rel,
        on = cols[-2],
    )
    diffs = (
        df
        [df[cols[-2]] == var]
        [cols]
        .groupby(
            by = cols[:2],
            as_index = False,
        )
        .sum()
    )
    cols.append('Prop')
    diffs[cols[-1]] = diffs[cols[-2]] / diffs[cols[2]]
    ufs_order = (
        diffs
        .groupby(
            by = cols[0],
            as_index = False,
        )
        .mean()
        .sort_values(
            by = cols[-1],
            ascending = False,
        )
        [cols[0]]
        .values
    )
    return (
        diffs
        .pivot(
            *[cols[1], cols[0], cols[-1]]
        )
        .sort_values(
            by = cols[1],
            ascending = False,
        )
        [ufs_order]
    )


def var_prop_per_parto(
        df,
        var,
        ufs_order,
        partos = {'ces' : 'CESARIANO', 'nor' : 'NORMAL'},
        cols = None,
    ):

    cols = ['UF', 'Ano', 'Parto', 'Linhas', 'Diferentes'] if cols is None else cols

    df_diffs = (
        df
        [df['Variável'] == var]
        [cols]
        .groupby(
            by = cols[:3],
            as_index = False,
        )
        .sum()
    )

    diff_ces = df_diffs[df_diffs[cols[2]] == partos['ces']].copy()
    diff_nor = df_diffs[df_diffs[cols[2]] == partos['nor']].copy()
    cols.append('Prop')
    diff_ces[cols[-1]] = diff_ces[cols[-2]] / diff_ces[cols[-3]]
    diff_nor[cols[-1]] = diff_nor[cols[-2]] / diff_nor[cols[-3]]
    ces_vals = diff_ces[cols[-1]].values
    nor_vals = diff_nor[cols[-1]].values
    prop_prop = nor_vals / (nor_vals + ces_vals)
    diff_final = diff_ces[cols[:2]].copy()
    diff_final[cols[-1]] = prop_prop
    
    return (
        diff_final
        .pivot(
            *[cols[1], cols[0], cols[-1]]
        )
        .sort_values(
            by = cols[1],
            ascending = False,
        )
        [ufs_order]
    )  