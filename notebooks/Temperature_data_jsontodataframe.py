import pandas as pd
import json
import os

# Cambiamos directorio si hace falta
# os.chdir("/home/leandro/Documents/Maestria/SeriesdeTiempo/time-series-tp/notebooks")

pathtemp_json = '../datasets/POWER_Point_Daily_20050101_20220831_034d8115S_058d2813W_LST.json'

f = open(pathtemp_json)
temp_json = json.load(f)
df_temp = pd.DataFrame(list(zip(list(tj.keys()), list(tj.values()))), columns =['Fecha', 'T_mean'])
df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], format='%Y%m%d')
df_temp = df_temp.sort_values('Fecha')

df_temp.to_csv('../datasets/Temperatura.csv')