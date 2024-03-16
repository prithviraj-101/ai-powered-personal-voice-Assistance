from flask import Flask, render_template, request
import pyttsx3
from bs4 import BeautifulSoup
import requests
import pyautogui
import speech_recognition
import threading
import datetime
import wikipedia
import webbrowser
import pywhatkit
from pynput.keyboard import Key, Controller
from time import sleep

app = Flask(__name__)

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

keyboard = Controller()

running = False

def greetMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning, sir")
    elif 12 <= hour < 18:
        speak("Good Afternoon, sir")
    else:
        speak("Good Evening, sir")

    speak("Please tell me, how can I help you?")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 5)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()
    except Exception as e:
        print("Say that again")
        return "None"

def run_jarvis():
    global running
    running = True
    while running:
        query = takeCommand()
        if "wake up" in query:
            greetMe()

            while True:
                query = takeCommand()
                if "go to sleep" in query:
                    speak("Ok sir. You can call me anytime")
                    break 
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("that's great, sir")
                elif "how r u" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                elif "google" in query:
                    searchGoogle(query)
                elif "youtube" in query:
                    searchYoutube(query)
                elif "wikipedia" in query:
                    searchWikipedia(query)
                elif "temperature" in query:
                    searchTemperature("temperature in rohtak")
                elif "weather" in query:
                    searchTemperature("temperature in rohtak")
                elif "stop" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "volume up" in query:
                    volumeup()
                elif "volume down" in query:
                    volumedown()
                elif "play a game" in query:
                    game_play()
                    
def searchGoogle(query):
    if "google" in query:
        query = query.replace("jarvis", "").replace("google search", "").replace("google", "")
        speak("This is what I found on Google")
        try:
            pywhatkit.search(query)
            result = wikipedia.summary(query, 1)
            speak(result)
        except:
            speak("No speakable output available")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "").replace("youtube", "").replace("jarvis", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from Wikipedia...")
        query = query.replace("wikipedia", "").replace("search wikipedia", "").replace("jarvis", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia..")
        speak(results)

def searchTemperature(query):
    search = query
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp}")

def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

def game_play():
    # Add your game logic here
    pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_jarvis():
    global running
    if not running:
        thread = threading.Thread(target=run_jarvis)
        thread.start()
    return "Jarvis started successfully!"

@app.route("/stop", methods=["POST"])
def stop_jarvis():
    global running
    running = False
    return "Jarvis stopped successfully!"

if __name__ == "__main__":
    app.run(debug=True)
