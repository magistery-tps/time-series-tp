import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import math
import os
from prophet import Prophet
from prophet.diagnostics import cross_validation
import itertools
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from prophet.diagnostics import performance_metrics


os.chdir('/home/leandro/Documents/Maestria/SeriesdeTiempo/time-series-tp/notebooks')

# Read all datasets of regresors
path_consumo = '../datasets/Consumo_hogar_diario.csv'
path_inflacion = '../datasets/inflacion_diaria.csv'
path_temperatura = '../datasets/Temperatura_lon_-58.2813_lat_-34.8115.csv'

df_consumo = pd.read_csv(path_consumo)
df_inflacion = pd.read_csv(path_inflacion)[['fecha', 'inflacion_diaria', 'Fuente', 'inflacion_acumulada']]
df_temperatura = pd.read_csv(path_temperatura)[['fecha', 'T_mean', 'T_max', 'T_min', 'longitud', 'latitud']]

# Multiplicative value for tickets value
df_consumo['por'] = 1
df_consumo.loc[df_consumo.periodo=='mensual', 'por'] = 2
df_consumo['precio_kWh'] = df_consumo['Total']*df_consumo['por']/df_consumo['Consumo']

# Change column type
df_consumo['fecha'] = df_consumo['fecha'].astype('datetime64[ns]')
df_inflacion['fecha'] = df_inflacion['fecha'].astype('datetime64[ns]')
df_temperatura['fecha'] = df_temperatura['fecha'].astype('datetime64[ns]')

df_regresors = pd.merge(df_consumo, df_inflacion, on=["fecha"])
df_regresors = pd.merge(df_regresors, df_temperatura, on=["fecha"])

df_regresors = df_regresors[['fecha', 'Consumo', 'Cargo fijo', 'Cargo variable',
       'Dias', 'subsidio', 'Total', 'Tipo',
       'Precio kWh', 'Dia',
       'precio_kWh', 'inflacion_acumulada', 'T_mean', 'T_max',
       'T_min', 'longitud', 'latitud']]

df_regresors['precio_kWh_norm'] = list(df_regresors.precio_kWh/df_regresors.inflacion_acumulada)
df_regresors = df_regresors.sort_values('fecha')

# vec_der = (df_regresors.precio_kWh_norm - df_regresors['precio_kWh_norm'].shift(-1))[::-1]
vec_der = (df_regresors.precio_kWh_norm.shift(+1) - df_regresors.precio_kWh_norm).values

value_vec = [1]
for i, value in enumerate(vec_der[1:]):
       if abs(value)>0.051:
              value_vec.append(-value_vec[i])
       else:
              value_vec.append(value_vec[i])

df_regresors['use'] = value_vec
df_regresors['precio_kWh_norm_nan'] = [np.NAN if value_vec[i]==-1 else df_regresors.precio_kWh_norm.values[i] for i in range(df_regresors.shape[0])]

df_regresor_new = df_regresors[['fecha', 'precio_kWh_norm_nan']].fillna(method="ffill")

df_regresors = pd.merge(df_regresors, df_regresor_new.rename(columns={'precio_kWh_norm_nan': 'precio_kWh_norm_new'}), on=["fecha"])

df_regresors.to_csv(f"../datasets/regresores_v1.csv")

df_regresors = pd.read_csv(f"../datasets/regresores_v1.csv")

plt.plot(df_regresors.fecha, df_regresors.precio_kWh_norm_nan, label = 'new')
plt.plot(df_regresors.fecha, df_regresors.precio_kWh_norm_new, label = 'new interpolate')
# plt.plot(df_regresors.fecha, df_regresors.use*.1, label = 'use')
# plt.plot(df_regresors.fecha, vec_der, label = 'derivada')
plt.plot(df_regresors.fecha, df_regresors.precio_kWh_norm, label = 'precio')
plt.axhline(y=0.05)
plt.axhline(y=-0.05)
plt.legend()
plt.ylabel('precio kWh normalizada')
plt.xlabel('Fecha [Año]')
plt.show()


path_demanda = '/home/leandro/Documents/Maestria/SeriesdeTiempo/data3_dia.csv'
df_dhistorica = pd.read_csv(path_demanda)
df_dhistorica = df_dhistorica.rename(columns={'dia': 'fecha'})
df_dhistorica['fecha'] = df_dhistorica['fecha'].astype('datetime64[ns]')

plt.plot(df_dhistorica.fecha, df_dhistorica.MWh)
df_dhistorica.dtypes

df_final = pd.merge(df_regresors, df_dhistorica, on=["fecha"])

plt.plot(df_final.fecha, df_final.precio_kWh_norm_new/df_final.precio_kWh_norm_new.max(), label = 'precio')
plt.plot(df_final.fecha, df_final.MWh/df_final.MWh.max(), label = 'consumo')
plt.show()

df_test = df_final[['fecha', 'MWh', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']]
df_test = df_test.rename(columns={"fecha": "ds", "MWh": "y"}, errors="raise")
df_test = df_test.sort_values('ds')

m = Prophet()
m.add_country_holidays(country_name='ARG')
m.add_seasonality(name='weekly', period=7, fourier_order=3)
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
m.add_seasonality(name='yearly', period=365.25, fourier_order=10)
m.add_regressor('precio_kWh_norm_new')
m.add_regressor('T_mean')
m.add_regressor('T_min')
m.add_regressor('T_max')
m.fit(df_test)

df_cv = cross_validation(m, initial='730 days', period='365 days', horizon = '365 days')


fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=df_cv.ds, y=df_cv.y, name='y'))
fig.add_trace(go.Scatter(x=df_cv.ds, y=df_cv.yhat))
fig.show()

param_grid = {
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
    'holidays_prior_scale': [0.01, 0.1, 1.0, 10.0],
    'seasonality_mode': ['additive', 'multiplicative']
}

# Generate all combinations of parameters
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
rmses = []  # Store the RMSEs for each params here

# Use cross validation to evaluate all parameters
for params in all_params:
    print(params)
    m = Prophet(**params)
    m.add_country_holidays(country_name='ARG')
    m.add_seasonality(name='weekly', period=7, fourier_order=3)
    m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    m.add_seasonality(name='yearly', period=365.25, fourier_order=10)
    m.add_regressor('precio_kWh_norm_new')
    m.add_regressor('T_mean')
    m.add_regressor('T_min')
    m.add_regressor('T_max')
    m.fit(df_test)  # Fit model with given params
    df_cv = cross_validation(m, initial='730 days', period='365 days', horizon = '365 days')
    if(params==all_params[0]):
        print('jfnre')
        df__ = df_cv
        df__['params'] = [params] * df_cv.shape[0]
    else:
        print('afbeif0')
        df_cv['params'] = [params] * df_cv.shape[0]
        df__ = pd.concat([df__, df_cv], ignore_index=True)
    # df_p = performance_metrics(df_cv, rolling_window=1)
    # rmses.append(df_p['rmse'].values[0])

# df__.to_csv(f"../datasets/df_cross_validation.csv")
df__ = pd.read_csv(f"../datasets/df_cross_validation.csv")
df__['ds'] = pd.to_datetime(df__.ds)
df__['cutoff'] = pd.to_datetime(df__.cutoff)

for params in all_params:
    df_este = df__[df__.params==str(params)].copy()
    df_p = performance_metrics(df_este[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'y', 'cutoff']], rolling_window=1)
    rmses.append(df_p['rmse'].values[0])

min_index = np.argmin(rmses)
max_index = np.argmax(rmses)
best_param = all_params[min_index]
df_min = df__[df__.params==all_params[min_index]]

fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=df_min.ds, y=df_cv.y/df_cv.y.max(), name='y'))
# fig.add_trace(go.Scatter(x=df_min.ds, y=df_min.yhat/df_min.yhat.max(), name='yhat'))
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.precio_kWh_norm_new/df_test.precio_kWh_norm_new.max(), name='precio'))
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.T_mean/df_test.T_mean.max(), name='T_mean'))
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.T_min/df_test.T_min.max(), name='T_min'))
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.T_max/df_test.T_max.max(), name='T_max'))
fig.show()


# Una sola predicción

df_train = df_test[df_test.ds<datetime(2020,12,31)]
df_test = df_test[df_test.ds>=datetime(2020,12,31)]

m = Prophet(**params)
m.add_country_holidays(country_name='ARG')
m.add_seasonality(name='weekly', period=7, fourier_order=3)
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
m.add_seasonality(name='yearly', period=365.25, fourier_order=10)
m.add_regressor('precio_kWh_norm_new')
m.add_regressor('T_mean')
m.add_regressor('T_min')
m.add_regressor('T_max')
m.fit(df_train)

forecast = m.predict(df_test[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']])

fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.y, name='y'))
fig.add_trace(go.Scatter(x=forecast.ds, y=forecast.yhat, name='yhat'))
fig.show()


fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.y/df_test.y.max(), name='y'))
fig.add_trace(go.Scatter(x=df_test.ds, y=(df_test.T_min - df_test.T_min.mean())/(df_test.T_min - df_test.T_min.mean()).min(), name='T max'))
# fig.add_trace(go.Scatter(x=forecast.ds, y=forecast.yhat/forecast.yhat.max(), name='yhat'))
fig.show()

df_test_expensive4 = df_test[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']].copy()
df_test_expensive4['precio_kWh_norm_new'] = 4 * df_test_expensive4['precio_kWh_norm_new']
forecast4 = m.predict(df_test_expensive4[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']])

df_test_expensive10 = df_test[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']].copy()
df_test_expensive10['precio_kWh_norm_new'] = 10 * df_test_expensive4['precio_kWh_norm_new']
forecast10 = m.predict(df_test_expensive10[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']])

forecast_por = {}
for i in [2, 4, 6, 8]:
    df_this = df_test[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']].copy()
    df_this['precio_kWh_norm_new'] = i * df_this['precio_kWh_norm_new']
    forecast_por[i] = m.predict(df_this[['ds', 'precio_kWh_norm_new', 'T_mean', 'T_min', 'T_max']])

fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=df_test.ds, y=df_test.y, name='y'))
fig.add_trace(go.Scatter(x=forecast.ds, y=forecast.yhat, name='yhat'))
for i in [2, 4, 6, 8]:
    fig.add_trace(go.Scatter(x=forecast_por[i].ds, y=forecast_por[i].yhat, name='yhat_' + str(i)))
fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="MWh",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig.show()


squares=list(map(lambda x:pow(x,2), [df_test.y.values-forecast.yhat.values]))