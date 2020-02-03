import pandas as pd
import numpy as np

df  = pd.read_csv('test.csv')
df=df.fillna(0)
print(df)

res =df[df['时间间隔'].isin(['14:00 - 14:30'])]

res.to_csv('res2.csv')
#
# result=[]
# i=3
# while i<3217:
#     result.append(df.loc[item].values[1])
#     i=i+12