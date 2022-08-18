select
	P.momento,
	P.parto,
	PL.regiao,
	PL.uf,
	PL.grupo,
	P.criticidade,
	count(*) as records
from
	partos P
	left join
	places PL
	on P.res_cod_municipio = PL.cod_municipio
group by
	P.momento,
	P.parto,
	PL.regiao,
	PL.uf,
	PL.grupo,
	P.criticidade
order by
	records desc