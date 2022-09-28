select count(CNES)
from "datasus-cnes"
where
	VINC_SUS = 1
	and
	CNES like '1%'
	and
	AP01CV01 = 1 -- 9006 -- Atendimento prestado Internação/Convênio SUS
	-- and
	-- AP02CV01 = 1 -- 115568 -- Atendimento prestado Atendimento Ambulatorial/Convênio SUS
	-- and
	-- AP03CV01 = 1 -- 37486 -- Atendimento prestado SADT/ Convênio SUS
	-- and
	-- AP04CV01 = 1 -- 14844 -- Atendimento prestado Urgência/Convênio SUS
	-- and
	-- AP05CV01 = 1 -- 10354 -- Atendimento prestado Outros/Convênio SUS
	-- and
	-- AP06CV01 = 1 -- 18892 -- Atendimento prestado Vigilância em Saúde/Convênio SUS
	-- and
	-- AP07CV01 = 1 -- 9030 -- Atendimento prestado Regulação/Convênio SUS
group by
	CNES