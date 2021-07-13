 # Create lagged dataset
import pandas as pd
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
from math import sqrt

# step 1: Define
series = pd.read_csv('shampoo-sales.csv', header=0, index_col=0 )
values = pd.DataFrame(series.values)
dataframe = pd.concat([values.shift(1), values], axis=1) # axis=1: 열 방향
dataframe.columns = ['t', 't+1']
print(dataframe.head(5))

# step 2: DataFrame을 Train set과 Test set으로 분리 (0.66)
X = dataframe.values
#print(X)
train_size = int(len(X) * 0.66)
train, test = X[1:train_size], X[train_size:]
train_X, train_Y = train[:, 0], train[:, 1] # 모든 행의 0번째 열, 1번째 열
test_X, test_Y = test[:, 0], test[:, 1]


