#!/usr/bin/env python
# coding: utf-8

# Import Libraries
import speech_recognition as sr
import pyttsx3

# libs for user commands
import datetime
import wikipedia
import webbrowser
import time
from ecapture import ecapture as ec
import pyjokes
import random
import config
import sys
from tkinter import *
from tkinter.ttk import *
import threading


class App(threading.Thread):

    def __init__(self):
        self.thread = threading.Thread.__init__(self)
        self.start()
        self.root = None
        self.button = None
        self.txt = None
        self.assistant_mode = None

    def configure_root(self):
        """configure the Tk widget"""
        self.root.title("Personal Assistant GUI")
        self.root.rowconfigure(0)  # , minsize=100, weight=1
        self.root.columnconfigure(0)  # , minsize=100, weight=1
        # self.root.geometry("")
        # self.root.iconbitmap(r"images\microphone.png")
        # self.root.resizable(width=FALSE, height=FALSE)

    def set_button_value(self):
        """Set value"""
        self.assistant_mode = 1

    def callback(self):
        self.root.quit()
        # self.root.destroy()
        # sys.exit()

    def run(self):
        """Run the main commands for creating the Tkinter GUI"""
        self.root = Tk()
        self.configure_root()
        Label(self.root, text='Personal Assistant', anchor=CENTER,
              font=("Poor Richard", 30, "bold")).grid(row=0, padx=10, pady=5)
        self.button = Button(self.root, text='Start Assistant', command=self.set_button_value,
                             cursor='hand2', state=DISABLED)
        # self.button.grid(row=1, column=0, padx=5, pady=5)
        self.txt = Text(self.root, wrap=WORD, state=DISABLED, spacing1=5)
        self.txt.grid(row=2, column=0, sticky=W + E, padx=10, pady=10)
        # update internal process in Tkinter
        self.root.update()
        self.root.update_idletasks()
        # to enable the GUI and python code from working concurrently
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

    def text_insert_assistant(self, text_input):
        """Insert text in Text Widget as the Personal Assistant"""
        self.txt.configure(state=NORMAL)
        self.txt.insert(END, "Assistant: " + text_input + "\n")
        self.txt.see(END)
        self.txt.configure(state=DISABLED)

    def text_insert_user(self, text_input):
        """Insert text in Text Widget as the User"""
        self.txt.configure(state=NORMAL)
        self.txt.insert(END, "User: " + text_input + "\n")
        self.txt.see(END)
        self.txt.configure(state=DISABLED)

    def restart_personal_assistant(self):
        """Restart the assistant after shutting it down"""
        if config.ai_assistant_running is False and app.assistant_mode == 0:
            self.button.config(state=NORMAL)
            self.button.grid(row=1, column=0, padx=5, pady=5)
        else:
            self.button.config(state=DISABLED)
            self.button.grid_forget()


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
        app.text_insert_assistant(speech)
        print(speech)
        speak(speech)
    elif 12 <= hour < 18:
        speech = random.choice(hello_list) + " " + greeting_list[1]
        app.text_insert_assistant(speech)
        print(speech)
        speak(speech)
    else:
        speech = random.choice(hello_list) + " " + greeting_list[2]
        app.text_insert_assistant(speech)
        print(speech)
        speak(speech)


def takeCommand():
    """Initialize the microphone and speech recognition"""
    r = sr.Recognizer()
    repeat_command = ["Pardon me, please say that again", "Sorry, could you repeat that", "Could you repeat that"]

    with sr.Microphone() as source:
        app.text_insert_assistant("Listening...")
        print("Listening...")
        # listen to the user's voice
        audio = r.listen(source)

        try:
            # recognize the user voice, speech-to-text
            statement = r.recognize_google(audio, language='en-in')
            app.text_insert_user(f"{statement}\n")  # (f"User said:{statement}\n")
            print(f"User said:{statement}\n")

        except Exception:
            speech = random.choice(repeat_command)
            app.text_insert_assistant(speech)
            speak(speech)
            return "None"

        return statement


def digital_commands(audio):
    """Contains the commands which the personal assistant can perform"""
    statement = audio
    created_by = ["who made you", "who created you", "who discovered you", "your name", "who built you"]
    bye_bye = ["bye", "stop", "shut down", "shutdown", "turn off", "turnoff"]
    available_commands = ["commands", "tasks", "assist"]
    connectors = ["how", "what", "can", "do"]
    personal_mood = ["I'm great, thanks.", "I'm doing good, thanks.", "Feeling fantastic!"]

    # todo: add scissors rock paper game

    if any(sub_list in statement for sub_list in bye_bye):
        """Shutting down the Personal Assistant"""
        speak('your personal assistant Kareem is shutting down')
        time.sleep(0.2)
        app.text_insert_assistant('your personal assistant Kareem is shutting down, Good bye')
        speak('Good bye')
        print('your personal assistant Kareem is shutting down, Good bye')
        # configuring  variables for shutting down the personal assistant
        engine.stop()
        config.ai_assistant_running = False
        config.silence_counter = 0
        app.assistant_mode = 0
        config.was_assistant_off = 1
        app.restart_personal_assistant()
        # to exit the function and not check the other commands
        return None

    if statement == "none":
        """To check how many time the assistant gets no feedback or command from the user"""
        config.silence_counter += 1
    else:
        config.silence_counter = 0

    if 'wikipedia' in statement:
        """Open Wikipedia"""
        app.text_insert_assistant('Searching Wikipedia...')
        speak('Searching Wikipedia...')
        statement = statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)
        app.text_insert_assistant("According to Wikipedia" + results)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open' in statement and 'youtube' in statement:
        """Open youtube website"""
        webbrowser.open_new_tab("https://www.youtube.com")
        app.text_insert_assistant("youtube is open now")
        speak("youtube is open now")
        time.sleep(5)

    elif 'open google' in statement:
        """Open google"""
        webbrowser.open_new_tab("https://www.google.com")
        app.text_insert_assistant("Google chrome is open now")
        speak("Google chrome is open now")
        time.sleep(5)

    elif 'open gmail' in statement:
        """Open gmail"""
        webbrowser.open_new_tab("https://gmail.com")
        app.text_insert_assistant("Google Mail open now")
        speak("Google Mail open now")
        time.sleep(5)

    elif 'time' in statement:
        """"Get current time for the user"""
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        app.text_insert_assistant(f"the time is {strTime}")
        speak(f"the time is {strTime}")

    elif 'news' in statement:
        """Open news"""
        webbrowser.open_new_tab("https://edition.cnn.com/")
        app.text_insert_assistant('Here are some headlines from the CNN news, Happy reading')
        speak('Here are some headlines from the CNN news, Happy reading')
        time.sleep(6)

    elif "camera" in statement or "take a photo" in statement:
        """Take a picture"""
        ec.capture(0, "CapturedByPythonProgramCamera", False)

    elif 'search' in statement:
        """Search in browser for something"""
        statement = statement.replace("search", "")
        webbrowser.open_new_tab(statement)
        app.text_insert_assistant("Your search window is ready!")
        speak("Your search window is ready!")
        time.sleep(5)

    elif 'how are you' in statement:
        """Reaction of the assistant mood"""
        speech = random.choice(personal_mood)
        app.text_insert_assistant(speech)
        speak(speech)

    elif 'who are you' in statement or 'what can you do' in statement:
        """Introducing the assistant to the user"""
        app.text_insert_assistant("I am Kareem, a personal assistant to help you in your tasks.")
        speak("I am Kareem, a personal assistant to help you in your tasks.")

    elif 'joke' in statement:
        """Tells a joke"""
        joke = pyjokes.get_joke()
        app.text_insert_assistant(joke)
        speak(joke)

    elif any(sub_list in statement for sub_list in created_by):
        """Gives info about the assistant"""
        app.text_insert_assistant("My name is Kareem. I was built by Anas.")
        print("My name is Kareem. I was built by Anas.")
        speak("My name is Kareem. I was built by Anas.")

    elif any(sub_list in statement for sub_list in available_commands) and \
            any(sub_list in statement for sub_list in connectors):
        """Gives info about the assistant"""
        text = "I can do a couple of tasks, such as: ... searching online, telling the time, " \
               "search Wikipedia, telling jokes too"
        app.text_insert_assistant(text)
        print(text)
        speak(text)

    elif type(statement) is str and statement != "none":
        """When the assistant program don't understand the command, it shall run this command"""
        app.text_insert_assistant("Unfortunately, I can't do this command yet.")
        app.text_insert_assistant("You can check the available commands mentioned in the documentation.")
        speak("Unfortunately, I can't do this command yet.")
        speak("You can check the available commands mentioned in the documentation.")

    if config.silence_counter > 2:
        """If user is not communicating with the assistant, the program shall turn off"""
        time.sleep(3)
        app.text_insert_assistant("Seems you are busy, you can call me back when you need me. Bye Bye!")
        speak("Seems you are busy, you can call me back when you need me. Bye Bye!")
        engine.stop()
        config.ai_assistant_running = False


def turn_assistant_on():
    """Called to restart the personal assistant"""
    global engine
    engine = pyttsx3.init(driverName='sapi5', debug=True)  # initialize the text-to-speech engine
    config.ai_assistant_running = True
    app.text_insert_assistant("\n Personal Assistant in On!\n")


if __name__ == '__main__':

    Loading_assistant_speech = "Loading personal assistant Kareem"
    speech = ["Tell me how can I help you?", "How can I help you?", "Can I help you?", "How can I assist you?"]

    app.text_insert_assistant(Loading_assistant_speech)
    print(Loading_assistant_speech)
    speak(Loading_assistant_speech)

    # run greeting function
    greeting()
    if config.ai_assistant_running: speak(random.choice(speech))

    while True:

        if config.ai_assistant_running:
            # check if the assistant should be restarted
            app.restart_personal_assistant()
            # Listen and take command from the user
            audio = takeCommand().lower()
            # take action and do what the user asks for
            digital_commands(audio)

        if app.assistant_mode:
            # restart the personal assistant
            turn_assistant_on()

# ___________________________________________________________________________________________________________
# Improvements:
# Done:
# 1. create a couple of lists with random.choice()
# 2. Create separate function for the commands
# 5. When the assistant is not capable of doing a command, it should tell the user so
# (meaning the program does not have that command listed)
# 7. Turn assistant off after some rounds when no reply is received
# shift print before speak command
# Text Widget not editable
# modify "start recording" button
# add how r u command
# auto scroll text widget till end

# Dev:
# fix error when exiting the app from gui
