select
	CODMUNNASC, -- CODMUNRES CODMUNNASC
	count(CODMUNNASC) as records
from
	"datasus-sinasc"
group by
	CODMUNNASC
order by
	count(CODMUNNASC) desc
-- where -- 74398079
-- 	ano_internacao between 2010 and 2019 -- 17109256
-- 	and
-- 	res_RSAUDCOD != 0 -- 17106725
-- 	and
-- 	res_SIGLA_UF != 'DF' -- 16817215
-- 	and
-- 	IDADE <= 18
-- group by
-- 	IDADE
-- order by
-- 	IDADE asc