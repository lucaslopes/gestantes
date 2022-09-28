select
	IDADEMAE as idade,
	CONSULTAS as consultas,
	ESCMAE as nivel_escolaridade,
	RACACORMAE as raca_cor,
	def_parto as tipo_parto,
	res_codigo_adotado as res_cod_municipio,
	nasc_codigo_adotado as hosp_cod_municipio,
	res_RSAUDCOD as res_cod_regiao_saude,
	nasc_RSAUDCOD as hosp_cod_regiao_saude,
	def_raca_cor as raca_cor_nascido,
	def_sexo as sexo_nascido,
	floor(PESO/100.00)*100 as peso_nascido,
	APGAR1 as apgar1,
	APGAR5 as apgar5,
	count(*) as records
from
	"datasus-sinasc"
where
	ano_nasc between 2010 and 2011
	and
	IDADEMAE between 10 and 49
	and
	CODESTAB is not null -- além de VINC_SUS
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
	and
	LOCNASC = 1 -- Hospital
	and
	GRAVIDEZ = 1 -- Única
	and
	CONSULTAS != 9
	and
	PARTO != 9
	and
	ESCMAE != 9
	and
	RACACORMAE != 9
	and
	RACACOR != 9
	and
	RACACORMAE is not null
	and
	SEXO != 0
	and
	PESO between 500 and 5000
	and
	APGAR1 between 0 and 10
	and
	APGAR5 between 0 and 10
group by
	IDADEMAE,
	CONSULTAS,
	ESCMAE,
	RACACORMAE,
	def_parto,
	res_codigo_adotado,
	res_RSAUDCOD,
	nasc_codigo_adotado,
	nasc_RSAUDCOD,
	def_raca_cor,
	def_sexo,
	APGAR1,
	APGAR5,
	floor(PESO/100.00)*100
order by
	floor(PESO/100.00)*100 asc
limit 1000