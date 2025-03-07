import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import requests
import pytz
from datetime import datetime

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def open_app(app_name):
    if "chrome" in app_name:
        os.system("start chrome")  # Windows
        return "Opening Chrome."
    elif "notepad" in app_name:
        os.system("notepad")  # Windows
        return "Opening Notepad."
    else:
        return "App not supported."

def set_reminder(reminder):
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder}\n")
    return f"Reminder set: {reminder}"

def get_time(city):
    try:
        # Get the timezone for the city
        timezone = pytz.timezone(city)
        current_time = datetime.now(timezone).strftime("%I:%M %p")
        return f"The current time in {city} is {current_time}."
    except pytz.UnknownTimeZoneError:
        return f"Sorry, I couldn't find the timezone for {city}."

def get_weather(city):
    api_key = "1ace23f0ecfd115478e0421063297ddf"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    
    if response.get("cod") != 200:  # Check if the request was successful
        return f"Sorry, I couldn't fetch the weather for {city}."
    
    weather = response["weather"][0]["description"]
    temperature = response["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
    return f"The weather in {city} is {weather} with a temperature of {temperature:.1f}°C."

def get_news(country="us"):
    api_key = "15532429ffd54315bfe66e29b6e4f925"
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    response = requests.get(url).json()
    
    if response.get("status") != "ok":  # Check if the request was successful
        return "Sorry, I couldn't fetch the news."
    
    headlines = [article["title"] for article in response["articles"]]
    return "Here are the top headlines: " + ". ".join(headlines[:3])

if __name__ == "__main__":
    speak("Hello, Bushi!!!. I am JARVIS!!!.")
    while True:
        command = listen_command()
        if "exit" in command or "stop" in command:
            speak("Goodbye, Bushi!!!!!")
            break
        elif "open" in command:
            response = open_app(command)
        elif "remind" in command:
            response = set_reminder(command)
        elif "weather" in command:
    # Extract the city name from the command
            city = command.replace("what's the weather in", "").strip()
            response = get_weather(city)
        elif "news" in command:
    # Extract the country code from the command
            country = command.replace("tell me the news in", "").strip()
            response = get_news(country)
        elif "time" in command:
    # Extract the city name from the command
            city = command.replace("what's the time in", "").strip()
            response = get_time(city)
    
        else:
            response = "Command not recognized."
        speak(response)

        from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

OPENWEATHERMAP_API_KEY = os.getenv("1ace23f0ecfd115478e0421063297ddf")
NEWSAPI_KEY = os.getenv("15532429ffd54315bfe66e29b6e4f925")