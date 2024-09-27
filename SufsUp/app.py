# Import the dependencies.

from flask import Flask, jsonify
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

# reflect the tables

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return jsonify({
        'Available Routes': [
            '/api/v1.0/precipitation',
            '/api/v1.0/stations',
            '/api/v1.0/tobs',
            '/api/v1.0/<start>',
            '/api/v1.0/<start>/<end>'
        ]
    })

@app.route('/api/v1.0/precipitation') #something is wrong
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= 'last_year_date').all()  # Replace with actual date logic
    session.close()
    
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

@app.route('/api/v1.0/stations') #this one was fine
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs') #something is wrong 
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= 'last_year_date').all()  # Replace with actual date logic
    session.close()
    
    tobs_list = [tob[0] for tob in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>') #start is a url variable, start is suppose to be replaced by somthing ex. date, meausements #need to figure out the value to replace start, is suppose to be a date
def start(start):   
    session = Session(engine)
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    session.close()
    
    return jsonify({
        'TMIN': results[0][0],
        'TAVG': results[0][1],
        'TMAX': results[0][2]
    })

@app.route('/api/v1.0/<start>/<end>') #need to figure out was start and end is, probs a date
def start_end(start, end):
    session = Session(engine)
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    
    return jsonify({
        'TMIN': results[0][0],
        'TAVG': results[0][1],
        'TMAX': results[0][2]
    })

if __name__ == '__main__':
    app.run(debug=True)

