begin;

delete from temp
where procedimento not like 'PARTO%';

INSERT INTO partos (ano, proc_rea, procedimento, cod_hosp, idade, raca_cor, res_regiao, res_uf, res_cod_municipio, res_municipio, res_regiao_saude, res_latitude, res_longitude, int_regiao, int_uf, int_cod_municipio, int_municipio, int_regiao_saude, int_latitude, int_longitude)
SELECT * FROM temp;

drop table temp;

commit;