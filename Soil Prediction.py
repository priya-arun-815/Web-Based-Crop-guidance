import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geocoder
import reverse_geocoder as rg
import pprint


# Importing the dataset
dataset = pd.read_csv('SIH.csv')
X = dataset.iloc[:, 0:2].values
y1= dataset.iloc[:, 3:4].values
y2=dataset.iloc[:,4:5].values
y3=dataset.iloc[:,5:6].values
y4=dataset.iloc[:,6:7].values

#Getting the lat and long and initialising the final result

g = geocoder.ip('me')
lat=g.latlng[0]
long=g.latlng[1]
location=[[lat,long]]
final_result=[]
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X=sc.fit_transform(X)

sc1=StandardScaler()
sc2=StandardScaler()
sc3=StandardScaler()
sc4=StandardScaler()
y_EC = sc1.fit_transform(y1)
y_N = sc2.fit_transform(y2)
y_P = sc3.fit_transform(y3)
y_K = sc4.fit_transform(y4)

from sklearn.neighbors import KNeighborsRegressor as KNR
regEC=KNR(n_neighbors=8, weights='distance')
regEC.fit(XEC_train,yEC_train)

regP=KNR(n_neighbors=8, weights='distance')
regP.fit(XP_train,yP_train)

from sklearn import ensemble
params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
          'learning_rate': 0.01, 'loss': 'ls'}
regN = ensemble.GradientBoostingRegressor(**params)
regN.fit(XN_train,yN_train)

from xgboost import XGBClassifier
regK = XGBClassifier( max_depth=2,gamma=2,eta=0.8,reg_alpha=0.5,reg_lambda=0.5)
regK.fit(XK_train,yK_train)

EC=(regEC.predict(location))
EC=list(sc1.inverse_transform(EC))
final_result.extend(EC)

N=(regN.predict(location))
N=list(sc2.inverse_transform(N))
final_result.extend(N)


P=regP.predict(location)
P=list(sc3.inverse_transform(P))
final_result.extend(P)

location=np.array([[lat,long]])
K=regK.predict(b)
K=list(sc4.inverse_transform(K))
final_result.extend(K)
final_result = [ '%.3f' % elem for elem in final_result ]
final_result = [float(i) for i in final_result] 
