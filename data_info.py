

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


def ncols_per_year_uf(df):
    cols = ['UF', 'Ano', 'Colunas']
    return (
        df[cols]
        .groupby(
            cols,
            as_index=False
        )
        .count()
        .pivot(
            *['Ano', 'UF', 'Colunas']
        )
        .sort_values(
            by = 'Ano',
            ascending = False,
        )
    )

def nrows_per_year_uf(df):
    cols = ['UF', 'Ano', 'Mês', 'Parto', 'Linhas']
    colunas = (
        df
        [cols]
        .groupby(
            cols,
            as_index=False
        )
        .count()
        [['UF', 'Ano', 'Linhas']]
        .groupby(
            cols[:2],
            as_index=False
        )
        .sum()
    )
    ufs_order = (
        colunas
        [['UF', 'Linhas']]
        .groupby('UF')
        .sum()
        .sort_values(
            'Linhas',
            ascending=False
        )
        .index
    )
    return (
        colunas
        .pivot(
            *['Ano', 'UF', 'Linhas']
        )
        .sort_values(
            by = 'Ano',
            ascending = False,
        )
        [ufs_order]
    )


def calc_prop(df):
    cols = ['UF', 'Ano', 'Mês', 'Parto', 'Linhas']
    columns = (
        df
        [cols]
        .groupby(
            cols,
            as_index=False
        )
        .count()
        [['UF', 'Ano', 'Parto', 'Linhas']]
        .groupby(
            ['UF', 'Ano', 'Parto'],
            as_index=False
        )
        .sum()
    )
    nor = columns[columns['Parto'] == 'NORMAL']['Linhas'].values
    ces = columns[columns['Parto'] == 'CESARIANO']['Linhas'].values
    nor_prop = nor / (nor + ces)
    cls = columns[['UF', 'Ano']].groupby(['UF', 'Ano'], as_index=False).count()
    cls['prop'] = nor_prop
    ufs_order = (
        cls
        [['UF', 'prop']]
        .groupby('UF')
        .sum()
        .sort_values(
            'prop',
            ascending=False
        )
        .index
    )
    return (
        cls
        .pivot(
            *['Ano', 'UF', 'prop']
        )
        .sort_values(
            by = 'Ano',
            ascending = False,
        )
        [ufs_order]
    )



def var_diff_per_year_uf(df, var):
    cols = ['Variável', 'Diferentes']
    res = (
        df
        [cols]
        .groupby(
            cols[0],
            as_index = False
        )
        .sum()
        .sort_values(
            cols[1],
            ascending = False,
        )
    )
    relevantes = [
        [
            'codigo_adotado',
            'Armazena o código atribuído ao município, tratando os casos em que múltiplos códigos tenham sido utilizados para um mesmo município ao longo do tempo',
        ],
        [
            'MUNNOMEX',
            'Nome (sem acentos, em maiúsculas) do Município',
        ],
        [
            'REGIAO',
            'Região do Brasil (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)'
        ],
        [
            'FRONTEIRA',
            'Indica (S ou N) se o município faz parte da faixa de fronteira (conforme IBGE)',
        ],
        [
            'AMAZONIA',
            'Indica (S ou N) se o município faz parte da Amazônia Legal (conforme IBGE)',  # Diferentes significa quantos links entre Amazônia Legal com demais regiões
        ],
        [
            'SIGLA_UF',
            'Sigla da unidade da federação',
        ],
        [
            'CAPITAL',
            'Indica (S ou N) se o município é capital da UF', # Diferentes significa quantos links entre capital com demais municípios
        ],
        [
            'MSAUDCOD',
            'Código da Macrorregional de Saúde a que o Município pertence',
        ],
        [
            'RSAUDCOD',
            'Código da Regional de Saúde a que o Município pertence',
        ],
        [
            'CSAUDCOD',
            'Código da Microrregional de Saúde a que o Município pertence'
        ],
    ]
    rel = pd.DataFrame(relevantes, columns=['Variável', 'Descrição'])
    variaveis = res[res['Variável'].isin(rel['Variável'])]
    variaveis.merge(
        rel,
        on = 'Variável',
    )
    cols = ['UF', 'Ano', 'Linhas', 'Diferentes']
    diffs = (
        df
        [df['Variável'] == var]
        [cols]
        .groupby(
            by=cols[:2],
            as_index=False,
        )
        .sum()
    )
    diffs['Prop'] = diffs['Diferentes'] / diffs['Linhas']
    ufs_order = (
        diffs
        .groupby(
            'UF',
            as_index=False
        )
        .mean()
        .sort_values(
            'Prop',
            ascending=False,
        )
        ['UF']
        .values
    )
    return (
        diffs
        .pivot(
            *['Ano', 'UF', 'Prop']
        )
        .sort_values(
            by = 'Ano',
            ascending = False,
        )
        [ufs_order]
    )




def var_prop_per_parto(df, var, ufs_order):
    cols = ['UF', 'Ano', 'Parto', 'Linhas', 'Diferentes']
    df_diffs = (
        df
        [df['Variável'] == var]
        [cols]
        .groupby(
            cols[:3],
            as_index=False,
        )
        .sum()
    )
    diff_ces = df_diffs[df_diffs['Parto'] == 'CESARIANO'].copy()
    diff_nor = df_diffs[df_diffs['Parto'] == 'NORMAL'].copy()

    diff_ces['Prop'] = diff_ces['Diferentes'] / diff_ces['Linhas']
    diff_nor['Prop'] = diff_nor['Diferentes'] / diff_nor['Linhas']

    ces_vals = diff_ces['Prop'].values
    nor_vals = diff_nor['Prop'].values
    prop_prop = nor_vals / (nor_vals + ces_vals)

    diff_final = diff_ces[cols[:2]].copy()
    diff_final['Prop'] = prop_prop
    return (
        diff_final
        .pivot(
            *['Ano', 'UF', 'Prop']
        )
        .sort_values(
            by = 'Ano',
            ascending = False,
        )
        [ufs_order]
    )  