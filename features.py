import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import json
from googlesearch import search
from tkinter import Radiobutton, Frame, Tk, LEFT, StringVar, Label, Entry, Button
from newscollector import scrappedData

soundEngine = pyttsx3.init('sapi5')
listener = sr.Recognizer()
listener.pause_threshold = 0.5
voices = soundEngine.getProperty('voices')
soundEngine.setProperty('voice', voices[1].id)

voices = soundEngine.getProperty('rate')
soundEngine.setProperty('rate', 140)
chromeURL = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
calcVals = ['add', 'subtract', 'divide', 'multiply']

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
            cmd = list(query.split())
            self.packages(cmd[0], cmd[-1])
        elif 'the time' in query:
            timeNow = "This is currently "+datetime.datetime.now().strftime("%H:%M")
            speak(timeNow)
        elif 'your name' in query:
            speak("My name is Korra")
            AskName()
        elif 'clear' in query:
            self.clear(list(query.split())[-1])
        elif 'search for' in query:
            query = query.replace('search for', '')
            self.find(query)
        elif 'grab some news' in query:
            speak("Please Wait...")
            scrappedData("https://currentaffairs.studyiq.com/daily/",
                         datetime.datetime.today().date())
            speak("Extraction Completed")
            os.startfile(os.path.realpath("StudyIQ"))
        else:
            speak("Currently in dev")

    def openStuff(self, openCmd):

        found = False
        for w in openPath['websites']:
            if w['name'] == openCmd:
                webbrowser.get(chromeURL).open(w['path'])
                found = True
        if not found:
            for p in openPath['programs']:
                if p['name'] == openCmd:
                    os.startfile(p['path'])
                    found = True
        if not found:
            for f in folders['folders']:
                if f['folder_name'] == openCmd:
                    os.startfile(os.path.realpath(f['path']))
                    found = True
        if not found:
            speak('Currently Not Known, Would you like to add Sir')
            self.pathAsk()

    def pathAsk(self):

        root = Tk()
        var = StringVar()

        def AppendPath():
            pathType = var.get()
            name = str(Name_Entry.get()).lower()
            path = str(Path_Entry.get())
            if pathType == 'websites':
                openPath[pathType].append({"name": name, "path": path})
                with open('json/openPaths.json', 'w') as add_website:
                    json.dump(openPath, add_website, indent=4)
            elif pathType == 'programs':
                openPath[pathType].append({"name": name, "path": path})
                with open('json/openPaths.json', 'w') as add_program:
                    json.dump(openPath, add_program, indent=4)
            elif var.get() == 'folders':
                folders[var.get()].append({"folder_name": name, "path": path})
                with open('json/folders.json', 'w') as add_folder:
                    json.dump(folders, add_folder, indent=4)
            root.quit()

        root.title("Add path")
        root.geometry('400x130')
        radio_btn = Frame(root)
        radio_btn.pack()

        website = Radiobutton(radio_btn, text="Website",
                              variable=var, value='websites')
        website.pack(side=LEFT)
        program = Radiobutton(radio_btn, text="Program",
                              variable=var, value='programs')
        program.pack(side=LEFT)
        folder = Radiobutton(radio_btn, text="Folder",
                             variable=var, value='folders')
        folder.pack(side=LEFT)

        path = Frame(root)
        path.pack()

        Name = Label(path, text="Name : ")
        Name.grid(row=0, column=0)
        Name_Entry = Entry(path, width=50)
        Name_Entry.grid(row=0, column=1, pady=10)
        Path = Label(path, text="Path : ")
        Path.grid(row=1, column=0)
        Path_Entry = Entry(path, width=50)
        Path_Entry.grid(row=1, column=1, pady=10)

        Submit = Frame(root)
        Submit.pack()

        sub_btn = Button(Submit, text="Submit", command=AppendPath)
        sub_btn.pack()

        root.mainloop()

    def wiki(self, query):

        speak("Searching Wikipedia...")
        query = query.replace('wikipedia', '')
        result = wikipedia.summary(query, sentences=2)
        speak('According to wikipedia..')
        speak(result)

    def clear(self, path):

        for d in folders["folders"]:
            if d['folder_name'] == path:
                semi_path = d['path']
                for p in os.listdir(semi_path):
                    full_path = os.path.join(semi_path, p)
                    if os.path.isfile(full_path):
                        os.remove(full_path)

    def packages(self, cmd, pkg):

        if cmd == 'install':
            cmd = "pip " + cmd + " " + pkg
        elif cmd == 'uninstall':
            cmd = "pip " + cmd + " -y " + pkg
        os.system(cmd)

    def calc(self, query):

        result = ""
        cmd = list(query.split())
        a = int(cmd[1])
        b = int(cmd[-1])
        if 'add' in query:
            result = "Sum is "+str(a+b)
        elif 'substract' in query:
            result = "Subracted result is "+str(b-a)
        elif 'divide' in query:
            try:
                result = "Result is "+str(a/b)
            except ZeroDivisionError:
                speak('Currently out of scope!')
        elif 'multiply' in query:
            result = "Multiplied result is "+str(a*b)
        speak(result)

    def find(self, query):
        for s in search(query, tld="co.in", num=1, stop=1, pause=2):
            webbrowser.get(chromeURL).open(str(s))


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
    greetWord = ""
    try:
        if greetTime > 0 and greetTime < 12:
            greetWord = 'Good Morning'+' '+name
        elif greetTime >= 12 and greetTime < 18:
            greetWord = 'Good Afternoon'+' '+name
        elif greetTime < 24 and greetTime >= 20:
            greetWord = 'Have Good Sleep after talk'+' '+name
        elif greetTime in [18, 19]:
            greetWord = 'Good Evening'+' '+name
    except:
        greetWord = 'Have A Nice Day, Mister'
    speak(greetWord)


def AskName():
    speak('By the Way, What\'s Yours')
    name = "Ok, mister" + takeCommand() + " I'll try to remember your name"
    speak(name)
