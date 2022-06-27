

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

def line_chart(
		df,
		x = 'Ano',
		y = 'n_cols',
		hue = None,
	):

	f, axe = plt.subplots(1, 1, figsize=(15, 7))
	# axe.set_title(f'Número de {value} por Ano x UF')

	return sns.lineplot(
		data = df,
		x = 'Ano',
		y = 'n_cols',
		ax = axe,
		hue=hue,
	)


def rel_plot(df,
		x='Ano', y='Linhas', hue='Parto',
	):

	f, axe = plt.subplots(1, 1, figsize=(15, 7))

	return sns.lineplot(
		data=df,
		x=x, y=y, hue=hue,
		# kind='line',
		ax = axe,

	)


def bar_plot(df, order,
		x="UF", y="Linhas", hue="Parto",
	):
		
	f, axe = plt.subplots(1, 1, figsize=(15, 7))
	
	return sns.barplot(
		data=df,
		# palette="dark",
		x=x, y=y, hue=hue,
		ax=axe,
		orient='v',
		order=order,
	)