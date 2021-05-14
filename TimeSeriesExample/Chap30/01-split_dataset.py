"""
    01-split_dataset.py
    원본 데이터를 dataset과 validation set으로 분리함

    - dataset.csv: from Jan. 1966 to Oct. 1974 (106개)
    - validation.csv: from Nov. 1974 to Oct. 1975 (12개)
    . 원본 데이터에서 마지막 12개의 데이터를 검증 용도로 사용하기 위해 데이터를 분리함
"""
from pandas import read_csv
'''
    read_csv()
    - header=0 : 1행이 컬럼 이름을 포함하고 있는 경우
    - index_col=0 : 인덱스로 사용할 컬럼을 지정 (0 -> 'Month')
    - parse_dates=True: 인덱스로 지정된 컬럼의 데이터를 날짜로 파싱함
      parse_dates=[index]
    - squeeze=True: DataFrame을 단일 컬럼의 Series로 변환
'''
series = read_csv('robberies.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
split_point = len(series)-12
dataset, validation = series[0:split_point], series[split_point:]
print('Dataset %d, Validation: %d' % (len(dataset), len(validation)))
# csv파일로 저장을 할때 헤더 정보를 저장하지 않음 (header=False, header 디폴트 값은 True)
dataset.to_csv('dataset.csv', header=False)
validation.to_csv('validation.csv', header=False)
