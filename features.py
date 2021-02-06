import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import json

soundEngine = pyttsx3.init('sapi5')
listener = sr.Recognizer()
listener.pause_threshold=0.5
voices = soundEngine.getProperty('voices')
soundEngine.setProperty('voice',voices[1].id)

voices = soundEngine.getProperty('rate')
soundEngine.setProperty('rate',140)
chromeURL = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
calcVals = ['add','subtract','divide','multiply'] 

with open('json/openPaths.json') as op:
    openPath = json.load(op)
with open('json/folder.json') as fl:
    folders = json.load(fl)

class commandCenter:
    def __init__(self, query):
        
        if "wikipedia" in query:
            self.wiki(query)
        elif "open" in query:
            openCmd = list(query.split())[-1]
            self.openStuff(openCmd)
        elif any(x in query for x in calcVals):
            self.calc(query)
        elif 'exit' in query:
            exit()
        elif query == 'shutdown my system' or query == 'shut down my system':
            os.system("shutdown /s /t 1")
        elif query == 'restart my system':
            os.system("shutdown /r /t 1")
        elif 'install' in query or 'uninstall' in query:
            cmd=list(query.split())
            self.packages(cmd[0],cmd[-1]) 
        elif 'the time' in query:
            timeNow = "This is currently "+datetime.datetime.now().strftime("%H:%M")
            speak(timeNow)
        elif 'your name' in query:
            speak("My name is Korra")
            AskName()
        elif 'clear' in query:
            self.clear(list(query.split())[-1])
        else:
            speak("Currently in dev")

    def openStuff(self,openCmd):

        found=False
        for w in openPath['websites']:
            if w['name']==openCmd:
                 webbrowser.get(chromeURL).open(w['path'])
                 found=True
        if not found:
            for p in openPath['programs']:
                if p['name']==openCmd:
                    os.startfile(p['path'])
                    # found=True            
        
    def wiki(self,query):

        speak("Searching Wikipedia...")
        query = query.replace('wikipedia','')
        result = wikipedia.summary(query,sentences=2)
        speak('According to wikipedia..')
        speak(result)

    def clear(self,path):

        for d in folders["folders"]:
            if d['folder_name'] == path:
                semi_path = d['path']
                for p in os.listdir(semi_path):
                    full_path = os.path.join(semi_path,p)
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                
    def packages(self,cmd,pkg):

        cmd = "pip "+ cmd + " " + pkg
        os.system(cmd)

    def calc(self,query):

        result=""
        cmd=list(query.split())
        a=int(cmd[1])
        b=int(cmd[-1])
        if 'add' in query:
            result="Sum is "+str(a+b)
        elif 'substract' in query:
            result="Subracted result is "+str(b-a)
        elif 'divide' in query:
            try:
                result="Result is "+str(a/b)
            except ZeroDivisionError:
                speak('Currently out of scope!')
        elif 'multiply' in query:
            result="Multiplied result is "+str(a*b)
        speak(result)

def speak(voice):

    soundEngine.say(voice)
    soundEngine.runAndWait()

def takeCommand():

    try:
        with sr.Microphone() as src:
            voice = listener.listen(src)
            command = listener.recognize_google(voice)
        return command
    except sr.UnknownValueError:
        speak('Can\'t Interpret')   

def wishMe(name):

    greetTime = int(datetime.datetime.now().hour)
    greetWord=""
    try:   
        if greetTime>0 and greetTime<12:
            greetWord='Good Morning'+' '+name
        elif greetTime>=12 and greetTime<18:
            greetWord='Good Afternoon'+' '+name
        elif greetTime<24 and greetTime>=20:
            greetWord='Have Good Sleep after talk'+' '+name
        elif greetTime in [18,19]:
            greetWord='Good Evening'+' '+name
    except:
        greetWord='Have A Nice Day, Mister'
    speak(greetWord)

def AskName():
    speak('By the Way, What\'s Yours')
    name = "Ok, mister" + takeCommand() + " I'll try to remember your name"
    speak(name)
            