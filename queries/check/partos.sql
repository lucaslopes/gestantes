select
	def_procedimento_realizado,
	count(def_procedimento_realizado) as records
from
	"datasus-sih"
where
	def_procedimento_realizado like 'PARTO%'
	and
	ano_internacao between 2010 and 2019 -- 17109256
	and
	res_RSAUDCOD != 0 -- 17106725
	and
	res_SIGLA_UF != 'DF' -- 16817215
	and
	IDADE between 10 and 60 -- 16816760
group by
	def_procedimento_realizado
order by
	count(def_procedimento_realizado) desc