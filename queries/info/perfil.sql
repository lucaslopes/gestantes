select
	idade,
	nivel_escolaridade,
	raca_cor,
	tipo_parto,
	res_cod_municipio,
	hosp_cod_municipio,
	res_cod_regiao_saude,
	hosp_cod_regiao_saude,
	raca_cor_nascido,
	apgar1,
	apgar5,
	count(*) as records
from
	sinasc
where
	ano between 2010 and 2011
	and
	idade between 10 and 49
	and
	n_gestados = 1 -- Única
	and
	consultas_pre_natal != "Ignorado"
	and
	nivel_escolaridade != 9
	and
	raca_cor != 9
	and
	raca_cor_nascido != "Ignorado"
	and
	raca_cor is not null
	and
	apgar1 between 0 and 10
	and
	apgar5 between 0 and 10
group by
	idade,
	consultas_pre_natal,
	nivel_escolaridade,
	raca_cor,
	tipo_parto,
	res_cod_municipio,
	hosp_cod_municipio,
	res_cod_regiao_saude,
	hosp_cod_regiao_saude,
	raca_cor_nascido,
	apgar1,
	apgar5
order by
	count(*) desc
-- limit 10000