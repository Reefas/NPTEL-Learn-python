import pandas as pd
import numpy as np
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

income=pd.read_csv('income.csv',na_values=[' ?'])
data=income.copy()

print(income.info())
print(income.isnull().sum())
print(income.describe())

cat_stats=income.describe(include='O')

print(income['JobType'].unique())

missing=income[income.isnull().any(axis=1)]

data2=income.dropna(axis=0)

correlation=data2.corr()

sns.countplot(data2['SalStat'])
sns.displot(data2['age'],bins=10)
sns.boxplot(y=data2['age'],x=data2['SalStat'])
sns.countplot(y='JobType',hue='SalStat',data=data2)
sns.countplot(y='EdType',hue='SalStat',data=data2)
sns.countplot(y='occupation',hue='SalStat',data=data2)
sns.boxplot(y=data2['hoursperweek'],x=data2['SalStat'])

# =============================================================================
# LogisticRegression model
# =============================================================================
 
data2['SalStat']=data2['SalStat'].map({' less than or equal to 50,000':0,' greater than 50,000':1})

#dropping insignificant variables
data2.drop(['nativecountry','race'],axis=1,inplace=True)

new_data=pd.get_dummies(data2,drop_first=True)

#storing the columns name
columns_list=list(new_data.columns)

#Separating the  input variable from columns_list
features=list(set(columns_list)-set(['SalStat']))

#Storing the output values in y
y=new_data['SalStat'].values

#Storing values from input feature
x=new_data[features].values

#Splitting the data in to train and test 
train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.3,random_state=0)

#Make an instance of LogisticRegression Model
logistic=LogisticRegression()

#fitting the values for x and y
logistic.fit(train_x,train_y)
logistic.coef_
logistic.intercept_

#Prediction from test data
pred=logistic.predict(test_x)

#Validation of model
Result=confusion_matrix(test_y,pred)   #Output is given as 2x2 matrix, Row: Actual (0,1), Column:Prediction (0,1)
accuracy=accuracy_score(test_y,pred)
print('Misclassified samples: %d'% (test_y!=pred).sum())
 
# =============================================================================
# KNN Model
# =============================================================================

from sklearn.neighbors import KNeighborsClassifier

from matplotlib import pyplot as plt

#Creating a KNN classifier instance
KNN_class=KNeighborsClassifier(n_neighbors=5)

#fitting the values for x and y
KNN_class.fit(train_x,train_y)

#Prediction from test data
KNN_pred=KNN_class.predict(test_x)

#Evaluation of model
KNN_Result=confusion_matrix(test_y,KNN_pred)
print('Accuracy score of KNN model is {}'.format(accuracy_score(test_y,KNN_pred)))
print('Misclassified samples of KNN model: %d'% (test_y!=KNN_pred).sum())


#Calculating error for k values between 1 to 20.
iteration=[]
for i in range(1,20):
    KNN_class=KNeighborsClassifier(n_neighbors=i)
    KNN_class.fit(train_x,train_y)
    KNN_pred=KNN_class.predict(test_x)
    temp=(test_y!=KNN_pred).sum()
    iteration.append(temp)
    
print(iteration)
print('Best suited value of n_neighbors is {}'.format(iteration.index(min(iteration))+1))

# =============================================================================
# END OF SCRIFT
# =============================================================================
