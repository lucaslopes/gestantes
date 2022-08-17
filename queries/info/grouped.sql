select
	P.ano,
	P.parto,
	PL.regiao,
	PL.uf,
	PL.grupo,
	P.mov_municipio,
	P.mov_regiao_saude,
	count(*) as records
from
	partos P
	left join
	places PL
	on
		P.res_cod_municipio = PL.cod_municipio
where
	ano between 2010 and 2019
	and
	grupo != '0'
	and
	not (P.mov_municipio = 0 and P.mov_regiao_saude = 1)
group by
	P.ano,
	P.parto,
	PL.regiao,
	PL.uf,
	PL.grupo,
	P.mov_municipio,
	P.mov_regiao_saude
order by
	ano asc,
	records desc