#!/usr/bin/python

#  Simple Hackable Pomodoro Timer
#  ===============================

#  Author: [Dmitry](http://dmi3.net) [Source](https://github.com/dmi3/bin)

#  Requirements
#  ------------
#  1. On Linux and Mac install package `python-tk`
#  2. pip install requests

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import time
import datetime
import os
import requests

API_TOKEN = '' # https://habitica.com/#/options/settings/api
USER_ID = '' # https://habitica.com/#/options/settings/api
TASK_ID = ''


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_attributes("-topmost", 1) # always on top
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(data="R0lGODlhIAAgAOMIAAAAAHkAAJcDALUhBgBlANM/JAChAPFdQv///////////////////////////////yH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAgALAAAAAAgACAAAASwEMlJq704622BB0ZofKDIUaQ4fuo5pSIcupK8eu1GkkM/EEDC7oMZeny/oBFQNCKDQmNz+FRKX5+D9lDoFlRIsG+55XrFPfSAvPV+RWH42Fh2q9VLN3LPHwj+AnlefYR+gIJdhX2AgUZ6inuMS5CGjH8BmAGTkJaAmZpOnJ0Cn5uKo6SZJCgfSKilRBc8Pq+qsR2ttKOwHlMArru2vTpLVy7FxifIQzQIyzvN0dLTEhEAOw=="))
        self.label = tk.Label(font=("Helvetica Neue", 44))
        self.label.pack()

        self.buttons = tk.Frame(self.root)
        self.buttons.pack()
        tk.Button(self.buttons, text ="Start", command=lambda: self.start()).pack(side=tk.LEFT)
        tk.Button(self.buttons, text ="Cancel", command=lambda: self.cancel()).pack(side=tk.LEFT)

        self.end = time.time()
        self.started = False

        self.update_clock()
        self.root.mainloop()

    def start(self):
        self.started = True
        self.end = time.time() + datetime.timedelta(minutes=25).total_seconds()

        print("start")

    def cancel(self):
        self.started = False
        self.end = time.time()

        print("canceled")
        requests.post('https://habitica.com/api/v3/tasks/'+TASK_ID+'/score/down', headers={'x-api-key': API_TOKEN, 'x-api-user': USER_ID})

    def complete(self):
        self.started = False

        print("completed")
        requests.post('https://habitica.com/api/v3/tasks/'+TASK_ID+'/score/up', headers={'x-api-key': API_TOKEN, 'x-api-user': USER_ID})

    def update_clock(self):
        delta = self.end - time.time()
        if delta<0:
            self.label.configure(text="00:00", bg="#d9d9d9")
            self.root.wm_title("Pomodoro")
            if self.started:
                self.complete()
        else:
            time_left = datetime.datetime.fromtimestamp(delta).strftime("%M:%S")
            self.root.wm_title("(%s) Pomodoro" % time_left)
            self.label.configure(text=time_left, bg="#ca1616")
        self.root.after(1000, self.update_clock)

app=App()
