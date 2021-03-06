# -*- coding: utf-8 -*-
"""titanic dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x9liyAYv9EYvxvVKzvBLPaL8JyYQ4_9E
"""

import pandas as pd
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns

test=pd.read_csv('test.csv')
train=pd.read_csv('train.csv')

train

train.describe()

train.Fare.sum()

train['Fare'].groupby(train['Sex']).mean()

train.isna().sum()

train["Age"].fillna(train["Age"].mean(),inplace=True )

train["Embarked"].fillna('S' ,inplace=True )

train.loc[1:5]

train[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean()

g = sns.FacetGrid(train, col='Survived')
g.map(plt.hist, 'Age', bins=20)

train[["Pclass", "Survived"]].groupby(['Pclass'], as_index=False).mean()

sns.barplot('Pclass', 'Survived', data=train, color="pink")
plt.show()

train.replace({'Sex':{'male':0,'female':1}},inplace=True)

train.replace({'Embarked':{'S':0,'C':1,'Q':2}},inplace=True)

train.drop(['PassengerId','Cabin','Ticket','Name'], axis=1,inplace=True)

x=train.drop(['Survived'], axis=1)

y=train['Survived']

#below this is modelling

corrMatrix = train.corr()
f, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(corrMatrix, annot=True)
plt.show()

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.20,random_state=42)

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix,log_loss

decision_tree = DecisionTreeClassifier()
decision_tree.fit(x_train, y_train)
Y_pred = decision_tree.predict(x_test)
acc_decision_tree = round(decision_tree.score(x_train, y_train) * 100, 2)
acc_decision_tree

model_dt = tree.DecisionTreeClassifier(criterion= "entropy")
model_dt = model_dt.fit(x_train, y_train)
y_pred = model_dt.predict(x_test)
dtc_accuracy = accuracy_score(y_test,y_pred)*100
print("accuracy=",dtc_accuracy)

model_dt2 = tree.DecisionTreeClassifier()
model_dt2 = model_dt2.fit(x_train, y_train)
y_pred = model_dt2.predict(x_test)
dtc_accuracy = accuracy_score(y_test,y_pred)*100
print("accuracy=",dtc_accuracy)

plt.figure(figsize=(50,20))
tree.plot_tree(model_dt.fit(x_train, y_train))

plt.figure(figsize=(50,20))
tree.plot_tree(model_dt2.fit(x_train, y_train))

from sklearn.tree import export_graphviz
export_graphviz(model_dt, out_file='tree_limited.dot', feature_names = x_test.columns,
                class_names = model_dt.predict(x_train).astype(str),
                rounded = True, proportion = False, precision = 2, filled = True)

from sklearn.tree import export_graphviz
export_graphviz(model_dt2, out_file='tree_limited1.dot', feature_names = x_test.columns,
                class_names = model_dt2.predict(x_train).astype(str),
                rounded = True, proportion = False, precision = 2, filled = True)

!dot -Tpng tree_limited.dot -o tree_limited.png -Gdpi=600

!dot -Tpng tree_limited1.dot -o tree_limited1.png -Gdpi=600

from IPython.display import Image
Image(filename = 'tree_limited.png')

Image(filename = 'tree_limited1.png')

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

train[train.columns] = scaler.fit_transform(train)

train

#Logistic Regression
#Important Parameters - C , penalty , solver ,
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=400 , penalty= 'l1' , solver = 'liblinear')
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
lr_accuracy = accuracy_score(y_test,y_pred)*100
lr_accuracy

y_pred=model.predict(x_test)
lr_log_loss=log_loss(y_test,y_pred)*10
lr_log_loss

from sklearn.metrics import roc_curve,auc
y_pred_proba = model.predict_proba(x_test)[:, 1]
[fpr, tpr, thr] = roc_curve(y_test, y_pred_proba)

idx = np.min(np.where(tpr > 0.95))
plt.figure()
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, color='coral', label='ROC curve (area = %0.3f)' % auc(fpr, tpr))
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (1 - specificity)', fontsize=14)
plt.ylabel('True Positive Rate (recall)', fontsize=14)
plt.title('Receiver operating characteristic (ROC) curve')
plt.legend(loc="lower right")
plt.show()

conf_mat = confusion_matrix(y_test.tolist() , y_pred )
print(conf_mat)

plt.figure(figsize=(4,4))
sns.heatmap(conf_mat,annot=True)
plt.show()

