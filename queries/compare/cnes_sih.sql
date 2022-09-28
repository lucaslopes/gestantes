select
	CNES -- count(distinct CNES)
from
	"datasus-sih"
where
	CNES like '1%'
	and
	PROC_REA in ('0310010039', '0411010034')
	-- and
	-- ano_internacao between 2010 and 2019
	-- and
	-- CNES is not null
	-- and
	-- res_RSAUDCOD != 0
	-- and
	-- res_SIGLA_UF != 'DF'
	-- and
	-- IDADE between 10 and 49
group by
	CNES
-- having
-- 	count(CNES) < UP_BOUND
-- 	and
-- 	count(CNES) >= LOW_BOUND
order by
-- 	count(CNES) desc,
	CNES asc
limit
	1000