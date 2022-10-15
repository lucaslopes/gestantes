

import os
from pathlib import Path


URL_API = 'https://bigdata-api.fiocruz.br'


PATH_DATABASES = os.path.join(*[
	str(Path.home()),
	'Databases',
])

PATH_DATABASE = os.path.join(*[
	PATH_DATABASES,
	'SINASC',
])


PATH_DB = os.path.join(*[
  PATH_DATABASE,
  'sinasc.db',
])


PATH_DATABASE_ZIP = os.path.join(*[
  PATH_DATABASE,
  'SINASC.zip',
])


PATH_DATA = 'data/'
PATH_QUERIES = 'queries/'


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
	'ano_nasc' : 'ano', # Ano do nascimento
	'def_parto' : 'tipo_parto', # Tipo de parto (Nominal, com as seguintes classificações: Vaginal; Cesáreo; Ignorado)
	'CODESTAB' : 'cnes_hosp', # Código de estabelecimento https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search=
	# Características da gestantante:
	'IDADEMAE'	: 'idade', # Idade da mãe em anos
	'RACACORMAE' : 'raca_cor', # Raça/cor da mãe
	'def_est_civil' : 'estado_civil', # Estado civil (Situação conjugal: Solteiro; Casado; Viúvo; Separado judicialmente/divorciado; União estável; Ignorado)
	'def_escol_mae' : 'escolaridade', # (Nenhuma; de 1 a 3 anos; de 4 a 7 anos; 8 a 11 anos; 12 anos e mais; Ignorado)
	'ESCMAE2010' : 'escolaridade_2010', # Escolaridade 2010. Valores: 0 – Sem escolaridade; 1 –Fundamental I (1a a 4a série); 2 – Fundamental II (5a a 8a série); 3 – Médio (antigo 2o Grau); 4 – Superior incompleto; 5 –Superior completo; 9 – Ignorado.
	'ESCMAEAGR1' : 'escolaridade_agg', # Escolaridade 2010 agregada. Valores: 00 – Sem Escolaridade; 01 – Fundamental I Incompleto; 02 – Fundamental I Completo; 03 – Fundamental II Incompleto; 04 – Fundamental II Completo; 05 – Ensino Médio Incompleto; 06 – Ensino Médio Completo; 07 – Superior Incompleto; 08 – Superior Completo; 09 – Ignorado; 10 – Fundamental I Incompleto ou Inespecífico; 11 – Fundamental II Incompleto ou Inespecífico; 12 – EnsinoMédio Incompleto ou Inespecífico.
	'SERIESCMAE' : 'serie_escolar', # Série escolar da mãe. Valores de 1 a 8.
	'CODOCUPMAE' : 'ocupacao', # Ocupação, conforme a Classificação Brasileira de Ocupações (CBO-2002)
	# Características do município de residencia:
	'CODMUNRES'	: 'res_cod_municipio', # Município de residência da mãe, em codificação idêntica a deCODMUNNASC, conforme tabela TABMUN
	# Características do município de nascimento:
	'CODMUNNASC'	: 'nasc_cod_municipio', # 	Município de ocorrência, em codificação idêntica a de CODMUNRES, conforme tabela TABMUN
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

