import pandas as pd
import matplotlib.pyplot as plt

#rawdata = pd.read_csv('/Users/changsu/PycharmProjects/EdgeMachine/2019-09-16-185528_sensor.csv')
rawdata = pd.read_csv('../data/2019-09-16-185528_sensor.csv')

pm25_raw = rawdata['pm2.5']

print(len(pm25_raw))

pm25_ma = rawdata['pm2.5'].rolling(window=6).mean() # 이동 평균 (window=6): 30초 간격으로 평균을 계산
pm25 = pm25_ma.dropna() # NAN 데이터 삭제

# Exponentially Weighted Moving Average (지수가중이동평균)
# span: 지수가중이동평균을 구할 때 관측데이터의 수
# pandas에서는 smoothing coefficient를 자동으로 결정해줌
pm25_ewm = pm25_raw.ewm(span=6).mean() # 지수 이동 평균
pm25_ewm = pm25_ewm.dropna()


#rawdata.plot(label='Raw PM2.5') # 모든 자료 그래프로 그려짐

plt.figure(figsize=(18, 6))
pm25_raw.plot(label='Raw PM2.5', color='black')
pm25.plot(label='Moving Average PM2.5', color='blue')
pm25_ewm.plot(label="Exponential Average PM2.5", color='red')

plt.legend()
plt.show()