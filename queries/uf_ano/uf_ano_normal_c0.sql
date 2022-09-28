select
    res_uf,
    ano,
    count(*) as partos
from
    partos
where
    parto = 'NORMAL'
    and
    res_municipio == int_municipio
group by
    res_uf, ano
order by
    partos desc
limit 1000