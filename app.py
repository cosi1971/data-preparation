# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:00:29 2019

@author: leeko
"""

from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
app = Flask(__name__)
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    impdata = 'spam.csv'
    df=pd.read_csv(impdata, encoding = "latin-1")
    df=df[['v1','v2']].copy() #drop the NaN columns
	# Features and Labels
    df['label'] = df['v1'].map({'ham': 0, 'spam': 1}) #map string values to integer values 
    df.columns=['class','message','label']
    X=df['message']
    y=df['label']
    
	# Extract Feature With CountVectorizer
    cv = CountVectorizer()
    X = cv.fit_transform(X) # Fit the Data
    
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
	#Naive Bayes Classifier
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    clf.fit(X_train,y_train)
    clf.score(X_test,y_test)
	#Alternative Usage of Saved Model
    joblib.dump(clf, 'NB_spam_model.pkl')
    NB_spam_model = open('NB_spam_model.pkl','rb')
    clf = joblib.load(NB_spam_model)
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
    return render_template('result.html',prediction = my_prediction)
if __name__ == '__main__':
	app.run(debug=True)
