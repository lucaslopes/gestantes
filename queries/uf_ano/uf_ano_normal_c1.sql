select
    res_uf,
    ano,
    count(*) as partos
from
    partos
where
    parto = 'NORMAL'
    and
    res_municipio != int_municipio
    and
    res_micro_regiao_saude == int_micro_regiao_saude
group by
    res_uf, ano
order by
    partos desc
limit 1000