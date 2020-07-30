#!/usr/bin/env python3
import sys
import tkinter as tk
import time
from tkinter import filedialog

class Application(tk.Tk):
    def __init__(self, temps):
        tk.Tk.__init__(self)
        self.attributes("-type", "dialog")
        self.temps = temps
        self.put_widgets()

    def put_widgets(self):
        self.compte = tk.Label(self, text=format_time(self.temps))
        self.compte.pack()
        self.lancer = tk.Button(self, text="lancer", command=self.rebours)
        self.lancer.pack()
        self.quitter = tk.Button(self, text="Quitter", command=self.quit)
        self.quitter.pack()

    def rebours(self):
        if self.temps > 0:
            self.temps -= 1
            self.compte.configure(text=format_time(self.temps))
            self.after(1000, self.rebours)
        else:
            for x in range(10):
                print("C'est fini !!")
            self.quit()

        

def test_longueur():
    try:
        temps = int(sys.argv[1])
    except:
        print("format temps incorrect")
        sys.exit()
    if (temps < 0) or (temps > 240):
        print("temps incorrect")
        sys.exit()

def format_time(secondes):
    minutes = secondes // 60
    sec = secondes - 60*minutes
    if minutes < 10:
        minutes = "0" + str(minutes)
    if secondes < 10:
        secondes = "0" + str(secondes)
    return f"00:{minutes}:{secondes}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("PROBLEME")
        sys.exit()
    test_longueur()
    temps = int(sys.argv[1])
    app = Application(temps)
    app.title("Compte à rebours")
    app.temps = temps
    app.mainloop()
