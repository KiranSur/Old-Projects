import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def scale(x, emphasis, train):
  scalar = MinMaxScaler(feature_range=(0,1))
  scalarEmphasis = MinMaxScaler(feature_range=(0,100))
  x_scaled = scalar.fit_transform(x)
  for emphasisValue in emphasis:
    emphasis_scaled = scalarEmphasis.fit_transform(np.array(train[train.columns.values[emphasisValue]]).reshape(-1,1))
    for index in range(len(x_scaled)):
      x_scaled[index][emphasisValue] = emphasis_scaled[index]
  #print(emphasis_scaled)
  return x_scaled

def getRatings(emphasized, typeData, data):
  '''typeData = 1 means county data
    typeData = 2 means global data'''
  data = pd.read_csv(data, encoding = "utf-8")
  outputDict = dict()
  if typeData == 1:

    test_fips = list(data['FIPS'])
    for x in range(len(test_fips)):
      leftover = 5-len(str(test_fips[x]))
      test_fips[x] = ("0"*leftover) + str(test_fips[x])

    outputDict["FIPS"] = list(data["FIPS"])
    outputDict["Area_Name"] = list(data["Area_Name"])
    data = data.drop(["FIPS","State","Area_Name"],axis = 1)
  elif typeData == 2:
    outputDict["Country_ID"] = list(data["Country_ID"])
    outputDict["Country"] = list(data["Country"])
    data = data.drop(["Country_ID","Country"],axis = 1)
  else:
    raise ValueError("TypeData is not 1 or 2")
  x = np.array(data.astype(float))

  scaled = scale(x, emphasized, data)
  k = 15
  model = KMeans(n_clusters=k,algorithm = "auto",n_init=25,max_iter=500).fit(scaled)

  labels = model.labels_
  rankings = [clusterNum for clusterNum in range(k)]
  rankings.sort(key = lambda num: model.cluster_centers_[num][emphasized[0]])
  for y in range(len(rankings)):
    rankings[y] += 1
  outputDict["Index"] = [rankings[label] for label in labels]
  df = pd.DataFrame(outputDict)
  df['FIPS'] = pd.DataFrame(test_fips)

  from urllib.request import urlopen
  import json
  with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

  import plotly.graph_objects as go

  fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.FIPS, z=df.Index,text=df.Area_Name,
                                    colorscale="RdBu", reversescale = True, zmin=0, zmax=df.Index.max(),
                                    marker_opacity=0.5, marker_line_width=0))
  fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

  import plotly.express as px
  fig.write_html("templates/countycategories.html")
  #return ""

# processed = pd.read_csv("clusts.csv")
# received = getRatings([25,26],5,processed)
# print(received)