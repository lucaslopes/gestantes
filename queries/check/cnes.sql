select
	count(CNES)
from
	"datasus-sih"
-- where
-- 	True
-- select
-- 	count(H.CNES)
-- from
-- 	"datasus-sih" as H
-- 	inner join
-- 	"datasus-sinasc" as N
-- 	on H.CNES = N.CODESTAB
-- where -- 157033546
-- 	H.PROC_REA in ('0310010039', '0411010034') -- 23302307
-- 	and
-- 	N.ano_nasc between 2010 and 2019 -- 17109256
-- 	and
-- 	H.res_RSAUDCOD != 0 -- 17106725
-- 	and
-- 	H.res_SIGLA_UF != 'DF' -- 16817215
-- 	and
-- 	H.IDADE between 10 and 70 -- 16816760
-- 	and
-- 	N.def_parto != 'Ignorado' -- 29117865
-- group by
-- 	H.CNES