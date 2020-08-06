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
most_active_station = "USC00519281"


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
        f"/api/v1.0/tobs<br>"
        f"Enter dates in YYYY-MM-DD formats<br>"
        f"If you only provide start date, you will get minimum, average and maximum temperature for all dates greater than the date you specified.<br>"
        f"/api/v1.0/<start><br>"
        f"If you provide a start and end date, you will get a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br>"
        f"/api/v1.0/<start>/<end>"
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
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").\
        all()
    
    session.close()

    tobs_list  = []
    for station, date, tobs in results:
        tobs_data = {}
        tobs_data["Station"] = station
        tobs_data["Date"] = date
        tobs_data["Temp Obs"] = tobs
        tobs_list.append(tobs_data)

    return jsonify(tobs_list)    

#/api/v1.0/<start>`
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()
    start_date_only = []
    #print(results)
    for tmin, tavg, tmax in results:
        start_date = {}
        start_date["Minimum Temperature"] = tmin
        start_date["Average Temperature"] = tavg
        start_date["Maximum Temperature"] = tmax
        start_date_only.append(start_date)

    return jsonify(start_date_only)


# `/api/v1.0/<start>/<end>`
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    print(results)
    session.close()
    date_range = []
    for tmin, tavg, tmax in results:
        two_dates = {}
        two_dates["Minimum Temperature"] = tmin
        two_dates["Average Temperature"] = tavg
        two_dates["Maximum Temperature"] = tmax
        date_range.append(start_date)

    return jsonify(date_range)

if __name__ == '__main__':
    app.run(debug=False)
