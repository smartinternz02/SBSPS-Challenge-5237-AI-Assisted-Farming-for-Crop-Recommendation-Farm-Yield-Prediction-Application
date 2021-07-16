#importing libraries
from operator import indexOf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template,request,send_from_directory
import os
import pickle

from numpy.core.fromnumeric import round_ 
app = Flask(__name__) #Initialize the flask App

cropRec = pd.read_csv('./Crop_recommendation.csv')
cropYield = pd.read_csv('./Crop_Yield.csv')

Nmodel = pickle.load(open('./Trained_Models/N.pkl', 'rb'))
Pmodel = pickle.load(open('./Trained_Models/P.pkl', 'rb'))
Kmodel = pickle.load(open('./Trained_Models/K.pkl', 'rb'))
cropmodel = pickle.load(open('./Trained_Models/crop.pkl', 'rb'))
yieldmodel = pickle.load(open('./Trained_Models/yield.pkl', 'rb'))
costmodel = pickle.load(open('./Trained_Models/cost.pkl', 'rb'))

label_object = {}
categorical_columns = ['label','state','encodedLabel','encodedState']
for col in categorical_columns[:2]:
    labelencoder = LabelEncoder()
    labelencoder.fit(cropYield[col])
    cropYield[categorical_columns.index(col)+2] = labelencoder.fit_transform(cropYield[col])
    label_object[col] = labelencoder

#default page of our web-app
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    #For rendering results on HTML GUI
    int_features = [x for x in request.form.values()]
    app.logger.info(int_features)
    state = int_features[4]
    try:
        for i in range(4):
            int_features[i] = float(int_features[i])
    except:
        return render_template('index.html',prediction_text='Please provide valid input!',yield_text=' ',cost_text=' ')
    final_features = np.array([int_features[:4]])
    nitrogen = Nmodel.predict(final_features)[0]
    phosporus = Pmodel.predict(np.array([[nitrogen]+int_features[:4]]))[0]
    pottasium = Kmodel.predict(np.array([[nitrogen]+[phosporus]+int_features[:4]]))[0]
    crop = cropmodel.predict(np.array([[nitrogen]+[phosporus]+[pottasium]+int_features[:4]]))[0]
    app.logger.info(state)
    
    if crop in cropYield['label'].to_numpy():
        X=[label_object['label'].transform(np.array([crop]))[0],label_object['state'].transform(np.array([state]))[0]]
        yield_quantity = round(yieldmodel.predict(np.array([X]))[0])
        cost = round(costmodel.predict(np.array([X+[yield_quantity]]))[0])
        return render_template('index.html', prediction_text='Recommended Crop: {}'.format(crop),yield_text='Estimated Yield: {} quintal/hectare'.format(yield_quantity),cost_text='Estimated cost: '+chr(8377)+' {}/hectare'.format(cost)) 
    return render_template('index.html', prediction_text='Recommended Crop: {}'.format(crop),yield_text='Estimated Yield: Not available for the above crop!',cost_text='Estimated cost: Not available for the above crop!') 


if __name__ == "__main__":
    app.run(debug=True)