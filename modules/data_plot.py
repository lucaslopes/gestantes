

from cProfile import label
import config
import data_info
import pandas as pd
import numpy as np
import seaborn as sns


from matplotlib import rcParams, pyplot as plt


rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Verdana']


custom_params = {
  "axes.spines.right": False,
  "axes.spines.top": False,
  "axes.spines.left": False, 
  "axes.spines.bottom": False,
}
sns.set_theme(
  style="dark", # darkgrid, whitegrid, dark, white, ticks
  palette="muted", # deep, muted, bright, pastel, dark, colorblind)
  color_codes=True,
  rc=custom_params,
)


def linreg_plot(x, y):
  sns.regplot(
    x=x, y=y,
    order=1, ci=None,
    scatter_kws={"s": 80})


def plot_scatter(df, ax):
  ax.axvline(x=0, ls='--', c='k', alpha=.5)
  ax.axhline(y=.5, ls='--', c='k', alpha=.5)
  p = sns.scatterplot(
		x='angle', y='intercept',
		data=df, hue='regiao',
  	palette=config.REGIAO_COR,
		s=600, alpha=.6,
		ax=ax
	)
  for i in range(df.shape[0]):
    ax.text(
      x=df.angle[i]-.045,y=df.intercept[i]-.015,s=df.uf[i], 
			fontdict=dict(color='w',size=8.5),
   )
  p.set(
    xlim=(-1, 1),
    ylim=(-.1, 1.1),
  )
  p.legend(
    fontsize=14,
    loc='lower left')
  # ax.yaxis.set_label_position("right")
  ax.yaxis.tick_right()
  return p


def plot_lin(x, y, reg, ax):
  p = sns.lineplot(
		x=x, y=y, ax=ax,
		color=config.REGIAO_COR[reg],
		linewidth=10, alpha=.45,
	)
  p.set(
    xlim=(0, 1),
    ylim=(-.1, 1.1),
  )
  return p


def plot_linreg(dfs): # uf, regiao, angle, intercept
  f, axes = plt.subplots(
    3, 2, figsize=[14,14],
    gridspec_kw={'width_ratios': [2, 1]}
	)
  for i, df in enumerate(dfs):
    plot_scatter(df, axes[i][1])
    axes[i][0].set_xlabel('time')
    for _, row in df.iterrows():
      x = np.linspace(0, 1, len(df))
      y = x * row['angle'] + row['intercept']
      plot_lin(x, y, row['regiao'], axes[i][0])
  axes[0][0].set_ylabel('ambos')
  axes[1][0].set_ylabel('normal')
  axes[2][0].set_ylabel('cesaria')
  f.tight_layout()


def plot_scatter_matrix(data): # uf, regiao, angle, intercept
  f, axes = plt.subplots(
    3, 3, figsize=[14,14],
	)
  for row, (r_label, dfs) in (
    enumerate(data.items())):
    axes[row][0].set_ylabel(r_label)
    for col, (c_label, df) in (
      enumerate(dfs.items())):
      plot_scatter(df, axes[row][col])
      axes[0][col].set_title(c_label)
      axes[0][col].set_xlabel('angle')
  f.tight_layout()

