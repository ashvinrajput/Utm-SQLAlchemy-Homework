import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Connection
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    
    return (
        f"Welcome to the Hawaii Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/station"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
 
    session = Session(engine)

    """Return a list of all dates and precipitation"""

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    weather_data = []
    for date, prcp in results:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        weather_data.append(date_dict)

    return jsonify(weather_data)



@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)

    """Return a list stations"""

    results = session.query(Station.station).all()

    session.close()

    station = [result[0] for result in results[:]]
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    station = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.station == active_stat).all()

    session.close()
 
    
    return jsonify(active_stations)


@app.route("/api/v1.0/date/<start>")
def start_date(start):
    session = Session(engine)
    temp = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == active_stat).filter(Measurement.date > query_date).order_by(Measurement.date).all()
        filter(Measurement.date >= start).all()
    
    session.close()
    return jsonify(stn_temp)


@app.route("/api/v1.0/date/<start>/<end>")
def calc_temps(start, end):
    session = Session(engine)
    calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all().filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    return jsonify(stn_temp_range)


if __name__ == "__main__":
    app.run(debug=True)