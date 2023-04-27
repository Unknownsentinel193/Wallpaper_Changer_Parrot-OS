import tkinter as tk
from tkinter import filedialog
import os
import random
import time
import platform
import subprocess

class WallpaperChangerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wallpaper Changer")

        self.folder_path = tk.StringVar()
        self.current_wallpaper = None
        self.run_wallpaper_changer = False

        self.folder_label = tk.Label(master, text="Wallpaper Folder")
        self.folder_label.pack()

        self.folder_entry = tk.Entry(master, textvariable=self.folder_path)
        self.folder_entry.pack()

        self.folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.folder_button.pack()

        self.load_button = tk.Button(master, text="Load Wallpapers", command=self.load_wallpapers)
        self.load_button.pack()

        self.start_button = tk.Button(master, text="Start Wallpaper Changer", command=self.start_wallpaper_changer)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Wallpaper Changer", command=self.stop_wallpaper_changer, state=tk.DISABLED)
        self.stop_button.pack()

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)

    def load_wallpapers(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            return
        self.wallpapers = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        self.show_wallpaper()

    def show_wallpaper(self):
        if self.run_wallpaper_changer:
            self.current_wallpaper = random.choice(self.wallpapers)
            if platform.system() == 'Windows':
                ctypes.windll.user32.SystemParametersInfoW(20, 0, self.current_wallpaper, 0)
            elif platform.system() == 'Darwin':
                subprocess.run(['osascript', '-e', f'set theDesktops to {{1, 2}}\nrepeat with aDesktop in theDesktops\n\ttell desktop aDesktop\n\t\tset picture to "{self.current_wallpaper}"\n\tend tell\nend repeat\n'])
            else:
                subprocess.run(['dconf', 'write', '/org/mate/desktop/background/picture-filename', f"'{self.current_wallpaper}'"])
            self.master.after(10000, self.show_wallpaper)

    def start_wallpaper_changer(self):
        self.load_wallpapers()
        self.run_wallpaper_changer = True
        self.start_button.config(state=tk.DISABLED)
        self.folder_entry.config(state=tk.DISABLED)
        self.folder_button.config(state=tk.DISABLED)
        self.load_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.wallpaper_changer()

    def stop_wallpaper_changer(self):
        self.run_wallpaper_changer = False
        self.start_button.config(state=tk.NORMAL)
        self.folder_entry.config(state=tk.NORMAL)
        self.folder_button.config(state=tk.NORMAL)
        self.load_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def wallpaper_changer(self):
        self.show_wallpaper()

if __name__ == '__main__':
    root = tk.Tk()
    app = WallpaperChangerGUI(root)
    root.mainloop()
