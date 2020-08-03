import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#from jupyter notebook, some data needed for flask
#precipitation in jupyter = last_date here
last_date = "2017-08-23"
one_year = "2016-08-23"
most_active_station = " USC00519281"


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs"
    )
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation") 
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).order_by(Measurement.date).all()

    session.close()


    ppt = []
    for data in results:
        ppt_dict = {}
        ppt_dict[data.date] = data.prcp
        ppt.append(ppt_dict)
    return jsonify(ppt)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

#Query the dates and temperature observations of the most active station for the last year of data.
  
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year).\
        all()
    session.close()

    tobs_list  = []
    for date, tobs in results:
        tobs_data = {}
        tobs_data["Station"] = most_active_station
        tobs_data["Date"] = date
        tobs_data["Temp Obs"] = tobs
        tobs_list.append(tobs_data)

    return jsonify(tobs_list)    


if __name__ == '__main__':
    app.run(debug=False)
