# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 00:14:57 2021

@author: abdewang
"""

from flask import Flask, render_template, request, jsonify
#import jsonify
import requests
#import waitress
import pickle
import numpy as np
import pandas as pd
import sklearn


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Age = int(request.form['Age'])
        Sex = request.form['Sex']
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form['smoker']
        region = request.form['region']

    
    entries = [[Age,Sex,bmi,children,smoker,region]]
    
    cols = ['age','sex','bmi','children','smoker','region']
    
    df = pd.DataFrame(data = entries, columns = cols )
    
    # data encoding
    if df['sex'].loc[0].lower() == 'female':
        df['sex_male'] = 0
        df = df.drop('sex',axis = 1)
    elif df['sex'].loc[0].lower() == 'male':
        df['sex_male'] = 1
        df = df.drop('sex',axis = 1)
    else:
        return "please enter the correct value of sex"
        
        
    if df['smoker'].loc[0].lower() == 'no':
        df['smoker_no'] = 0
        df = df.drop('smoker',axis = 1)
    elif df['smoker'].loc[0].lower() == 'yes':
        df['smoker_yes'] = 1
        df = df.drop('smoker',axis = 1)
    else:
        return "please enter the correct value of smoker"
    
    if df['region'].loc[0].lower() == 'northwest':
        df['region_northwest'] = 1
        df['region_southeast'] = 0
        df['region_southwest'] = 0
        df = df.drop('region',axis = 1)
    elif df['region'].loc[0].lower() == 'southeast':
        df['region_northwest'] = 0
        df['region_southeast'] = 1
        df['region_southwest'] = 0
        df = df.drop('region',axis = 1)
    elif df['region'].loc[0].lower() == 'southwest':
        df['region_northwest'] = 0
        df['region_southeast'] = 0
        df['region_southwest'] = 1
        df = df.drop('region',axis = 1)
    else:
        return "please enter the correct value of region"
        
    if df.shape[1] == 8:
        prediction = model.predict(df)
        
        return render_template('index.html',prediction_text="Medical Insurance Cost is {}".format(prediction))

if __name__=="__main__":
    app.run(host='0.0.0.0', port=$PORT)
    #app.run(host='0.0.0.0', port=5003,debug=True)
    #waitress.serve(app, host='0.0.0.0', port=5003)
