

import config
import data_info
import pandas as pd
import numpy as np
import seaborn as sns


from matplotlib import pyplot as plt


sns.set_theme(color_codes=True)


def linreg_plot(x, y):
  sns.regplot(
    x=x, y=y,
    order=1, ci=None,
    scatter_kws={"s": 80})


def plot_scatter(df, ax):
  p = sns.scatterplot(
		x='angle', y='intercept',
		data=df, hue='regiao',
  	palette=config.REGIAO_COR,
		s=200, alpha=.5,
		ax=ax
	)
  p.set(
    xlim=(-.8, .8),
    ylim=(-.1, 1.1),
  )
  p.legend(loc='lower left')
  return p


# uf	regiao	angle	intercept
def plot_linreg(dfs):
  f, axes = plt.subplots(
    3, 2, figsize=[14,14],
    gridspec_kw={'width_ratios': [2, 1]}
	)
  for i, df in enumerate(dfs):
    plot_scatter(df, axes[i][1])
    for _, row in df.iterrows():
      x = np.linspace(0, 1, len(df))
      y = x * row['angle'] + row['intercept']
      sns.lineplot(
				x=x, y=y, ax=axes[i][0],
				color=config.REGIAO_COR[row['regiao']],
			)
  # sns.set(font_scale=5)
  f.tight_layout()


def generate_plots(fnames):
	d = dict()
	for fname in fnames:
		label = fname.split('_')[-2]
		df = pd.read_csv(
			f'data/xz/{fname}.csv.xz',
			index_col=0)
		d[label] = (
			data_info.get_params_per_uf(df))
	return d