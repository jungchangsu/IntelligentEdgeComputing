from pandas import read_csv
from matplotlib import pyplot

series = read_csv('dataset.csv', header=None, index_col=0, parse_dates=True, squeeze=True)
pyplot.figure(1)
# subplot(nrows, ncols, index)
pyplot.subplot(211)
series.hist()

pyplot.subplot(212)
series.plot(kind='kde') # KDE (Kernal Density Estimate)
pyplot.savefig("density.png")