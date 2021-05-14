# Boxplots of time series

from pandas import read_csv
from pandas import DataFrame
from pandas import Grouper
from matplotlib import pyplot

series = read_csv('dataset.csv', header=None, index_col=0, parse_dates=True, squeeze=True)
print(series)
'''
    freq
    'A': Year end frequency
    'H': hourly frequency    
'''
groups = series['1966':'1973'].groupby(Grouper(freq='A'))
print(groups)
years = DataFrame()
for name, group in groups:
    years[name.year] = group.values
years.boxplot()
#pyplot.show()
pyplot.savefig("boxplot.png")