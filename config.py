

import os
from pathlib import Path


PATH_SIHSUS = os.path.join(*[
	str(Path.home()),
	'Databases',
	'SIHSUS',
])


PATH_DB = os.path.join(*[
	PATH_SIHSUS,
	'sihsus.db',
])


PATH_SIHSUS_ZIP = '/Volumes/SanDisk/SIHSUS.zip'
PATH_DATA = 'data'
PATH_QUERIES = 'queries'


PARTO = { # http://sigtap.datasus.gov.br/tabela-unificada/app/sec/inicio.jsp
	310010039 : 'NORMAL', # 03.10.01.003-9 - PARTO NORMAL
	411010034 : 'CESARIANO', # 04.11.01.003-4 - PARTO CESARIANO
}


PERIODS = [[2010, 2011], [2014, 2015], [2018,2019]]


ESCOLARIDADE = {
	0 : 'NaN',
	1 : 'Analfabeto',
	2 : 'Primeiro',
	3 : 'Segundo',
	4 : 'Terceiro',
}


ETNIA = {
	99 : 'NaN',
	1 : 'Branca',
	2 : 'Preta',
	3 : 'Parda',
	4 : 'Amarela',
	5 : 'Indígena',
}


COLUMNS = {
	# Características do hospital	
	'PROC_REA'	: 'parto', # Procedimento realizado,
	'ano_internacao'	: 'ano', # Ano de internação,
	'CNES'	: 'cod_hosp', # Código CNES do hospital,
	# Características da gestantante
	'IDADE'	: 'idade', # Idade,
	'INSTRU'	: 'grau', # Grau de instrução do paciente,
	'RACA_COR'	: 'etnia', # Raça/cor do paciente,
	# Características do município de residencia
	'res_REGIAO'	: 'res_regiao', # Região de residência do paciente,
	'res_SIGLA_UF'	: 'res_uf', # Sigla da unidade da federação de residência do paciente,
	'int_codigo_adotado'	: 'res_cod_municipio', # Armazena o código atribuído ao município do estabelecimento de internação,
	'res_MUNNOMEX'	: 'res_municipio', # Nome (sem acentos, em maiúsculas) do Município de residência do paciente,
	'res_MSAUDCOD'	: 'res_macro_regiao_saude', # Código da Macrorregional de Saúde a que o Município de residência do paciente pertence,
	'res_RSAUDCOD'	: 'res_regiao_saude', # Código da Regional de Saúde a que o Município de residência do paciente pertence,
	'res_CSAUDCOD'	: 'res_micro_regiao_saude', # Código da Microrregional de Saúde a que o Município de residência do paciente pertence,
	'res_LATITUDE'	: 'res_latitude', # Latitude da sede do Município de residência do paciente,
	'res_LONGITUDE'	: 'res_longitude', # Longitude da sede do Município de residência do paciente,
	# Características do município de internação
	'int_REGIAO'	: 'int_regiao', # Região do estabelecimento de internação,
	'int_SIGLA_UF'	: 'int_uf', # Sigla da unidade da federação do estabelecimento de internação,
	'res_codigo_adotado'	: 'int_cod_municipio', # Armazena o código atribuído ao município de residência do paciente,
	'int_MUNNOMEX'	: 'int_municipio', # Nome (sem acentos, em maiúsculas) do Município do estabelecimento de internação,
	'int_MSAUDCOD'	: 'int_macro_regiao_saude', # Código da Macrorregional de Saúde a que o Município do estabelecimento de internação que foi à óbito pertence,
	'int_RSAUDCOD'	: 'int_regiao_saude', # Código da Regional de Saúde a que o Município do estabelecimento de internação,
	'int_CSAUDCOD'	: 'int_micro_regiao_saude', # Código da Microrregional de Saúde a que o Município do estabelecimento de internação,
	'int_LATITUDE'	: 'int_latitude', # Latitude da sede do Município do estabelecimento de internação,
	'int_LONGITUDE'	: 'int_longitude', # Longitude da sede do Município do estabelecimento de internação,
}


UF_REGIAO = {
  'BR': 'BR',
  'RO': 'NT',
	'AC': 'NT',
	'AM': 'NT',
	'RR': 'NT',
	'PA': 'NT',
	'AP': 'NT',
	'TO': 'NT',
 	'MA': 'ND',
	'PI': 'ND',
	'CE': 'ND',
	'RN': 'ND',
	'PB': 'ND',
	'PE': 'ND',
	'AL': 'ND',
	'SE': 'ND',
	'BA': 'ND',
	'MG': 'SD',
	'ES': 'SD',
	'RJ': 'SD',
	'SP': 'SD',
	'PR': 'SL',
	'SC': 'SL',
	'RS': 'SL',
	'MS': 'CO',
	'MT': 'CO',
	'GO': 'CO',
	'DF': 'CO',
}


REGIAO_COR = { # https://matplotlib.org/stable/gallery/color/named_colors.html
	'BR': 'k',
	'NT': 'g',
	'ND': 'r',
	'SD': 'm',
	'SL': 'c',
	'CO': 'y',
}


def main():
	print(PARTO)


__name__ == '__main__' and main()

