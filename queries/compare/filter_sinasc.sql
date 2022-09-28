select
	count(*) as records
from
	"datasus-sinasc"
where
	ano_nasc between 2010 and 2019
	and
	IDADEMAE between 10 and 49
	and
	PARTO != 9
	and
	LOCNASC = 1 -- Hospital
	and
	CODESTAB is not null
	and
	nasc_codigo_adotado is not null
	and
	nasc_RSAUDCOD is not null
	and
	res_codigo_adotado is not null
	and
	res_RSAUDCOD is not null
	and
	res_RSAUDCOD != 5301