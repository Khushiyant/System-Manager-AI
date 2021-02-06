import features as fs
from tkinter import *

class interactiveUI:
    def __init__(self,master,screen_height,screen_width,photo):
        
        self.listen = Button(master,command=self.commander,image=photo,borderwidth=0,activebackground='cyan')
        self.listen.pack()

    def commander(self):
        fs.speak("How may I help you")
        try:
            query = fs.takeCommand()
            query=query.lower()
            fs.commandCenter(query)
        except AttributeError:
            pass 

if __name__ == '__main__':    
    fs.wishMe("Khushiyant")
    root=Tk()
    photo = PhotoImage(file = "D:/Projects/Python/My_Alexa/img/voice.png")
    screen_height=root.winfo_height()
    screen_width=root.winfo_width()
    interactiveUI(root,screen_height,screen_width,photo)
    root.mainloop()

        
