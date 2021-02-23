from tkinter import *
from tkinter.ttk import *
import threading
import time

# root = Tk()
# txttxt = Text(root).grid(row=1, column=1, sticky=W + E, padx=20, pady=20)


# insert(Tk.End, "Hi")
class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.root = None
        self.txt = None

    def configure_root(self):

        self.root.title("Personal Assistant GUI")
        self.root.rowconfigure(0, minsize=100, weight=1)
        self.root.columnconfigure(1, minsize=100, weight=1)
        # self.root.geometry("")
        self.root.iconbitmap(r"images\robot_icon.png")
        # self.root.resizable(width=FALSE, height=FALSE)

    def create_widgets(self):
        Label(self.root, text='Personal Assistant', anchor=CENTER).grid(row=0, columnspan=2)
        Button(self.root, text='Start Recording', cursor='hand2').grid(row=1, column=0,
                                                                       sticky=W + E)  # , image=mic_image
        self.txt = Text(self.root)
        self.txt.grid(row=1, column=1, sticky=W + E, padx=20, pady=20)
        print('App create widgets')

    def callback(self):
        self.root.quit()

    def run(self):
        import time
        self.root = Tk()
        self.configure_root()
        Label(self.root, text='Personal Assistant', anchor=CENTER).grid(row=0, columnspan=2)
        Button(self.root, text='Start Recording', cursor='hand2').grid(row=1, column=0,
                                                                       sticky=W + E)  # , image=mic_image
        self.txt = Text(self.root)
        self.txt.grid(row=1, column=1, sticky=W + E, padx=20, pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

    def run_app_with_code(self):
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

    def text_insert(self, text_input):
        self.txt.insert(END, text_input)



# def text_insert(text_input):
#     app.txt.insert(Tk.END, text_input)


# create obj for App class to init the gui
# app = App()


if __name__ == "__main__":
    app = App()
    # time.sleep(2)
    app.text_insert("Hi")
    # mainloop()
