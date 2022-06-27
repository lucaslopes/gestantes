

import seaborn as sns
from matplotlib import pyplot as plt


def heatmap(
		df,
		value = 'meses',
		annot = False,
		cmap = 'Greens',
	):
	
	f, axe = plt.subplots(1, 1, figsize=(15, 7))
	axe.set_title(f'Número de {value} por Ano x UF')

	return sns.heatmap(
		data = df,
		cmap = cmap,
		linewidths = .5,
		linecolor = 'black',
		vmin = 0,
		square = True,
		annot = annot,
		ax = axe,   
	)


def pie_chart(df):

	return plt.pie(
		x = df['Coluna'],
		labels = df['Tipo'],
	)