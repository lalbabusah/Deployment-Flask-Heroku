from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        
        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        
        # Duration
        Duration_hour = Arrival_hour - Dep_hour
        Duration_min = Arrival_min - Dep_min
        if (Arrival_hour < Dep_hour):
            Duration_hour = Duration_hour+24
        if (Arrival_min < Dep_min):
            Duration_hour = Duration_hour-1
            Duration_min = Duration_min+60
        
        # Total Stops
        Total_Stops = int(request.form["stops"])
        
        # Airline
        Airline = [0,0,0,0,0,0,0,0,0,0,0,0]
        d1 = {'Air Asia':0, 'Air India':1, 'GoAir':2, 'IndiGo':3, 'Jet Airways':4, 'Jet Airways Business':5, 
              'Multiple carriers':6, 'Multiple carriers Premium economy':7, 'SpiceJet':8, 'Trujet':9, 
              'Vistara':10, 'Vistara Premium economy':11}
        airline=request.form['airline']
        Airline[d1[airline]] = 1
       
        # Source
        Source = [0,0,0,0,0]
        d2 = {'Banglore':0, 'Chennai':1, 'Delhi':2, 'Kolkata':3, 'Mumbai':4}
        source = request.form["Source"]
        Source[d2[source]] = 1
        
        # Destination
        Destination = [0,0,0,0,0,0]
        d3 = {'Banglore':0, 'Cochin':1, 'Delhi':2, 'Hyderabad':3, 'Kolkata':4,'New Delhi':5}
        destination = request.form["Destination"]
        Destination[d3[destination]] = 1

       
        features = [Total_Stops, Day, Month, Dep_hour, Dep_min, Arrival_hour, Arrival_min, 
                    Duration_hour, Duration_min] + Airline + Source + Destination
        prediction=model.predict([features])

        output=round(prediction[0],2)

        return render_template('index.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
