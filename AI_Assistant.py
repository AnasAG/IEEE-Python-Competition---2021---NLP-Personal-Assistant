#!/usr/bin/env python
# coding: utf-8

# Import Libraries
import speech_recognition as sr
import pyttsx3

# import gui_interface as gui

# libs for user commands
import datetime
import wikipedia
import webbrowser
import time
from ecapture import ecapture as ec
import pyjokes
import random
import config
# not used
# import json
# import requests
# import pyaudio
# import wolframalpha
# import os
# import subprocess

from tkinter import *
from tkinter.ttk import *
import threading


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.root = None
        self.txt = None
        self.assistant_mode = None

    def configure_root(self):

        self.root.title("Personal Assistant GUI")
        self.root.rowconfigure(0, minsize=100, weight=1)
        self.root.columnconfigure(1, minsize=100, weight=1)
        # self.root.geometry("")
        self.root.iconbitmap(r"images\microphone.png")
        # self.root.resizable(width=FALSE, height=FALSE)

    def create_widgets(self):
        Label(self.root, text='Personal Assistant', anchor=CENTER).grid(row=0, columnspan=2)
        Button(self.root, text='Start Recording', cursor='hand2').grid(row=1, column=0,
                                                                       sticky=W + E)  # , image=mic_image
        self.txt = Text(self.root)
        self.txt.grid(row=1, column=1, sticky=W + E, padx=20, pady=20)
        print('App create widgets')

    def button_value(self):
        self.assistant_mode = 1
        print("self.assistant_mode is ", self.assistant_mode)
        print('inside button_value func')

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.configure_root()
        Label(self.root, text='Personal Assistant', anchor=CENTER).grid(row=0, columnspan=2)
        Button(self.root, text='Start Assistant', command = self.button_value,cursor='hand2').grid(row=1, column=0,
                                                                       sticky=W + E)  # , image=mic_image
        self.txt = Text(self.root)
        self.txt.grid(row=1, column=1, sticky=W + E, padx=20, pady=20)
        self.root.update()
        self.root.update_idletasks()

        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

    def run_app_with_code(self):
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

    def text_insert_assistant(self, text_input):
        self.txt.insert(END, "Assistant: " + text_input + "\n")

    def text_insert_user(self, text_input):
        self.txt.insert(END, "User: " + text_input + "\n")


# initialize the GUI class, to be able to use its functions in the code
app = App()
time.sleep(2)  # time for the gui setup to complete processing

# Setup voice engine
engine = pyttsx3.init(driverName='sapi5', debug=True)  # initialize the text-to-speech engine
voices = engine.getProperty('voices')  # get available voices
engine.setProperty('voice', voices[0].id)  # set male voice (number 0), female voice (number 2)
engine.setProperty('rate', 175)  # set speech speed/rate


def speak(text):
    """Say the text then wait the internal process to finish"""
    engine.say(text)
    engine.runAndWait()


def greeting():
    """Greet the user with the appropriate reaction depending on time of the day"""
    hello_list = ["Hello", "Hi"]
    greeting_list = ["Good Morning", "Good Afternoon", "Good Evening"]
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speech = random.choice(hello_list) + " " + greeting_list[0]
        speak(speech)
        app.text_insert_assistant(speech)
        print(speech)
    elif 12 <= hour < 18:
        speech = random.choice(hello_list) + " " + greeting_list[1]
        speak(speech)
        app.text_insert_assistant(speech)
        print(speech)
    else:
        speech = random.choice(hello_list) + " " + greeting_list[2]
        speak(speech)
        app.text_insert_assistant(speech)
        print(speech)


def takeCommand():
    """Initialize the microphone and speech recognition"""
    r = sr.Recognizer()
    repeat_command = ["Pardon me, please say that again", "Sorry, could you repeat that", "Could you repeat that"]

    with sr.Microphone() as source:
        app.text_insert_assistant("Listening...")
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            app.text_insert_user(f"{statement}\n")  # (f"User said:{statement}\n")
            print(f"User said:{statement}\n")

        except Exception:
            speak(random.choice(repeat_command))
            return "None"

        return statement


def digital_commands(audio):
    """Contains the commands which the personal assistant can perform"""
    statement = audio
    created_by = ["who made you", "who created you", "who discovered you", "your name"]
    bye_bye = ["bye", "stop", "shut down", "shutdown", "turn off", "turnoff"]
    available_commands = ["commands", "tasks", "assist"]
    connectors = ["how", "what", "can", "do"]

    # print("Init statement", statement)
    # print("Init statement", type(statement))
    # print("silence_counter", silence_counter)
    # print("silence_counter", type(silence_counter))

    # todo: add scissors rock paper game

    if any(sub_list in statement for sub_list in bye_bye):
        speak('your personal assistant Kareem is shutting down')
        time.sleep(0.2)
        speak('Good bye')
        app.text_insert_assistant('your personal assistant Kareem is shutting down, Good bye')
        print('your personal assistant Kareem is shutting down, Good bye')
        engine.stop()
        config.ai_assistant_running = False
        config.silence_counter = 0
        app.assistant_mode = 0
        config.was_assistant_off = 1
        # to exit the function and not check the other commands
        return None

    if statement == "none":
        config.silence_counter += 1
    else:
        config.silence_counter = 0

    if 'wikipedia' in statement:
        app.text_insert_assistant('Searching Wikipedia...')
        speak('Searching Wikipedia...')
        statement = statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)

        speak("According to Wikipedia")
        app.text_insert_assistant("According to Wikipedia" + results)
        print(results)
        speak(results)

    elif 'open youtube' in statement:
        webbrowser.open_new_tab("https://www.youtube.com")
        app.text_insert_assistant("youtube is open now")
        speak("youtube is open now")
        time.sleep(5)

    elif 'open google' in statement:
        webbrowser.open_new_tab("https://www.google.com")
        app.text_insert_assistant("Google chrome is open now")
        speak("Google chrome is open now")
        time.sleep(5)

    elif 'open gmail' in statement:
        webbrowser.open_new_tab("https://gmail.com")
        app.text_insert_assistant("Google Mail open now")
        speak("Google Mail open now")
        time.sleep(5)

    elif 'time' in statement:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        app.text_insert_assistant(f"the time is {strTime}")
        speak(f"the time is {strTime}")

    elif 'news' in statement:
        webbrowser.open_new_tab("https://edition.cnn.com/")
        app.text_insert_assistant('Here are some headlines from the CNN news, Happy reading')
        speak('Here are some headlines from the CNN news, Happy reading')
        time.sleep(6)

    elif "camera" in statement or "take a photo" in statement:
        ec.capture(0, "CapturedByPythonProgramCamera", False)

    elif 'search' in statement:
        statement = statement.replace("search", "")
        webbrowser.open_new_tab(statement)
        app.text_insert_assistant("Your search window is ready!")
        speak("Your search window is ready!")
        time.sleep(5)

    elif 'who are you' in statement or 'what can you do' in statement:
        app.text_insert_assistant("I am Kareem, a personal assistant to help you in your tasks.")
        speak("I am Kareem, a personal assistant to help you in your tasks.")

    elif 'joke' in statement:
        joke = pyjokes.get_joke()
        app.text_insert_assistant(joke)
        speak(joke)

    elif any(sub_list in statement for sub_list in created_by):
        app.text_insert_assistant("My name is Kareem. I was built by Anas.")
        speak("My name is Kareem. I was built by Anas.")
        print("My name is Kareem. I was built by Anas.")

    elif any(sub_list in statement for sub_list in available_commands) and \
        any(sub_list in statement for sub_list in connectors):
        text = "I can do a couple of tasks, such as: ... searching online, telling the time, " \
               "search Wikipedia, telling jokes too"
        app.text_insert_assistant(text)
        speak(text)
        print(text)

    elif type(statement) is str and statement != "none":  # and "None" in statement:
        app.text_insert_assistant("Unfortunately, I can't do this command yet.")
        app.text_insert_assistant("You can check the available commands mentioned in the documentation.")
        speak("Unfortunately, I can't do this command yet.")
        speak("You can check the available commands mentioned in the documentation.")

    if config.silence_counter > 2:
        time.sleep(3)
        app.text_insert_assistant("Seems you are busy, you can call me back when you need me. Bye Bye!")
        speak("Seems you are busy, you can call me back when you need me. Bye Bye!")
        engine.stop()
        config.ai_assistant_running = False


def turn_assistant_on():
    global engine
    engine = pyttsx3.init(driverName='sapi5', debug=True)  # initialize the text-to-speech engine
    config.ai_assistant_running = True


if __name__ == '__main__':

    Loading_assistant_speech = "Loading personal assistant Kareem"
    speech = ["Tell me how can I help you?", "How can I help you?", "Can I help you?", "How can I assist you?"]

    app.text_insert_assistant(Loading_assistant_speech)
    print(Loading_assistant_speech)
    speak(Loading_assistant_speech)

    # run greeting function
    greeting()
    # set ai_assistant_running True to run the while loop below
    # config.ai_assistant_running = True
    if config.ai_assistant_running: speak(random.choice(speech))

    while True:

        if config.ai_assistant_running:
            # if config.was_assistant_off:
            #     greeting()
            #     config.was_assistant_off = 1
            # hear the user and take command
            print("still in while loop ...")
            audio = takeCommand().lower()
            # take action and do what the user asks for
            digital_commands(audio)

        if app.assistant_mode:
            turn_assistant_on()

# ___________________________________________________________________________________________________________
# Improvements:
# Done:
# 1. create a couple of lists with random.choice()
# 2. Create separate function for the commands
# 5. When the assistant is not capable of doing a command, it should tell the user so
# (meaning the program does not have that command listed)
# 7. Turn assistant off after some rounds when no reply is received
# Dev:
# 3. Better user sentence analyses, to have more robust understanding of the command
# 4. Deploy as a web app
# 6. Test each command function
