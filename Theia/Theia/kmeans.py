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
  outputDict = dict()
  if typeData == 1:
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
  output = pd.DataFrame(outputDict)

  return output

'''processed = pd.read_csv("theiaData1.csv")
received = getRatings([25,26],5,processed)
print(received)'''

