#seaborn

import seaborn as sns
import matplotlib.pyplot as plt
tips = sns.load_dataset('tips') #seaborn built-in dataset
print(tips.head())

#histogram
#sns.displot(tips['total_bill'])


#joint plots
#sns.jointplot(x='total_bill',y='tip',data=tips,kind='scatter') #also do kind = 'reg' or 'hex'

#sns.pairplot(tips) #plots pairwise relationships across dataframe

#sns.pairplot(tips,hue='sex',palette='coolwarm') #distinguish between sexes


#lesson ends with interesting kernel plots that are used to make a normal Gaussian distribution

#sns.boxplot(x="day", y="total_bill", data=tips,palette='rainbow')



#matrix plots
flights = sns.load_dataset('flights')

#heatmap
print(tips.corr())
#sns.heatmap(tips.corr(),cmap='coolwarm',annot=True)

#for flights
pvflights = flights.pivot_table(values='passengers',index='month',columns='year')
print(pvflights)
#sns.heatmap(pvflights)
#sns.clustermap(pvflights) #notice how this clusters the years and months by their volumes

#grids
iris = sns.load_dataset('iris')
print(iris.head())

g = sns.PairGrid(iris) #PairGrid is the setup
#g.map(plt.scatter) #maps to the grid. This shows correlation
#sns.pairplot(iris)

#regression plots
sns.lmplot(x='total_bill',y='tip',data=tips)

#pandas built-in viz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df1 = pd.read_csv('df1',index_col=0)
plt.style.use('dark_background') #not sure why this isn't working

print(df1['A'].hist())
#plt.show()

#interactive data viz using Plotly and Cufflinks
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import chart_studio.plotly as py
import plotly_express as px

df = pd.DataFrame(np.random.randn(100,4),columns='A B C D'.split()) #random data
print(df.head())

df2 = pd.DataFrame({'Category':['A','B','C'],'Values':[32,43,50]})
print(df2.head())
#init_notebook_mode(connected=True)
cf.set_config_file(offline=True)
#df.iplot(kind='scatter',x='A',y='B',mode='markers',size=10)
#df2.iplot(kind='bar',x='Category',y='Values')
#not working; kinda frustrating
ar = np.arange(100).reshape((10,10))
fig = px.scatter(ar, x=2, y=6, size=1, color=5)
fig.show()
