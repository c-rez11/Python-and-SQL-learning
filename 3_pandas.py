# pandas
import numpy as np
import pandas as pd

labels = ['a','b','c']
my_list = [10,20,30]
arr = np.array([10,20,30])
d = {'a':10,'b':20,'c':30}

#print(pd.Series(data=my_list))
#print(pd.Series(data=d))

print(pd.Series(data=my_list,index=labels))

print(pd.Series(arr))

#indexing
ser1 = pd.Series([1,2,3,4],index = ['USA', 'Germany','USSR', 'Japan'])  
print(ser1)
ser2 = pd.Series([1,2,5,4],index = ['USA', 'Germany','Italy', 'Japan'])    
print(ser2)
print(ser1['USA'])
print(ser1 + ser2) # this will try to match the indices and return the value
    #for example, this function returns 2 for USA, because in each index,
    #the USA value equals 1, so 1+1 = 2

# DataFrames
from numpy.random import randn
print(np.random.seed(101))

df = pd.DataFrame(randn(5,4),index='A B C D E'.split(),columns='W X Y Z'.split())
print(df) # prints a 5x4 vector with row labels ABCDE and columns WXYZ
print(df['W'])

# create a new column
df['new'] = df['W'] + df['Y']
print(df)
# drop it
df.drop('new',axis=1)
df.drop('E',axis=0)

print(df.loc['A']) # selecting rows
print(df.iloc[2]) #selecting based off position rather than label
print(df.loc['B','Y'])

#conditional statements
print(df>0) #returns true/false booleans
print(df[df>0]) #returns value if true, null if false
print(df[df['W']>0]) # returns rows only if value in column W is > 0
print(df[df['W']>0]['Y']) # of rows where column W is positive, return column Y

# and/or statements
print(df[(df['W']>0) & (df['Y'] > 1)]) # returns rows where both W>0 AND Y>1

# index hierarchy
df.reset_index()
newind = 'CA NY WY OR CO'.split()
df['States'] = newind #sets new column of labels at the end of the data
print(df)

df.set_index('States') #still have two indices here
print(df)

df.set_index('States',inplace=True) #now the A-E index is gone
print(df)

#multi-index DataFrame
outside = ['G1','G1','G1','G2','G2','G2']
inside = [1,2,3,1,2,3]
hier_index = list(zip(outside,inside)) #creates a list of tuples
hier_index = pd.MultiIndex.from_tuples(hier_index) #passes the tuples intot the df
print(hier_index)

df = pd.DataFrame(np.random.randn(6,2),index=hier_index,columns=['A','B'])
print(df)

#how to index over this multi-index
print(df.loc['G1'])
print(df.loc['G1'].loc[1])

df.index.names = ['Group','Num']
print(df)
print(df.xs('G1')) #prints only the rows of G1
print(df.xs(['G1',1])) #prints only the first row of G1
print(df.xs(1,level='Num')) #prints only the first row of each group


#dealing with missing data
df = pd.DataFrame({'A':[1,2,np.nan],
                  'B':[5,np.nan,np.nan],
                  'C':[1,2,3]})
print(df) #as we see, there are null values
print(df.dropna()) #drop any rows that have nulls
print(df.dropna(axis=1)) #drop entire column if contains null
print(df.dropna(thresh=2)) #if there are 2 or more nulls, drop the row
print(df.fillna(value='Fill Value')) #inputs your input for the nulls
print(df['A'].fillna(value=df['A'].mean())) # fill nulls with the mean (not recommended)


#group by
data = {'Company':['GOOG','GOOG','MSFT','MSFT','FB','FB'],
       'Person':['Sam','Charlie','Amy','Vanessa','Carl','Sarah'],
       'Sales':[200,120,340,124,243,350]}
df = pd.DataFrame(data)
print(df)
by_comp = df.groupby("Company") #group rows by company
print(by_comp.mean()) #mean sales by company
print(by_comp.describe())


#merging, joining, and concatenating
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                        index=[0, 1, 2, 3])
df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                         index=[4, 5, 6, 7]) 
df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                        index=[8, 9, 10, 11])
print(df1)
print(pd.concat([df1,df2,df3])) #concat adds rows to existing columns
print(pd.concat([df1,df2,df3],axis=1)) #concat adds columns; lots of null data

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']}) 

print(pd.merge(left,right,how='inner',on='key')) #merges data on key, similar to SQL inner join
    #'inner' can be replaced with left, right, or outer joins and they work like SQL
    #can also be done on multiple columns, such as 'key1' and 'key2'


#pandas operations (random useful stuff)
df = pd.DataFrame({'col1':[1,2,3,4],'col2':[444,555,666,444],'col3':['abc','def','ghi','xyz']})
print(df.head()) #similar to SQL's "limit 10". Default is top 5 rows
print(df['col2'].unique()) #only unique values in col2
print(df['col2'].nunique()) #number of unique value
print(df['col2'].value_counts()) #returns count of each unique value

#select from df using criteria from multiple columns
newdf = df[(df['col1']>2) & (df['col2']==444)]
print(newdf)

#applying functions
def times2(x):
    return x*2
print(df['col1'].apply(times2))


del df['col1'] #delete column
print(df.columns) #get column names
print(df.index) #get index names

print(df.sort_values(by='col2')) #sort values
print(df.isnull()) #check for nulls. Returns TRUE if null
df.dropna() #drops null values

df = pd.DataFrame({'col1':[1,2,3,np.nan],
                   'col2':[np.nan,555,666,444],
                   'col3':['abc','def','ghi','xyz']})
print(df.head())
print(df.fillna('FILL')) # replace nulls with specific value

#pivot table
data = {'A':['foo','foo','foo','bar','bar','bar'],
     'B':['one','one','two','two','one','one'],
       'C':['x','y','x','y','x','y'],
       'D':[1,3,2,5,4,1]}

df = pd.DataFrame(data)
print(df) #how the data normally looks

#this pivots the data so that the values are the numbers in Column D,
#each unique value in Column C becomes its own column
#each value is indexed by columns A and B
print(df.pivot_table(values='D',index=['A','B'],columns=['C']))

#read data from csv, excel, SQL, exc
#need these packages first:
#conda install sqlalchemy, lxml, html5lib, and BeautifulSoup4

#df.to_csv('example',index=False)
#pd.read_excel('Excel_Sample.xlsx',sheetname='Sheet1')

#read HTML
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_html('http://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/')
print(df[0])

#read SQL -- this could take a bit of setup, so I won't do it here. See notes for details

