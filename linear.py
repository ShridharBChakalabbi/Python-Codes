import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
from sklearn.datasets import load_boston
boston=load_boston()
print(boston.data)
boston.keys()
print(boston.feature_names)
print(boston.DESCR)
boston_df=pd.DataFrame(boston.data)
boston_df.columns=boston.feature_names
print(boston.data.shape)
print(boston.target.shape)
boston_df['PRICE']=boston.target
print(boston_df.head())
boston_df.info()
boston_df.describe()
boston_df.columns
sns.pairplot(boston_df)
sns.distplot(boston_df['PRICE'])
y = boston_df['PRICE']
X = boston_df[['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX','PTRATIO', 'B', 'LSTAT']]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train,y_train)
print('Coefficients: \n',lm.coef_)
predictions = lm.predict(X_test)
plt.scatter(y_test,predictions)
plt.xlabel('Y Test')
plt.ylabel('Predictions')
from sklearn import metrics
print('MSE: ',metrics.mean_squared_error(y_test,predictions))
print('RMSE: ',np.sqrt(metrics.mean_squared_error(y_test,predictions)))
sns.distplot((y_test-predictions),bins=50)
coefficients = pd.DataFrame(lm.coef_,X.columns)
coefficients.columns = ['Coefficients']
coefficients
