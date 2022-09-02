import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import math

plt.rcParams.update({'font.size': 22})
path_consumo = '../datasets/consumo_electrico.csv'

datos_ce = pd.read_csv(path_consumo)

# Intervalo de tiempo estudiado
cfecha = datetime(2006,1,1)
ffecha = datetime(2022,1,1)
all_dates = pd.date_range(cfecha,ffecha-timedelta(days=1),freq='d').values

# Columnas de interés
cols_interes = ['Consumo', 'Cargo fijo', 'Cargo variable', 'Precio servicio electrico', 'Dias',
                'Contri municipal %', 'IVA %', 'Imp Sta Cruz %', 'Coef', 'Contribucion', 'subsidio', 'Total']

# Trabajo con mi consumo eléctrico
datos_ce['Año'] = datos_ce['Año'].astype('Int64')
datos_ce['Mes'] = datos_ce['Mes'].astype('Int64')
datos_ce['Dia'] = [1]*datos_ce.shape[0]
datos_ce = datos_ce.dropna(how='all')
datos_ce['fecha'] = pd.to_datetime((datos_ce.Año*10000+datos_ce.Mes*100+datos_ce.Dia).apply(str), format='%Y%m%d')
fechas_ce = datos_ce.fecha.values
fechas_todas = pd.date_range(cfecha, ffecha-timedelta(days=1), freq='d').values
fechas_df = pd.DataFrame(list(set(all_dates) - set(fechas_ce)), columns=['fecha'])
df_consumo = pd.concat([datos_ce, fechas_df], ignore_index=True)
df_consumo = df_consumo.sort_values('fecha', ascending=False).reset_index(drop=True)

# Replico el valor de precio de temperatura del 1/12/2021 en el 31/12/2021
ind_0 = df_consumo[df_consumo.fecha==datetime(2021,12,1)].index[0]
ind_1 = df_consumo[df_consumo.fecha==datetime(2021,12,31)].index[0]
df_consumo.loc[ind_1, cols_interes] = df_consumo.loc[ind_0, cols_interes]

# Teniendo los datos de consumo ordenado por fecha descendente. Replico el dato anterior, siempre y cuando no haya un dato nuevo
for i in range(df_consumo.shape[0]):
    df_trato = df_consumo.loc[i, cols_interes].copy()
    if not(math.isnan(df_trato.Consumo)):
        df_sirve = df_trato
    else:
        df_consumo.loc[i, cols_interes] = df_sirve

plt.plot(df_consumo.fecha, df_consumo['Cargo variable']/df_consumo.Consumo)
plt.legend()
plt.ylabel('Precio')
plt.xlabel('Fecha [Año]')
plt.show()

# Guardo los datos
df_consumo.to_csv('../datasets/Consumo_hogar_diario.csv')