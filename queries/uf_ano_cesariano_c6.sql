select
    res_uf,
    ano,
    count(*) as partos
from
    partos
where
    parto = 'CESARIANO'
    and
    res_regiao != int_regiao
group by
    res_uf, ano
order by
    partos desc
limit 1000