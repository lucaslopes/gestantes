select
    res_uf,
    ano,
    count(*) as partos
from
    partos
where
    parto = 'CESARIANO'
    and
    res_regiao_saude != int_regiao_saude
    and
    res_macro_regiao_saude == int_macro_regiao_saude
group by
    res_uf, ano
order by
    partos desc
limit 1000