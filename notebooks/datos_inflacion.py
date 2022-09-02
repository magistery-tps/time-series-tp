import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import math
from calendar import monthrange

plt.rcParams.update({'font.size': 22})
path_consumo = '../datasets/inflacion.csv'

datos_inflacion = pd.read_csv(path_consumo)
datos_inflacion['Año'] = datos_inflacion['Año'].astype('Int64')
datos_inflacion['Mes'] = datos_inflacion['Mes'].astype('Int64')
datos_inflacion['Dia'] = [1]*datos_inflacion.shape[0]
datos_inflacion['fecha'] = pd.to_datetime((datos_inflacion.Año*10000+datos_inflacion.Mes*100+datos_inflacion.Dia).apply(str), format='%Y%m%d')
datos_inflacion['n_daymonth'] = datos_inflacion['fecha'].dt.days_in_month.astype(float)
datos_inflacion['inflacion_mas_1'] = (1 + 0.01*datos_inflacion.Inflacion).astype(float)
datos_inflacion = datos_inflacion.assign(inflacion_diaria=lambda x: x['inflacion_mas_1']**(1/x['n_daymonth']))

plt.plot(datos_inflacion.fecha, datos_inflacion.inflacion_diaria)
plt.legend()
plt.ylabel('Precio')
plt.xlabel('Fecha [Año]')
plt.show()

# Intervalo de tiempo estudiado
cfecha = datetime(2006,1,1)
ffecha = datetime(2022,1,1)

# Columnas de interés
cols_interes = ['Inflacion', 'Unnamed: 4','Fuente', 'inflacion_diaria']

# Trabajo con mi consumo eléctrico
fechas_inf = datos_ce.fecha.values
fechas_todas = pd.date_range(cfecha, ffecha-timedelta(days=1), freq='d').values
fechas_df = pd.DataFrame(list(set(fechas_todas) - set(fechas_inf)), columns=['fecha'])
datos_inflacion = pd.concat([datos_inflacion, fechas_df], ignore_index=True)
datos_inflacion = datos_inflacion.sort_values('fecha', ascending=True).reset_index(drop=True)

# Replico el valor de precio de temperatura del 1/12/2021 en el 31/12/2021

# Teniendo los datos de consumo ordenado por fecha descendente. Replico el dato anterior, siempre y cuando no haya un dato nuevo
for i in range(datos_inflacion.shape[0]):
    df_trato = datos_inflacion.loc[i, cols_interes].copy()
    if not(math.isnan(df_trato.inflacion_diaria)):
        df_sirve = df_trato
    else:
        datos_inflacion.loc[i, cols_interes] = df_sirve


plt.plot(datos_inflacion.fecha, datos_inflacion.inflacion_diaria)
plt.legend()
plt.ylabel('Precio')
plt.xlabel('Fecha [Año]')
plt.show()

# Guardo los datos
datos_inflacion.to_csv('../datasets/inflacion_diaria.csv')