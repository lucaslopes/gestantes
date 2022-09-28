select
	res_codigo_adotado,
	int_codigo_adotado,
	count(*) as procedimentos
from
	"datasus-sih"
where 
	PROC_REA = '0310010039' -- in ('0310010039', '0411010034')
	and
	ano_internacao between 2018 and 2019
	and
	CNES is not null
	and
	res_RSAUDCOD != 0
	and
	res_SIGLA_UF = 'RJ'
	and
	IDADE between 10 and 49
group by
	res_codigo_adotado,
	int_codigo_adotado
-- having
-- 	count(*) = 1
order by
	count(*) desc