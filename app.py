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
measurement = Base.classes.measurement
station = Base.classes.station

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

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year).order_by(measurement.date).all()

    session.close()


    ppt = []
    for data in results:
        ppt_dict = {}
        ppt_dict[data.date] = data.prcp
        ppt.append(ppt_dict)
    return jsonify(ppt)

if __name__ == '__main__':
    app.run(debug=False)
