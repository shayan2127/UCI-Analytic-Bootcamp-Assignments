import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

#########################
app = Flask(__name__)
#########################

@app.route("/")
def welcome():

    return (
        f"Here are the list of available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start</br>"
        f"/api/v1.0/start/end"
    )

#######################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():

    first_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_selected = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    falls = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_selected).order_by(Measurement.date).all()

    total_falls = []
    for fall in falls:
        row = {}
        row["date"] = fall[0]
        row["prcp"] = fall[1]
        total_falls.append(row)

    return jsonify(total_falls)

#######################################################################

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.name, Station.station)
    stations_df = pd.read_sql(stations.statement, stations.session.bind)
    
    return jsonify(stations_df.to_dict())

#######################################################################

@app.route("/api/v1.0/tobs")
def tobs():

    first_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_selected = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_selected).order_by(Measurement.date).all()

    total_temps = []
    for temp in temps:
        row = {}
        row["date"] = temp[0]
        row["tobs"] = temp[1]
        total_temps.append(row)

    return jsonify(total_temps)

#######################################################################

@app.route("/api/v1.0/start")
def start():
  
    two_years = dt.timedelta(days=730)
    end =  dt.date(2017, 8, 23)
    first_date = end - two_years

    observed_temps_tyrs = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= first_date).filter(Measurement.date <= end).all()
    observed_temps_tyrs

    tyrs_temps = list(np.ravel(observed_temps_tyrs))
    
    return jsonify(tyrs_temps)

#######################################################################
# I have noticed that this part and previous part cannot be run at the same time; so please push Ctrl+C and exit the python 
# and then re-run the code which will work and the previous part will not!

@app.route("/api/v1.0/start/end")
def startend():

    one_year = dt.timedelta(days=365)
    end =  dt.date(2017, 8, 23)
    first_date = end - one_year

    observed_temps_oyr = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= first_date).filter(Measurement.date <= end).all()
    observed_temps_oyr

    oyr_temps = list(np.ravel(observed_temps_oyr))
    
    return jsonify(oyr_temps)

#######################################################################

if __name__ == '__main__':
    app.run(debug=True)
