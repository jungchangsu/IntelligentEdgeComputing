# calculated mean squared error (평균 제곱 오차)
# root mean squared error
from sklearn.metrics import mean_squared_error
from math import sqrt
expected =    [0.0, 0.5, 0.0, 0.5, 0.0]
predictions = [0.2, 0.4, 0.1, 0.6, 0.2]
mse = mean_squared_error(expected, predictions)
print('MSE: %f'% mse)
rmse = sqrt(mse)
print('RMSE: %f' % rmse)

