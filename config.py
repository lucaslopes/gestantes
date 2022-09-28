

import os
from pathlib import Path


URL_API = 'https://bigdata-api.fiocruz.br'


PATH_SIHSUS = os.path.join(*[
	str(Path.home()),
	'Databases',
	'SIHSUS',
])


PATH_DB = os.path.join(*[
  PATH_SIHSUS,
  'partos.db',
])


PATH_SIHSUS_ZIP = '/Volumes/SanDisk/SIHSUS.zip'
PATH_DATA = 'data/'
PATH_QUERIES = 'queries/'


with open(
  	PATH_QUERIES + 'modify/delete.sql'
  ) as f:
	FILTER_QUERY = f.read()


YEAR_RANGE = [2010, 2020]  # Last not included


PERIODS = {
	2010 : 'antes', 2011 : 'antes',
 	2018 : 'depois', 2019 : 'depois',
	'outros' : 'durante',
}


PARTO = { # http://sigtap.datasus.gov.br/tabela-unificada/app/sec/inicio.jsp
	310010039 : 'NORMAL', # 03.10.01.003-9 - PARTO NORMAL
	411010034 : 'CESARIANO', # 04.11.01.003-4 - PARTO CESARIANO
}


COLUMNS = {
	# Características do hospital:
	'ano_internacao' : 'ano', # Ano de internação	
	# 'def_procedimento_realizado' : 'procedimento', # PARTO NORMAL / PARTO CESARIANO
	'PROC_REA' : 'parto', # Procedimento realizado	
	'CNES' : 'cnes', # Código do Cadastro Nacional de Estabelecimentos de Saúde
	# Características da gestantante:
	'IDADE'	: 'idade', # Idade
	'def_raca_cor' : 'raca_cor', #	Definição de raça/cor do paciente
	# Características do município de residencia:
	'res_codigo_adotado'	: 'res_cod_municipio', # Armazena o código atribuído ao município do estabelecimento de internação
	'res_MUNNOMEX' : 'res_municipio', # Nome (sem acentos, em maiúsculas) do Município de residência do paciente
	'res_RSAUDCOD' : 'res_regiao_saude', # Código da Regional de Saúde a que o Município de residência do paciente pertence
	'res_SIGLA_UF' : 'res_uf', # Sigla da unidade da federação de residência do paciente
	'res_REGIAO' : 'res_regiao', # Região de residência do paciente
	'res_LATITUDE' : 'res_latitude', # Latitude da sede do Município de residência do paciente
	'res_LONGITUDE'	: 'res_longitude', # Longitude da sede do Município de residência do paciente
	# Características do município de internação:
	'int_codigo_adotado'	: 'int_cod_municipio', # Armazena o código atribuído ao município de residência do paciente
	'int_MUNNOMEX'	: 'int_municipio', # Nome (sem acentos, em maiúsculas) do Município do estabelecimento de internação
	'int_RSAUDCOD'	: 'int_regiao_saude', # Código da Regional de Saúde a que o Município do estabelecimento de internação
	'int_SIGLA_UF'	: 'int_uf', # Sigla da unidade da federação do estabelecimento de internação
	'int_REGIAO'	: 'int_regiao', # Região do estabelecimento de internação
	'int_LATITUDE'	: 'int_latitude', # Latitude da sede do Município do estabelecimento de internação
	'int_LONGITUDE'	: 'int_longitude', # Longitude da sede do Município do estabelecimento de internação
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
	print(COLUMNS)


__name__ == '__main__' and main()

