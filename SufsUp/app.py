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
Base.prepare(autoload_with=engine)

# references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

#session (link) from Python to the DB

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

#percipitaion route
@app.route('/api/v1.0/precipitation') 
def precipitation():
    recent_date_query = session.query(func.max(Measurement.date)).scalar()
    last_year_date = dt.datetime.strptime(recent_date_query, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date).all()
    session.close()


    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

#stations route
@app.route('/api/v1.0/stations') 
def stations():
    results = session.query(Station.station).all()
    session.close()
    
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)


#tobs route
@app.route('/api/v1.0/tobs') 
def tobs():
    last_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    last_year_date = last_year_date.strftime('%Y-%m-%d')
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= last_year_date).all()
    session.close()
    
    tobs_list = [tob[0] for tob in results]
    return jsonify(tobs_list)

#start date route
@app.route('/api/v1.0/<start>') 
def start(start):   
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

#start and end date route
@app.route('/api/v1.0/<start>/<end>') 
def start_end(start, end):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run()

