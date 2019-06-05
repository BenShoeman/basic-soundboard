import os
import tkinter as tk
from SoundboardApp import SoundboardApp

root = tk.Tk()
root.title("Basic Soundboard")
root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
app = SoundboardApp(master=root)
app.pack(fill="both", expand=True)

# Hack to get it to start on top
root.lift()
root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", False)

app.mainloop()