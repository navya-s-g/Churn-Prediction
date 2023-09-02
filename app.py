
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics
from flask import Flask, request, render_template
import pickle

app = Flask("__name__")

df_1=pd.read_csv("test.csv")

q = ""

@app.route("/")
def loadPage():
	return render_template('home.html', query="")


@app.route("/", methods=['POST'])
def predict():
    
    '''
    CustomerID	
    Name	
    Age	
    Gender	
    Location	
    Subscription_Length_Months	
    Monthly_Bill	
    Total_Usage_GB	
    '''
    

    
    inputQuery1 = request.form['query1']
    inputQuery2 = request.form['query2']
    inputQuery3 = request.form['query3']
    inputQuery4 = request.form['query4']
    inputQuery5 = request.form['query5']
    inputQuery6 = request.form['query6']
    inputQuery7 = request.form['query7']
    inputQuery8 = request.form['query8']
    
    

    model = pickle.load(open("model.sav", "rb"))
    
    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, 
             inputQuery8]]
    
    new_df = pd.DataFrame(data, columns = ['CustomerID'	,'Name'	,'Age'	,'Gender'	,'Location'	,'Subscription_Length_Months'	,'Monthly_Bill'	,'Total_Usage_GB'])
    
    df_2 = pd.concat([df_1, new_df], ignore_index = True) 
    # Group the tenure in bins of 12 months
    labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 24, 12)]
    
    df_2['Subscription_Length_Group'] = pd.cut(df_2.Subscription_Length_Months.astype(int), range(1, 30, 12), right=False, labels=labels)
    #drop column customerID and tenure
    df_2.drop(columns= ['CustomerID','Subscription_Length_Months'], axis=1, inplace=True)   
    
    
    
    
    new_df__dummies = pd.get_dummies(df_2[['Name'	,'Age'	,'Gender'	,'Location'		,'Monthly_Bill'	,'Total_Usage_GB']])
    
    
    #final_df=pd.concat([new_df__dummies, new_dummy], axis=1)
        
    
    single = model.predict(new_df__dummies.tail(1))
    probablity = model.predict_proba(new_df__dummies.tail(1))[:,1]
    
    if single==1:
        o1 = "This customer is likely to be churned!!"
        o2 = "Confidence: {}".format(probablity*100)
    else:
        o1 = "This customer is likely to continue!!"
        o2 = "Confidence: {}".format(probablity*100)
        
    return render_template('home.html', output1=o1, output2=o2, 
                           query1 = request.form['query1'], 
                           query2 = request.form['query2'],
                           query3 = request.form['query3'],
                           query4 = request.form['query4'],
                           query5 = request.form['query5'], 
                           query6 = request.form['query6'], 
                           query7 = request.form['query7'], 
                           query8 = request.form['query8'])
    
app.run()

