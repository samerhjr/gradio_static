import gradio as gr
import pandas as pd
import numpy as np
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from urllib.request import urlretrieve
import pickle

def encode_ages(df): # Binning ages 
    df.Age = df.Age.fillna(-0.5)
    bins = (-1, 0, 5, 12, 18, 25, 35, 60, 120)
    categories = pd.cut(df.Age, bins, labels=False)
    df.Age = categories
    return df

def encode_fares(df): # Binning fares
    df.Fare = df.Fare.fillna(-0.5)
    bins = (-1, 0, 8, 15, 31, 1000)
    categories = pd.cut(df.Fare, bins, labels=False)
    df.Fare = categories
    return df

def encode_sex(df):
    mapping = {"male": 0, "female": 1}
    return df.replace({'Sex': mapping})

urlretrieve("https://gr-models.s3-us-west-2.amazonaws.com/titanic_model.sav","titanic_model.sav")
clf = pickle.load(open("titanic_model.sav", 'rb'))

import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('https://raw.githubusercontent.com/gradio-app/titanic/master/train.csv')

def transform_features(df):
    df = encode_ages(df)
    df = encode_fares(df)
    df = encode_sex(df)
    return df

train = data[['PassengerId', 'Fare', 'Age', 'Sex', 'Survived']]
train = transform_features(train)


X_all = train.drop(['Survived', 'PassengerId'], axis=1)
y_all = train['Survived']

num_test = 0.20
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=num_test, random_state=23)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print(accuracy_score(y_test, predictions))

def predict_survival(sex, age, fare):
    df = pd.DataFrame.from_dict({'Sex': [sex], 'Age': [age], 'Fare': [fare]})
    df = encode_sex(df)
    df = encode_fares(df)
    df = encode_ages(df)
    pred = clf.predict_proba(df)[0]
    return {'Perishes': pred[0], 'Survives': pred[1]}

sex = gr.inputs.Radio(['female', 'male'], label="Sex")
age = gr.inputs.Slider(minimum=0, maximum=120, default=22, label="Age")
fare = gr.inputs.Slider(minimum=0, maximum=1000, default=100, label="Fare (british pounds)")

iface = gr.Interface(predict_survival, [sex, age, fare], "label", live=True)