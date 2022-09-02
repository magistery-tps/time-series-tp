import pandas as pd
import json
import os

# Cambiamos directorio si hace falta
# os.chdir("/home/leandro/Documents/Maestria/SeriesdeTiempo/time-series-tp/notebooks")

pathtemp_json = '../datasets/POWER_Point_Daily_20050101_20220831_034d8115S_058d2813W_LST.json'

f = open(pathtemp_json)
temp_json = json.load(f)
tm = temp_json['properties']['parameter']['T2M']
tmax = temp_json['properties']['parameter']['T2M_MAX']
tmin = temp_json['properties']['parameter']['T2M_MIN']
df_temp = pd.DataFrame(list(zip(list(tm.keys()), list(tm.values()), list(tmax.values()), list(tmin.values()))),
                       columns =['Fecha', 'T_mean', 'T_max', 'T_min'])
df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], format='%Y%m%d')
df_temp['longitud'] =  temp_json['geometry']['coordinates'][0]
df_temp['latitud'] = temp_json['geometry']['coordinates'][1]
df_temp = df_temp.sort_values('Fecha')

df_temp.to_csv(f"../datasets/Temperatura_lon_{str(temp_json['geometry']['coordinates'][0])}_lat_{str(temp_json['geometry']['coordinates'][1])}.csv")