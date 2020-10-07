<!---Project Logo -->
<br />
<p align="center">
  <h3 align="center">Climate Analysis of Honolulu</h3>
  <p align="center">
    A SQLclahemy anf Flask Project
    <br />
</p>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)

<!-- ABOUT THE PROJECT -->
## About The Project

![surfs-up.png](Images/surfs-up.png)

In this project, I perform some climate analysis on the Honolulu, Hawaii. I performed the following tasks.

## Step 1 - Climate Analysis and Exploration

To begin, I used Python and SQLAlchemy to do basic climate analysis and data exploration of my climate database. All of the following analysis were completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Choose a start date and end date ensuring that the data range is approximately 3-15 days total.

* Use SQLAlchemy `create_engine` to connect to your sqlite database.

* Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* Design a query to retrieve the last 12 months of precipitation data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

  ![precipitation](Images/precipitation.png)

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Design a query to calculate the total number of stations.

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

  * Which station has the highest number of observations?

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filter by the station with the highest number of observations.

  * Plot the results as a histogram with `bins=12`.

    ![station-histogram](Images/station-histogram.png)

- - -

## Step 2 - Climate App

Once the initial analysis was complete, I designed a Flask API based on the queries that I had developed.

* I used Flask to create following routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


- - -


### Built With
* [Python](https://www.python.org/about/)
  * [SQLAlchemy](https://docs.sqlalchemy.org/en/13/)
  * [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html)
  * [Flask](https://flask-doc.readthedocs.io/en/latest/)



**Additional reference materials:**

_Best-README-Template_ Retrieved from: [https://github.com/othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)






