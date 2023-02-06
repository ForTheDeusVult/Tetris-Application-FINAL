#imports
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from TKObjects.frames.leaderboard_frame import LeaderboardFrame

#Leaderboard Screen Class
class LeaderboardScreen(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        #initialises CTkTopLevel
        super().__init__(*args, **kwargs)

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Screen properties
        self.title("Leaderboard!")
        self.geometry("650x700")
        self.config(
            padx=10,
            pady=10,
        )

        #disables resizing and interaction with other windows
        self.resizable(False, False)
        self.grab_set()

        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frames
        self.leaderboard_frame = LeaderboardFrame(self)
        self.leaderboard_frame.grid(
            row=0,
            column=0,
            rowspan=1,
            columnspan=1,
            sticky="nsew",
        )
