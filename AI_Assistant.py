#!/usr/bin/env python
# coding: utf-8

# Import Libraries
import speech_recognition as sr
import pyttsx3
import flask_webapp

# libs for user commands
import datetime
import wikipedia
import webbrowser
import time
from ecapture import ecapture as ec
import random

# not used
import json
import requests
import pyaudio
import wolframalpha
import os
import subprocess

# _________________________________________________________________
# Setup voice engine

engine = pyttsx3.init(driverName='sapi5', debug=True)  # initialize the text-to-speech engine
voices = engine.getProperty('voices')  # get available voices
engine.setProperty('voice', 'voices[1].id')  # set male voice (number 1)
engine.setProperty('rate', 175)  # set speech speed/rate


# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greeting():
    hello_list = ["Hello", "Hi", "Haalaa"]
    greeting_list = ["Good Morning", "Good Afternoon", "Good Evening"]
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speech = random.choice(hello_list) + " " + greeting_list[0]
        speak(speech)
        print(speech)
    elif 12 <= hour < 18:
        speech = random.choice(hello_list) + " " + greeting_list[1]
        speak(speech)
        print(speech)
    else:
        speech = random.choice(hello_list) + " " + greeting_list[2]
        speak(speech)
        print(speech)


def takeCommand():
    r = sr.Recognizer()
    repeat_command = ["Pardon me, please say that again", "Sorry, could you repeat that", "Could you repeat that"]
    now = datetime.datetime.now().time()  # time object
    print(now)
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"User said:{statement}\n")

        except Exception as e:
            speak(random.choice(repeat_command))
            return "None"
        return statement


def digital_commands(audio):
    global ai_assistant_running
    statement = audio
    created_by = ["who made you", "who created you", "who discovered you"]
    bye_bye = ["bye", "stop", "shut down", "shutdown", "turn off", "turnoff"]

    # todo: add again function: repeats the last answer
    # todo: add sissers rock paper game

    if any(sub_list in statement for sub_list in bye_bye):
        speak('your personal assistant Kareem is shutting down')
        time.sleep(0.2)
        speak('Good bye')
        print('your personal assistant Kareem is shutting down, Good bye')
        engine.stop()
        ai_assistant_running = False

    if 'wikipedia' in statement:
        speak('Searching Wikipedia...')
        statement = statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in statement:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("youtube is open now")
        time.sleep(5)

    elif 'open google' in statement:
        webbrowser.open_new_tab("https://www.google.com")
        speak("Google chrome is open now")
        time.sleep(5)

    elif 'open gmail' in statement:
        webbrowser.open_new_tab("https://gmail.com")
        speak("Google Mail open now")
        time.sleep(5)

    elif 'time' in statement:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"the time is {strTime}")

    elif 'news' in statement:
        news = webbrowser.open_new_tab("https://edition.cnn.com/")
        speak('Here are some headlines from the CNN news, Happy reading')
        time.sleep(6)

    elif "camera" in statement or "take a photo" in statement:
        ec.capture(0, "robo camera", False)

    elif 'search' in statement:
        statement = statement.replace("search", "")
        webbrowser.open_new_tab(statement)
        time.sleep(5)

    elif 'who are you' in statement or 'what can you do' in statement:
        speak("I am Kareem, a personal assistant to help you in your tasks.")

    elif any(sub_list in statement for sub_list in created_by):
        speak("I was built by Anas")
        print("I was built by Anas")


if __name__ == '__main__':

    global ai_assistant_running

    Loading_assistant_speech = "Loading personal assistant Kareem"
    speech = ["Tell me how can I help you?", "How can I help you?", "Can I help you?", "Hey, how can I assist you?"]

    print(Loading_assistant_speech)
    speak(Loading_assistant_speech)
    greeting()

    # count = 1
    ai_assistant_running = True
    if ai_assistant_running: speak(random.choice(speech))

    # time_intervals = []
    while ai_assistant_running:
        # now = datetime.datetime.now().time() # time object
        # print(now)
        # time_intervals.append(now)
        audio = takeCommand().lower()  # audio is type: str
        digital_commands(audio)

# ___________________________________________________________________________________________________________
# Improvements:

# 1. create a couple of lists with random.choice()
# 2. Create separate function for the commands
# 3. Better user sentence analyses, to have more robust understanding of the command
# 4. Deploy as a web app
# 5. When the assistant is not capable of doing a command, it should tell the user so
# (meaning the program does not have that command listed)
# 6. Test each command function
# 7. Turn assistant off after some rounds when no reply is received
