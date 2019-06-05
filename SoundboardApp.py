import configparser
import easygui
from functools import partial
import os
from playsound import playsound
import sys
import tkinter as tk

class SoundboardApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Apply config settings
        self.conf_parser = configparser.ConfigParser()
        if os.path.exists("config.ini"):
            self.conf_parser.read("config.ini")
        else:
            self.conf_parser["settings"] = {}
        if "settings" not in self.conf_parser:
            self.conf_parser["settings"] = {}
        
        first_time = False

        self.sound_dir = self.conf_parser["settings"].get("sounddir")
        if self.sound_dir is None:
            first_time = True
            self.sound_dir = easygui.diropenbox(title="First Time Setup: Choose Sound File Directory")
            if self.sound_dir is None:
                sys.exit(1)

        self.bg_color = self.conf_parser["settings"].get("bgcolor")
        self.fg_color = self.conf_parser["settings"].get("fgcolor")
        if self.bg_color is None or self.fg_color is None:
            first_time = True
            resp = easygui.buttonbox("Choose a UI theme:",
                title="First Time Setup",
                choices=("Light", "Gray", "Dark")
            )
            if resp == "Dark":
                self.bg_color = "#454545"
                self.fg_color = "#DDDDDD"
            elif resp == "Gray":
                self.bg_color = "#777777"
                self.fg_color = "#222222"
            else:
                self.bg_color = "#DDDDDD"
                self.fg_color = "#222222"
        self.master.config(background=self.bg_color)
        self.config(background=self.bg_color)

        if "soundnames" not in self.conf_parser:
            self.conf_parser["soundnames"] = {}
        self.soundnames_dict = self.conf_parser["soundnames"]

        self.hotkeys = self.conf_parser["settings"].get("hotkeys")
        if self.hotkeys is None:
            first_time = True
            resp = easygui.ynbox("Do you wish to use default keyboard hotkeys?",
                title="First Time Setup"
            )
            if resp:
                self.hotkeys = "1 2 3 4 5 6 7 8 9 0 - = q w e r t y u i o p a s d f g h j k l z x c v b n m"
            else:
                self.hotkeys = "none"
        
        if first_time:
            easygui.msgbox("Configuration done! You can edit these preferences in "
                "config.ini or delete config.ini to use the first time setup again.",
                title="First Time Setup"
            )

        self.pack()
        self.create_widgets()

        # Apply more config settings
        window_width = self.conf_parser["settings"].get("windowwidth")
        window_height = self.conf_parser["settings"].get("windowheight")
        window_x = self.conf_parser["settings"].get("windowx")
        window_y = self.conf_parser["settings"].get("windowy")
        if (
            window_width is not None
            and window_height is not None
            and window_x is not None
            and window_y is not None
        ):
            self.master.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
            self.update_idletasks()

    def create_widgets(self):
        self.buttons = []
        # Create a button for every sound in the sounddir, sorted by filename.
        # Prefer user-specified names first, then actual filenames next
        soundfiles = os.listdir(self.sound_dir)
        soundnames = list(map(
            lambda fn: self.soundnames_dict.get(fn, fn), soundfiles
        ))
        btn_width = max(len(name) for name in soundnames)
        for soundname, soundfile in sorted(
            zip(soundnames, soundfiles), key=lambda x: x[0]
        ):
            button = tk.Button(self,
                text=soundname,
                bg=self.bg_color, fg=self.fg_color, width=btn_width,
                borderwidth=1, pady=5
            )
            button["command"] = partial(
                self.play_sound,
                os.path.join(self.sound_dir, soundfile)
            )
            self.buttons.append(button)
            button.pack(side="top", fill="both", expand=True)
        
        # Bind hotkeys to buttons' commands
        if self.hotkeys.lower() != "none":
            for btn, key in zip(self.buttons, self.hotkeys.split()):
                self.master.bind(key, btn["command"])
                btn["text"] += f" ({key.upper()})"

    def play_sound(self, filename):
        playsound(filename, block=False)
    
    def destroy(self):
        self.conf_parser["settings"]["sounddir"] = self.sound_dir
        self.conf_parser["settings"]["hotkeys"] = self.hotkeys
        self.conf_parser["settings"]["bgcolor"] = self.bg_color
        self.conf_parser["settings"]["fgcolor"] = self.fg_color
        self.conf_parser["settings"]["windowwidth"] = str(self.master.winfo_width())
        self.conf_parser["settings"]["windowheight"] = str(self.master.winfo_height())
        self.conf_parser["settings"]["windowx"] = str(self.master.winfo_x())
        self.conf_parser["settings"]["windowy"] = str(self.master.winfo_y())
        with open("config.ini", 'w') as f:
            self.conf_parser.write(f)
        super().destroy()