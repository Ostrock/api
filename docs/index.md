# Solar Info API

"""provides an API that requests data from 7timer.info and returns in data 
model specified

This module allow to reaching the endpoint from and gathering weather information

It' retrieves data from the "civil" product that provides weather forecasting
for the next seven days with a time frame of three hours.

Passing a longitude latitude to the 7 timer app returns it as the middle point 
of an area that reaches 10 km².

The main objective is to restrict the information retrieved only for two day
from date.

This module implements a simple logic to reverse and estimate an average of the 
portion of retrieved area that is going to be in an open sky receiving direct
solar radiation

## Endpoints
There are two endpoints, booth requests the data from 7timer but from different
imputs

### seven-timer endpoint 
To access this endpoint go to the provided URl or to your localhost O(on docker
it should be http://0.0.0.0)

there are two parameter to pass: 
 * lon: a string representing the intended longitude coordinate
 * lat: a string representing the intended latitude coordinate

Each of the parameters can provided the information in any of this forms:
 * 52.3106763272102
 * 52,3106763272102
 * -52.3106763272102
 * +52.3106763272102
 * +52,3106763272102
 * 52
 * +52
 * -52

 It' advised that is preferably using any forms with or without the dot as a 
 decimal separator

 Even though the API can handler parameters with commas as a decimal separator
 this is considered a mistake e will raise a wirning log message to inform the
 user that dot is preferable.

 ## postal endpoint
Postal endpoint uses googlemaps api to retrieve the of that query and return the
specified information

There are just one parameters for this endpoint:
* code: a string representing the postal or zip code 

The google maps API can geodecode any query that return one single result.

You can search for for addresses or cities 

## Result
The result of this api is immediately return to the browser as a 
"WeatherTimeSeriesDcit object with the following fields and types:

    - "timestamp": str,
    - "end_date": str,
    - "lon": float,
    - "lat": float,
    - "dataseries": [
                     "timestamp": str, 
                     "cloud_cover": int, 
                     "temperature": int, 
                     "open_sky": float
 
    *timestamp: a string representation of the requested information to 7timer
        in utc time
    *end_date: a string representation of the end_date in utc time
    *lon: the longitude requested as a float
    *lat: The Latitude requested as a float
    *dataseries: a set of data returned from 7timer filtered to display:
        ** timestamp for the weather forecasting
        ** cloud_cover as an int that references to a table with minimum and maximum
            percentage that the area covered by clouds
        ** temperature as an int in for the weather forecasting
        ** open_sky: an average estimative of the uncovered area of retrieved 
            data 
 
 This simplifies the parameters needed to be passed to 7timer endpoint, these 
 are handled by the application

 If the provided location is in the boundaries 

 ## Run the application
 Clone the repository
 got to the file api.src.handlers.gmpas.py and insert your googmaps API-KEY

 Build the image with the command:
 > docker image build --file custom-docker-file-name --tag demo-app-image

 run the docker image:
 docker container run --publish 80:80 --name demo-app-container demo-app-image

access the endpoint you prefer and pass the parameters:
* seven-timer: localhost/seven-timer?lon=0&lat=0
* postal: localhost/postal?code=28014