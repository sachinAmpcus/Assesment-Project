import pandas as pd
import numpy as np

d = {'Date': ['01-Sept','02-Sept','03-Sept','04-Sept','05-Sept',
            '06-Sept','07-Sept','08-Sept','09-Sept','10-Sept'], 
    'Temperature': [18,17,14,16,15,14,16,19,13,14],
    'WindSpeed': [9,12,np.nan,6,10,13,18,5],
    'Rainfall': [1,3,0,4,5,7,6]}

df = pd.DataFrame(data=d)

# TO DO
df['Rainfall'].ffill(axis=0, inplace=True)

print(df.head(10))