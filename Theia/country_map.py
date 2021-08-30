import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import statsmodels.api as sm
from sklearn import metrics
import numpy as np  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

pd.set_option('display.max_colwidth', -1)

data = 'data.csv'

data = pd.read_csv(data, encoding = "utf-8")

data_ref = data.drop(['Postal Code', 'Name', 'State FIPS'], axis = 1)

X = data_ref.drop(['CSI Recession Index'], axis = 1)
y = data['CSI Recession Index']

data.isnull().any()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

regressor = LinearRegression()  
regressor.fit(X_train, y_train)

coeff_df = pd.DataFrame(regressor.coef_, X.columns, columns=['Coefficient'])

y_pred = regressor.predict(X_test)

df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

test_raw = 'countries.csv'
test_raw = pd.read_csv(test_raw, encoding = "utf-8")

test_data = test_raw.drop(["Country ID", "Country"], axis=1)

y_pred = regressor.predict(test_data)

test_raw['Index'] = y_pred

globe = test_raw.drop(["Unemployment"], axis=1)

import plotly.graph_objects as go
import pandas as pd

fig = go.Figure(data=go.Choropleth(
    locations = globe['Country ID'],
    z = globe['Index'],
    text = globe['Country'],
    colorscale = 'RdBu',
    autocolorscale=False,
    reversescale = True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Severity Index',
))

fig.update_layout(
    title_text='Global Recession Severity',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)



import plotly.express as px
fig.write_html("templates/map.html")
# fig.show()

