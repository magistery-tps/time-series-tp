import seaborn as sns
import matplotlib.pyplot as plt


def leyends(figure, xlabel ='', ylabel='', title=''):
    figure.set_title(title)
    figure.set_xlabel(xlabel)
    figure.set_ylabel(ylabel)


def plot_hist(values, xlabel ='', ylabel='', title=''):
    leyends(sns.histplot(values), xlabel, ylabel, title)
    plt.show()

def plot_col_hist(df, column, xlabel):
    plot_hist(df[column].values, xlabel, column, f'Histogram - {column}')


def plot_ts(values, xlabel ='', ylabel='', title=''):
    times  = list(range(len(values)))
    leyends(sns.lineplot(x=times, y=values), xlabel, ylabel,  title)
    plt.show()

def plot_col_ts(df, column, xlabel):
    plot_ts(df[column].values, xlabel, column,  f'Time serie - {column}')

def boxplot(values, title=''):
    leyends(sns.boxplot(x=values), title = title)
    plt.show()

def plot_col_boxplot(df, column):
    boxplot(df[column].values, f'Boxplot - {column}')

def plot_ts_var(df, column, time_label = 'Días'):
    plot_col_ts(df, column, time_label)
    plot_col_boxplot(df, column)
    plot_col_hist(df, column, time_label)