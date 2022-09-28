select
    res_uf,
    ano,
    count(*) as partos
from
    partos
where
    parto = 'NORMAL'
    and
    res_macro_regiao_saude != int_macro_regiao_saude
    and
    res_uf == int_uf
group by
    res_uf, ano
order by
    partos desc
limit 1000