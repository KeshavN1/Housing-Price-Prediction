import pickle
from flask import Flask, request, app, jsonify,url_for, render_template
import pandas as pd 
import numpy as np

app =Flask(__name__)
#Load the pickle file
rfmodel = pickle.load(open('rfmodel.pkl', 'rb'))
scalar = pickle.load(open('scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/predict_api', methods=['POST'])

def predict_api():
    data= request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output = rfmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict', methods=['POST']) 

def predict():
     data =[float(x) for x in request.form.values()]
     final_input = scalar.transform(np.array(data).reshape(1,-1))
     print(final_input)
     output = rfmodel.predict(final_input)[0]
     return render_template('homepage.html', prediction_text="The House Value prediction is {}".format(output) )


if __name__ =="__main__":

        app.run(debug=True)