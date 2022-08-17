with

brasil as (
	select
		ano,
		parto,
		count(*) as quantity
	from
		partos P
		left join
		places PL
		on
			P.res_cod_municipio = PL.cod_municipio
	where
		PL.uf is not null
		and
		ano between 2010 and 2019
	group by
		ano,
		parto
),

municipal as (
	select
		ano,
		parto,
		count(*) as quantity
	from
		partos P
		left join
		places PL
		on
			P.res_cod_municipio = PL.cod_municipio
	where
		PL.uf is not null
		and
		mov_municipio = 1
		and
		ano between 2010 and 2019
	group by
		ano,
		parto
),

regional as (
	select
		ano,
		parto,
		count(*) as quantity
	from
		partos P
		left join
		places PL
		on
			P.res_cod_municipio = PL.cod_municipio
	where
		PL.uf is not null
		and
		mov_regiao_saude = 1
		and
		ano between 2010 and 2019
	group by
		ano,
		parto
),

frac_municipal as (
	select
		M.ano as ano,
		M.parto as parto,
		'municipal' as scope,
		100.0 * M.quantity / B.quantity as percent
	from
		municipal M
		left join
		brasil B
		on
			M.ano = B.ano
			and
			M.parto = B.parto
	group by
		M.ano,
		M.parto
),

frac_regional as (
	select
		R.ano as ano,
		R.parto as parto,
		'regional' as scope,
		100.0 * R.quantity / M.quantity as percent
	from
		regional R
		left join
		municipal M
		on
			R.ano = M.ano
			and
			R.parto = M.parto
	group by
		R.ano,
		R.parto
),

frac as (
	select * from frac_municipal M
	union
	select * from frac_regional M
)

select * from frac