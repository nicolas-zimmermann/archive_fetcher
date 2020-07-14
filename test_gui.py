import tkinter as tk
from tkinter import filedialog

class Application(tk.Tk):
    """Tiny window using tkinter in a OOP fashion"""
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes("-type", "dialog")
        self.mettre_widgets()

    def mettre_widgets(self):
        """Pour creer et mettre les widgets dans le bazard"""
        self.url = tk.Entry(self, text="url :")
        self.url.pack()
        self.bouton = tk.Button(self, text="Download",
                                command=self.get_content)
        self.bouton.pack()
        self.explore = tk.Button(self, text="explore", command=self.browse_files)
        self.explore.pack()

    def get_content(self):
        print(self.url.get())

    def browse_files(self):
        filename = filedialog.askdirectory(title="Select a directory")
        print(filename)
    

if __name__ == "__main__":
    app = Application()
    app.title("Archive Fetcher")
    app.mainloop()
