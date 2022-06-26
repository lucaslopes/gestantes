

import seaborn as sns
from matplotlib import pyplot as plt


def heatmap(
		df
	):
	
	f, axe = plt.subplots(1, 1, figsize=(15, 7))
	axe.set_title('Número de meses por Ano x UF')

	return sns.heatmap(
		data = df,
		cmap = 'Greens',
		linewidths = .5,
		linecolor = 'black',
		vmin = 0,
		square = True,
		annot = True,
		ax = axe,   
	)


def pie_chart(df):

	return plt.pie(
		x = df['Coluna'],
		labels = df['Tipo'],
	)