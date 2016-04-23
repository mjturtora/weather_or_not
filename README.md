# weather_or_not

`weather_or_not` is a project created for the "Clear to land" challenge of the 2016 
[NASA Space Apps Challenge] (https://2016.spaceappschallenge.org/locations/tampa-fl-usa)

4/22/16

The project will use the API at [NOAA's AVIATION WEATHER CENTER] (https://www.aviationweather.gov/dataserver) 
dataserver to find if there are any SIGMET warnings within a traveller's flight path that might result in a 
flight delay.

The UI will allow the traveller to input their departure and destination airports and 
ask if they have a direct flight. If not, layover airports will be requested. From the 
list of airports on the traveller's itinerary, version 0 will do a real time query of the 
Aviation 
Weather Center to determine if there is the potential for a weather related flight 
delay at the time of the request.

Enhancements might include incorporating weather forecasts to predict problems for 
flights at some future time, checking real time flight data for reported delays, and 
machine learning methods for delay prediction.