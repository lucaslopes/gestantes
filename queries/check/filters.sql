select
	count(*)
from
	"datasus-sih"
where -- 157033546
	PROC_REA in ('0310010039', '0411010034') -- 23302307
	and
	ano_internacao between 2010 and 2019 -- 17109256
	and
	res_RSAUDCOD != 0 -- 17106725
	and
	res_SIGLA_UF != 'DF' -- 16817215
	and
	IDADE >= 10 -- 16816760