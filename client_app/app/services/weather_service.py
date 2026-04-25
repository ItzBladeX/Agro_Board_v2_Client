import geocoder, requests
import streamlit as st



def fetch_weather():
    try:
        lat, lon = geocoder.ip('me').latlng
        # url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation"
        print("Your approximate location (latitude, longitude):", lat, lon)

        response = requests.get(url)
        data = response.json()
        return data
    except:
        return None
    

def perse_weather(data):
    geo = geocoder.ip('me')
    return {
        "temperature" : round(data["current_weather"]["temperature"],2),
        "windspeed" : round(data["current_weather"]["windspeed"],2),
        "rainfall" : round(sum(data["hourly"]["precipitation"][:12]),2),
        "city" : geocoder.ip("me")
        }
    
@st.cache_data
def get_weather():
    raw = fetch_weather()
    if raw is None:
        return {"temperature" : None,"windspeed" : None,"rainfall" : None,"city" : None,}
    return perse_weather(raw)


 # weather = data["current_weather"]

    # rainfall = sum(data["hourly"]["precipitation"][:12])

    

    # if arg == "temp":
    #     return f"☀️ {round(weather["temperature"], 2)} °C"
    # elif arg == "wind":
    #     return f"💨 {round(weather["windspeed"],2)} km/h"
    # elif arg == "rainfall":
    #     return f"🌧️ {round(rainfall,2)} mm"
    # elif arg == "station":
    #     return f"🏠 {city}"

    # print("Open-Meteo Current Weather:")
    # print(data["current_weather"])
    # print(response)
    # print(response)
    # print(f"""
    #     City: {city}
    #     State: {state}
    #     Country: {country}
    #     Time: {weather['time']}
    #     Temp: {weather["temperature"]} °C
    #     Wind Speed: {weather["windspeed"]} km/h
    #     Rainfall: {rainfall} mm
    # """)
    # lit.st.metric("Weather", weather["temperature"], -3)

# except Exception as e:
#     print(
#         "Error while Searching for weather, Try again when enternet is available !", e)
#     return "—"