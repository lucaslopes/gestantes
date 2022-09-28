select
	res_cod_municipio,
	int_cod_municipio,
	count(*) as records
from
	partos
group by
	res_cod_municipio,
	int_cod_municipio
order by
	records desc