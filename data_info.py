
import config
import pandas as pd


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