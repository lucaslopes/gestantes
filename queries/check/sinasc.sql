select
	count(*) as records
from
	"datasus-sinasc"
where -- 74398079
	ano_nasc between 2010 and 2019 -- 29157184
	and
	IDADEMAE between 10 and 49 -- 29152867
	and
	PARTO != 9 -- 29113721
	and
	LOCNASC = 1 -- Hospital -- 28633228
	and
	CODESTAB is not null -- 28631784
	and
	nasc_codigo_adotado is not null -- 28631784
	and
	nasc_RSAUDCOD is not null -- 28631784
	and
	res_codigo_adotado is not null -- 28631784
	and
	res_RSAUDCOD is not null -- 28631784
	and
	res_RSAUDCOD != 5301 -- 28197164