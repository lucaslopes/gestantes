

import os
from pathlib import Path


URL_DB = ''.join([
	'https://drive.google.com/',
	'uc?id=',
	'149l5K6rEXWZ6MhIfSsatSN_Q5Esum7x1',
])


PATH_SIHSUS = os.path.join(*[
		str(Path.home()),
		'storage',
		'databases',
		'sihsus',
])


PATH_DB = os.path.join(*[
		PATH_SIHSUS,
		'SIHSUS.zip',
])


PATH_JAY = os.path.join(*[
		PATH_SIHSUS,
		'jay',
])


LOCAL_DATA = os.path.join(*[
		os.getcwd(),
		'data',
])


LOCAL_SIHSUS = os.path.join(*[
		LOCAL_DATA,
		'info',

])


LOCAL_FILES = {
	'format' : 'pkl',
	'compression' : 'xz',
}


LOCAL_SIHSUS = os.path.join(*[
	LOCAL_DATA,
	'info',
	'.'.join([
		'sihsus',
		LOCAL_FILES['format'],
		LOCAL_FILES['compression'],
	])
])


LOCAL_DICT = os.path.join(*[
	LOCAL_DATA,
	'info',
	'.'.join([
		'dict',
		LOCAL_FILES['format'],
		LOCAL_FILES['compression'],
	])
])


FNAME_PAT = '_(.*)_t.csv$'


FNAME_COLS = [
	'Arquivo',
	'UF',
	'Ano',
	'Mês',
	'Parto',
	'Linhas',
	'Colunas',
	'Variável',
	'Diferentes',
]


FILTERS = {
		'PROC_REA' : [
				310010039,
				411010034,
		],
}


RENAME = {
	'PROC_REA' : {  # http://sigtap.datasus.gov.br/tabela-unificada/app/sec/inicio.jsp
		310010039 : 'NORMAL',     # 03.10.01.003-9 - PARTO NORMAL
		411010034 : 'CESARIANO',  # 04.11.01.003-4 - PARTO CESARIANO
	},
}


RES_INT_VARS = [
	[
		'REGIAO',
		'Região do Brasil (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)'
	],
	[
		'SIGLA_UF',
		'Sigla da unidade da federação',
	],
	[
		'MSAUDCOD',
		'Código da Macrorregional de Saúde a que o Município pertence',
	],
	[
		'RSAUDCOD',
		'Código da Regional de Saúde a que o Município pertence',
	],
	[
		'CSAUDCOD',
		'Código da Microrregional de Saúde a que o Município pertence'
	],
	[
		'MUNNOMEX',
		'Nome (sem acentos, em maiúsculas) do Município',
	],
	[
		'codigo_adotado',
		'Armazena o código atribuído ao município, tratando os casos em que múltiplos códigos tenham sido utilizados para um mesmo município ao longo do tempo',
	],
	[
		'CAPITAL',
		'Indica (S ou N) se o município é capital da UF', # Diferentes significa quantos links entre capital com demais municípios
	],
	[
		'FRONTEIRA',
		'Indica (S ou N) se o município faz parte da faixa de fronteira (conforme IBGE)',
	],
	[
		'AMAZONIA',
		'Indica (S ou N) se o município faz parte da Amazônia Legal (conforme IBGE)',  # Diferentes significa quantos links entre Amazônia Legal com demais regiões
	],
]


#############################################
# Main

def main():
		
	print(FNAME_COLS)


__name__ == '__main__' and main()

