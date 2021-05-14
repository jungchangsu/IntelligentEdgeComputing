'''
    ARIMA 모델을 이용한 시계열 분석
    - ARIMA (Autoregressive Integrated Moving Average)
    - 참고 사이트: https://byeongkijeong.github.io/ARIMA-with-Python/
    - 사용 데이터: 최근 60일간의 비트코인 시세 자료
        . 사이트: https://www.blockchain.com/ko/charts/market-price?timespan=60days
        . Blockchain Luxembourg S.A
        . Data format: csv 파일
        +----------------+----------+
        |       Date     |  Price   |
        +----------------+----------+
        |2021-03-12 0:00 |  57764   |
        +----------------+----------+
'''

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
# heaer=None: 컬럼 이름이 없는 경우, header=0: 첫번째 행이 컬럼 이름인 경우
series = pd.read_csv('../../data/market-price.csv', header=0, index_col=0, squeeze=True)
series.plot()
'''
plt.title("Blockchain Price")
plt.xlabel("Date")
plt.ylabel("Price")

plot_acf(series, lags=60)
plot_pacf(series, lags=20)
plt.show()
'''

"""
ARIMA 내용 
 - order(p, d, q): autoregressive, difference, moving average 순서
 - trend:
    . 'c'= constant term (Default value)
    . 't'= linear trend
    . "nc"= no constant (long run mean is zero, no intercept and no trend)
"""

model = ARIMA(series, order=(0, 1, 1))
model_fit = model.fit(trend='nc', full_output=True, disp=1)
print(model_fit.summary())
model_fit.plot_predict()
fore = model_fit.forecast(steps=2)
print(fore)
plt.show()