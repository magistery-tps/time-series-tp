import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



def leyends(figure, xlabel ='', ylabel='', title=''):
    figure.set_title(title)
    figure.set_xlabel(xlabel)
    figure.set_ylabel(ylabel)


def plot_col_hist(df, column, bins=10, title_prefix='', figsize=(20, 3), plot=True):
    sns.set(rc = {'figure.figsize':figsize})
    f = sns.histplot(data=df, x=column, bins=bins)
    leyends(f, title=f'{title_prefix}Histograma: {to_title(column)}')
    if plot:
        plt.show()

def to_title(value): return value.lower().replace("_", " ").capitalize()


def plot_ts(values, xlabel='', ylabel='', title='', figsize=(20, 3), plot=True):
    sns.set(rc = {'figure.figsize':figsize})
    times  = list(range(len(values)))
    f = sns.lineplot(x=times, y=values, marker="o")
    
    if title == '':
        title = xlabel
    leyends(f, xlabel, ylabel,  title=f'Serie de tiempo: {to_title(ylabel)}')
    if plot:
        plt.show()

    
def plot_col_ts(df, x_column, y_column, title_prefix='', figsize=(20, 3), plot=True):
    sns.set(rc = {'figure.figsize':figsize})
    f = sns.lineplot(data=df, x=x_column, y=y_column, marker="o")
    leyends(f, title=f'{title_prefix}Serie de tiempo: {to_title(y_column)}')
    if plot:
        plt.show()
    
def boxplot(values, title='', figsize=(20, 3), plot=True):
    sns.set(rc = {'figure.figsize':figsize})
    leyends(sns.boxplot(x=values), title = to_title(title))
    if plot:
        plt.show()

def plot_col_boxplot(df, column, title_prefix='', figsize=(20, 3)):
    boxplot(df[column].values, f'{title_prefix}Boxplot: {to_title(column)}')

def plot_ts_var(df, x_column, y_column, bins=5, title_prefix='', figsize=(20, 3)):
    sns.set(rc = {'figure.figsize':figsize})
    plot_col_ts(df, x_column, y_column, title_prefix=title_prefix)
    plot_col_boxplot(df, y_column, title_prefix=title_prefix)
    # plot_col_hist(df, y_column, bins=bins, title_prefix=title_prefix)