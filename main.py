import threading
import json
import asyncio
import aiohttp
from time import sleep
from tkinter import *
from tkinter import scrolledtext 
from datetime import datetime
from tkinter import messagebox as mb

ws = None

async def update_mes():
    global a
    global ws
    i = 1.0
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://localhost:8000/ws') as ws:
            async for not_json_msg in ws:
                message = not_json_msg.json()
                if message["mode"] == "message":
                    text.config(state=NORMAL)
                    dt = datetime.fromtimestamp(message["timestamp"])
                    dt = str(dt)[:-7]
                    dt = dt[11:19]
                    text.insert(i, "[" + dt + " " + message["username"] + "]\n")
                    i += 1.0
                    text.insert(i, message["text"] + "\n")
                    i += 1.0
                    text.insert(i, "\n ")
                    i += 1.0
                    text.config(state=DISABLED)
                elif message["mode"] == "reg":
                    if message["status"]=="true":
                        mes_box_reg_info(True,"Успешный вход!")
                        a = True
                    elif message["status"]=="false":
                        mes_box_reg_info(False,"Неправильный пароль! Повторите попытку")
                        a = False
                    elif message["status"]=="newreg":
                        mes_box_reg_info(True,"Успешная регистрация!")
                        a = True

async def send_message():
    if a == True:
        message = json.dumps({
                                                "mode": "message",
                                                "username": elog.get(),
                                                "text": e1.get()
                                                })
        await ws.send_str(message)
        e1.delete(0, END)
    else:
        mb.showerror("Уведомление","Сначала авторизуйся!")


async def reg_user():
    message = json.dumps({
                                            "mode": "reg",
                                            "username": elog.get(),
                                            "password": epassw.get()
                                            })
    await ws.send_str(message)

def mes_box_reg_info(error,text):
    if error == False:
        mb.showerror("Уведомление",text)
    else:
        mb.showinfo("Уведомление",text)

root = Tk()
root.geometry('420x600')

l1 = Label(text="MoreliaTalk", font=("Comic Sans MS", 24, "bold"))
text = scrolledtext.ScrolledText(width=49, height=30,state=DISABLED)
b1 = Button(text="Отправить", width=12, height=1)
e1 = Entry(width=49)

elog = Entry(width=20)
epassw = Entry(width=20)
b_send_userdata = Button(text="Авторизоваться", width=12)
b_send_userdata.config(command=lambda:asyncio.run(reg_user()))

b1.config(command=lambda:asyncio.run(send_message()))
l1.pack()

elog.place(y=50, x=20)
epassw.place(y=50, x=160)
b_send_userdata.place(y=50, x=300)

b1.place(y=570, x=307)
e1.place(y=570, x=5)
text.place(x=5, y=80)

t = threading.Thread(target=lambda:asyncio.run(update_mes()))

t.start()
root.mainloop()

