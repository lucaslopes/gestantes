

import pandas as pd


def months_per_year_uf(
        tabelas
    ):
    
    return (
        pd.DataFrame(
        (
            tabelas
            .groupby(
                by = ['UF', 'Ano'],
                as_index = False,
            )
            .count()
        ))
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