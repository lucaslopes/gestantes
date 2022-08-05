

import os
from pathlib import Path


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


COLUMNS = {
	# Características do hospital:
	'ano_internacao' : 'ano', # Ano de internação	
	'def_procedimento_realizado' : 'procedimento', # PARTO NORMAL / PARTO CESARIANO
	'CNES' : 'cod_hosp', # Código CNES do hospital
	# Características da gestantante:
	'IDADE'	: 'idade', # Idade
	'def_raca_cor' : 'raca_cor', #	Definição de raça/cor do paciente
	# Características do município de residencia:
	'res_REGIAO' : 'res_regiao', # Região de residência do paciente
	'res_SIGLA_UF' : 'res_uf', # Sigla da unidade da federação de residência do paciente
	'res_codigo_adotado'	: 'res_cod_municipio', # Armazena o código atribuído ao município do estabelecimento de internação
	'res_MUNNOMEX' : 'res_municipio', # Nome (sem acentos, em maiúsculas) do Município de residência do paciente
	'res_RSAUDCOD' : 'res_regiao_saude', # Código da Regional de Saúde a que o Município de residência do paciente pertence
	'res_LATITUDE' : 'res_latitude', # Latitude da sede do Município de residência do paciente
	'res_LONGITUDE'	: 'res_longitude', # Longitude da sede do Município de residência do paciente
	# Características do município de internação:
	'int_REGIAO'	: 'int_regiao', # Região do estabelecimento de internação
	'int_SIGLA_UF'	: 'int_uf', # Sigla da unidade da federação do estabelecimento de internação
	'int_codigo_adotado'	: 'int_cod_municipio', # Armazena o código atribuído ao município de residência do paciente
	'int_MUNNOMEX'	: 'int_municipio', # Nome (sem acentos, em maiúsculas) do Município do estabelecimento de internação
	'int_RSAUDCOD'	: 'int_regiao_saude', # Código da Regional de Saúde a que o Município do estabelecimento de internação
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

