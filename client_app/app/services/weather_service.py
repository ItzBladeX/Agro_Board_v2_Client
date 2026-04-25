import geocoder, requests
import streamlit as st
@st.cache_data
def get_weather():
    raw = fetch_weather()
    if raw is None:
        return {"temperature" : "-","windspeed" : "-","rainfall" : "-","city" : "-"}
    return perse_weather(raw)

def fetch_weather():
    try:
        lat, lon = geocoder.ip('me').latlng
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation"
        print("Your approximate location (latitude, longitude):", lat, lon)
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None
    
def perse_weather(data):
    geo = geocoder.ip('me')
    return {
        "temperature" : round(data["current_weather"]["temperature"],2),
        "windspeed" : round(data["current_weather"]["windspeed"],2),
        "rainfall" : round(sum(data["hourly"]["precipitation"][:12]),2),
        "city" : geo.city if geo else None
        }
    



