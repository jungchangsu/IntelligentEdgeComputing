import matplotlib.pyplot as plt
import pandas as pd

"""
데이터 구조 
datetime,pm2.5,pm10,temperature,humidity
2020-12-11 09:43:03,31,35,21.4,29.5
2020-12-11 09:43:09,31,37,21.4,29.5
2020-12-11 09:43:14,29,34,21.4,29.5
"""

def zero_row_check(dataframe, col):
    """
        DataFrame에서 0인 행 검색
    :param dataframe:
    :param col:
    :return:
    """
    zero_index = dataframe[dataframe[col] == 0].index
    print("Column: {0}, zero rows: {1} ".format(col, len(zero_index)))

#df = pd.read_csv('2020-12-11.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
df = pd.read_csv('../data/2020-12-11.csv', sep=',')
print("Head")
print(df.head())

# 센서의 값이 0인 행을 제거함

print('-----------------------------------------------------')
#print(df.shape)    # 데이터의 크기 출력
#print(df.dtypes)    # 각 컬럼의 데이터 타입 출력

'''
    object형태이 'datetime' 컬럼을 datatime형으로 변환
    'datetime' 컬럼을 'date'와 'time'으로 분리함 
    t_datetime()함수 호출: DatetimeIndex 형태로 변환됨 
'''
df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H:%M:%S")
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time
df['hour'] = df['datetime'].dt.hour
print(df.dtypes)
#print(df.head())

# 센서 데이터 별 DataFrame을 생성함
pm25_df = df[['datetime', 'hour', 'pm2.5']]
pm25_df = pm25_df[pm25_df['pm2.5'] != 0]   # PM2.5의 값이 0인 행을 삭제함
print("pm25_df data types")
print(pm25_df.dtypes)

'''
pm10_df = df[['date', 'hour', 'pm10']]
pm10_df = pm10_df[pm10_df['pm10'] != 0]
zero_row_check(pm10_df, 'pm10')

temperature_df = df[['date', 'hour', 'temperature']]
temperature_df = temperature_df[temperature_df['temperature'] != 0]

humidity_df = df[['date', 'hour', 'humidity']]
humidity_df = humidity_df[humidity_df['humidity'] != 0]
zero_row_check(humidity_df, 'humidity')
'''

'''
    Dictionary 생성: key=hour, value=측정데이터 
    {(1':평균값), (2: 평균값), ... (24: 평균값)} 
'''
pm25_df = pm25_df.groupby(pd.Grouper(key='datetime', freq='H')).mean().astype(int)
print(pm25_df)
# DataFrame을 list로 변환
pm25_time_list = pm25_df['hour'].values.tolist()
pm25_value_list = pm25_df['pm2.5'].values.tolist()

#plt.bar(pm25_time_list, pm25_value_list)
plt.plot(pm25_time_list, pm25_value_list, marker='o')
plt.show()

#result = pm25_df.groupby(pd.Grouper(freq='H'))['pm2.5']
#print(result)
#pm25groups = pm25_df.groupby(pd.Grouper(freq='H')).mean()





