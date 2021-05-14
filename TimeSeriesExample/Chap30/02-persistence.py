from pandas import read_csv
from sklearn.metrics import mean_squared_error
from math import sqrt
# header=0, 첫 번째 row에 헤더 정보가 있으므로 건너뜀
# header=None
series = read_csv('dataset.csv', header=None, index_col=0, parse_dates=True, squeeze=True)

X = series.values
X = X.astype('float32')
print(len(X))
train_size = int(len(X) * 0.50)
# dataset.csv의 데이터를 50%: train, 50%: test 용도로 나눔
train, test = X[0:train_size], X[train_size:]

# walk-forward validation
history = [x for x in train]
predictions = list()
for i in range(len(test)):
    # predict
    yhat = history[-1]
    predictions.append(yhat)

    #observation
    obs = test[i]
    history.append(obs)
    print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
# report performance
rmse = sqrt(mean_squared_error(test, predictions))
print('RMSE: %.3f' % rmse)