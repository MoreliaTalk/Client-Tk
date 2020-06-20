import threading
# import random
import requests
from time import sleep
from tkinter import Tk
from tkinter import END
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter import Entry
from tkinter import Scrollbar
from tkinter import RIGHT
from tkinter import Y
from datetime import datetime


def update_messages():
    lasttimestamp = 0.0
    i = 1.0
    while True:
        response = requests.get("https://serverpocegram.pythonanywhere.com/get_messages",
                                params={"after": lasttimestamp}
                                )
        messages = response.json()["messages"]
        for message in messages:
            dt = datetime.fromtimestamp(message["timestamp"])
            dt = str(dt)[:-7]
            dt = dt[11:19]
            text.insert(i, "[" + dt + " " + message["username"] + "]\n")
            i += 1.0
            text.insert(i, message["text"] + "\n")
            i += 1.0
            lasttimestamp = message["timestamp"]
        sleep(1)


def send_message():
    url = "https://serverpocegram.pythonanywhere.com/send_message"
    text = e1.get()
    requests.get(url, json={
                            "username": elog.get(),
                            "password": epassw.get(),
                            "text": text
                            })
    e1.delete(0, END)


root = Tk()
root.geometry('420x600')

l1 = Label(text="Pocegram", font=("Comic Sans MS", 24, "bold"))
text = Text(width=49, height=30)
b1 = Button(text="Отправить", width=12,height=1)
e1 = Entry(width=49)
elog = Entry(width=20)
epassw = Entry(width=20)
scroll = Scrollbar(command=text.yview)
b1.config(command=send_message)

threadview = threading.Thread(target=update_messages)
threadview.start()

l1.pack()
elog.place(y=50, x=50)
epassw.place(y=50, x=230)
scroll.pack(side=RIGHT, fill=Y)
text.config(yscrollcommand=scroll.set)
b1.place(y=570, x=307)
e1.place(y=570, x=5)
text.place(x=5, y=80)
root.mainloop()
