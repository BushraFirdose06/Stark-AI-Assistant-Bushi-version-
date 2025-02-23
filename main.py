import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import requests

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

def get_weather(city="New York"):
    api_key = "1ace23f0ecfd115478e0421063297ddf"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    weather = response["weather"][0]["description"]
    return f"The weather in {city} is {weather}."

def get_news():
    api_key ="15532429ffd54315bfe66e29b6e4f925"  # news API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    headlines = [article["title"] for article in response["articles"]]
    return "Here are the top headlines: " + ". ".join(headlines[:3])

if __name__ == "__main__":
    speak("Hello, Bushi!!!. I am JARVIS!!!.")
    while True:
        command = listen_command()
        if "exit" in command or "stop" in command:
            speak("Goodbye, Bushi!!!!! miss yah.")
            break
        elif "open" in command:
            response = open_app(command)
        elif "remind" in command:
            response = set_reminder(command)
        elif "weather" in command:
            response = get_weather()
        elif "news" in command:
            response = get_news()
        else:
            response = "Command not recognized."
        speak(response)

        from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")