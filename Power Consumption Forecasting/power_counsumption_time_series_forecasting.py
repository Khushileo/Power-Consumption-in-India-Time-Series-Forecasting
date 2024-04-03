# -*- coding: utf-8 -*-
"""Power_Counsumption_time_series_forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fP40odSR3IX9XwQiOX1cc2OfQICTeSRJ
"""

!pip install --upgrade nbformat

!pip install prophet

!pip install -qy pandas==1.3.4 numpy==1.21.4 seaborn==0.9.0 matplotlib==3.5.0 scikit-learn==0.20.1

import pandas as pd
from prophet import Prophet
from matplotlib import pyplot
from matplotlib.pyplot import figure
from sklearn.metrics import mean_absolute_error
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv('/content/long_data_.csv')

df.head()

df.shape

df['Dates'] = pd.to_datetime(df['Dates'])

df = df.groupby(df['Dates'], as_index = False).mean()
df.head()

df.shape

df = df[['Dates','Usage']]

fig = px.line(df, x='Dates', y='Usage')
fig.show()

df.columns = ['ds','y']

df.head()

model=Prophet()

model.fit(df)

model.component_modes

future_dates = model.make_future_dataframe(periods=365,freq='d',include_history=True)
future_dates.shape

future_dates.head()

prediction=model.predict(future_dates)

prediction.head()

trace_open = go.Scatter(
    x = prediction["ds"],
    y = prediction["yhat"],
    mode = 'lines',
    name="Forecast"
)
trace_high = go.Scatter(
    x = prediction["ds"],
    y = prediction["yhat_upper"],
    mode = 'lines',
    fill = "tonexty",
    line = {"color": "#57b8ff"},
    name="Higher uncertainty interval"
)
trace_low = go.Scatter(
    x = prediction["ds"],
    y = prediction["yhat_lower"],
    mode = 'lines',
    fill = "tonexty",
    line = {"color": "#57b8ff"},
    name="Lower uncertainty interval"
)
trace_close = go.Scatter(
    x = df["ds"],
    y = df["y"],
    name="Data values"
)

#make list for all three scattle objects.
data = [trace_open,trace_high,trace_low,trace_close]
# Construct a new Layout object.
#title - It will display string as a title of graph
layout = go.Layout(title="Power consumption forecasting")
#A list or tuple of trace instances (e.g. [Scatter(…), Bar(…)]) or A single trace instance (e.g. Scatter(…), Bar(…), etc.)
#A list or tuple of dicts of string/value properties where: - The ‘type’ property specifies the trace type.

fig = go.Figure(data=data)
fig.show()

fig = go.Figure([go.Scatter(x=df['ds'], y=df['y'],mode='lines',
                    name='Actual')])
#You can add traces using an Express plot by using add_trace
fig.add_trace(go.Scatter(x=prediction['ds'], y=prediction['yhat'],
                   mode='lines+markers',
                    name='predicted'))
#To display a figure using the renderers framework, you call the .show() method on a graph object figure, or pass the figure to the plotly.io.show function.
#With either approach, plotly.py will display the figure using the current default renderer(s).
fig.show()

#Return a Numpy representation of the DataFrame.
y_true = df['y'].values

#Here we have specified [:498] because in y_true we have 498 data points so for comparing both series we need equal shape of series.
y_pred = prediction['yhat'][:498].values

#Parameters:
#y_truearray-like of shape = (n_samples) or (n_samples, n_outputs)
#Ground truth (correct) target values.

#y_predarray-like of shape = (n_samples) or (n_samples, n_outputs)
#Estimated target values.

mae = mean_absolute_error(y_true, y_pred)
print('MAE: %.3f' % mae)

"""# **Optimizing the model for better forecasting**"""

model1=Prophet(daily_seasonality=True).add_seasonality(name='yearly',period=365,fourier_order=70)

model1.fit(df)

model1.component_modes

future_dates1=model1.make_future_dataframe(periods=365)

prediction1=model1.predict(future_dates1)

from sklearn.metrics import mean_absolute_error
y_true = df['y'].values
y_pred = prediction1['yhat'][:498].values
mae = mean_absolute_error(y_true, y_pred)
print('MAE: %.3f' % mae)

import plotly.graph_objects as go
fig = go.Figure([go.Scatter(x=df['ds'], y=df['y'],mode='lines',
                    name='Actual')])

fig.add_trace(go.Scatter(x=prediction1['ds'], y=prediction1['yhat'],
                   mode='lines+markers',
                    name='predicted'))

fig.show()

