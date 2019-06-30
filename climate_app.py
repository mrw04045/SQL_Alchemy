#################################################
# Import Dependencies
#################################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Define routes
#################################################

# Define home route
@app.route("/")
def home():
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "<br/>"
        "NOTE: start_date and end_date are in form yyyy-mm-dd<br/>"
        "/api/v1.0/start_date<br/>"
        "/api/v1.0/start_date/end_date<br/>"
    )

# Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform a query to retrieve the data and precipitation scores for last 12 months of data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    # Append results to prcp_dict
    prcp_dict = {}
    for date, prcp in results:
        prcp_dict[date] = prcp

    return jsonify(prcp_dict)

# Define stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).distinct().all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)


# Define tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)

# Define route for finding tmin, tmax, and tavg for dates >= start date
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    # Create dictionary st_date_dict with results
    st_date_dict = {}
    for tmin, tmax, tavg in results:
        st_date_dict["min temp"] = tmin
        st_date_dict["max temp"] = tmax
        st_date_dict["avg temp"] = tavg
    
    return jsonify(st_date_dict)

# Define route for finding tmin, tmax, and tavg for dates >= start date and <= end date
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)).filter(and_(Measurement.date >= start_date, Measurement.date <= end_date)).all()

    # Create dictionary st_end_date_dict with results
    st_end_date_dict = {}
    for tmin, tmax, tavg in results:
        st_end_date_dict["min temp"] = tmin
        st_end_date_dict["max temp"] = tmax
        st_end_date_dict["avg temp"] = tavg

    return jsonify(st_end_date_dict)
           
if __name__ == "__main__":
    app.run(debug=True)

