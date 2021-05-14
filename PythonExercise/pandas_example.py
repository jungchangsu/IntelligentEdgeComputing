'''
    Pandas 연습
'''
#import pandas as pd

'''
dict_data = {'a':1, 'b':2, 'c':3}
series_data = pd.Series(dict_data)
print(type(series_data))
print(series_data)

tup_data = ('용근', '1995-02-08', '남', True)
series_data = pd.Series(tup_data, index=['이름', '생년월일', '성별', '학생여부'])
print(series_data)
'''
import pandas as pd

df = pd.DataFrame({'c0':[0,1,2], 'c1':[1,2,3], 'c2':[4,5,6], 'c3':[7,8,9]})
print(df)
df.to_csv('test.csv', index=False)