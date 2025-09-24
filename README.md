# IA1-Data-Mashup

# Project Description:

APIs used (with links):
1. GeoDB Cities API (https://rapidapi.com/wirefreethought/api/geodb-cities)
2. OpenWeatherMap API (https://openweathermap.org/api)

## How to set up and run locally?
0. Sign-up in GeoDB Cities API and OpenWeatherMap API to get your unique API key. Do not share this to anyone.

1. Create a virtual environment
```
python -m venv .venv
```
2. Activate the virtual environment. Ensure that you are in the folder where the venv is stored.
``` 
(for Windows) venv\Scripts\activate
```
```
(for Mac) source venv/bin/activate
```
3. Install Flask (skip this step if you have it installed already)
```
python -m pip install flask requests python-dotenv
```
4. Create an .env file. Input your API keys in this file as is; no other punctuations. Again, do not share it as these APIs have a limit rate for every account.
```
GEODB_API_KEY=your_geodb_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```
5. Run the flask server through typing this in the terminal. Ensure that you are in the folder where app.py is.
```
python app.py
```
6. If the previous steps worked properly, there should be some lines that say:
```
*Running on http://127.0.0.1:5000/
Press CTRL+C to quit
```

## How the data join works (with a short example)
1. When searching for a city, the app first calls GeoDB Cities API using the input. The latitude and longitude returned by GeoDB are sent to OpenWeatherMap API to get real-time weather data.
```
example:
{
    "id": "12345",
    "city": "Manila",
    "country": "Philippines",
    "latitude": 14.5995
    "longitude": 120.9842
}
```
2. The coordinates used as a logical key allows data from both APIs to be merged into a single object in Python. 
```
{
  "main": {
    "temp": 30.5,
    "feels_like": 32.1,
    "humidity": 70
  },
  "weather": [
    { "description": "light rain" }
  ],
  "wind": {
    "speed": 3.5
  }
}
```
2.1 There is a computed field, feels_like_difference that shows the difference between the actual temperature and the 'feels like' temperature.
```
feels_like_difference = feels_like - temp = 32.1 - 30.5 = 1.6
```

3. The combined data is sent to results.html where it will displayed in a unified view.
```
{
  "city": "Manila",
  "country": "Philippines",
  "latitude": 14.5995,
  "longitude": 120.9842,
  "temperature": 30.5,
  "feels_like": 32.1,
  "description": "light rain",
  "humidity": 70,
  "wind_speed": 3.5,
  "feels_like_difference": 1.6
}
```

## NOTE: Known limitations
- The APIs have a limit rate.
- The search is limited to top 5 city matches only.

###### AI usage:
- Used to provide guidance on API integration and structuring the project using Flask.
- Used to integrate the loading circle in terms of its appearance and functionality (such as when it should only appear).
- Used to know how to hide API keys when committing project to Github
- Generate API results to be used as an example.

