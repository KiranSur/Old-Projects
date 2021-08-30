import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import statsmodels.api as sm
from sklearn import metrics
import numpy as np  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from country_map import regressor

test_raw = 'counties.csv'
test_raw = pd.read_csv(test_raw)
test_fips = list(test_raw['FIPS'])

for x in range(len(test_fips)):
    leftover = 5-len(str(test_fips[x]))
    test_fips[x] = ("0"*leftover) + str(test_fips[x])


test_data = test_raw.drop(["FIPS", "Area_Name"], axis=1)

y_pred = regressor.predict(test_data)

test_raw['Index'] = y_pred

df = test_raw.drop(["Unemployment", "FIPS"], axis=1)

df['FIPS'] = pd.DataFrame(test_fips)


from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df['FIPS'], z=df.Index,text=df.Area_Name,
                                    colorscale="RdBu", reversescale = True, zmin=0, zmax=df.Index.max(),
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

import plotly.express as px
fig.write_html("templates/countymap.html")