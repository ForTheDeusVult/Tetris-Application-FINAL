#imports
from tkinter import *
import tkinter as tk
import customtkinter as ctk

#Tutorial Frame Class
class TutorialFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        #initialises ctk.CTkFrame
        super().__init__(*args, **kwargs)

        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 2), weight=0)

        # Labels
        self.intro_label = ctk.CTkLabel(
            master=self,
            text="Tutorial!",
            font = ("Arial", 32, "bold"),
            width=50,
            height=40,
            corner_radius=8,
        )
        self.intro_label.pack(
            pady=(30,0),
            anchor=CENTER,
        )

        #Game Label
        self.game_label = ctk.CTkLabel(
            master=self,
            text="About Tetris:",
            width=50,
            height=30,
            font = ("Arial", 14, "bold")
        )
        self.game_label.pack(
            padx=15,
            pady=5,
            anchor=W,
        )

        #Description Label
        self.description_label = ctk.CTkTextbox(
            master=self,
            font = ("Arial", 14),
            width=550,
            height=180,
            corner_radius=8,
            # bg_color="#212529",
            fg_color="#343a40",
            wrap="word",
            spacing2=10,
        )
        
        #Description Label
        self.description_label.pack(
            padx=10,
            anchor=CENTER,
        )
        self.description_label.insert(
            0.0,
            """The aim of Tetris is simple - cause the falling blocks to fill each horizontal line by moving and rotating the pieces into place. With each line fully cleared, the row will vanished, and you will be awarded points for depending on how many lines you clear in one go! Every 10 lines cleared will increase the level, awarding more points per line cleared, but speeding up the game as a result. See how long you can play before the pieces reach the top and cause a game over! """,
        )

        # Tutorial Label
        self.tutorial_label = ctk.CTkLabel(
            master=self,
            text="Keybinds:",
            width=50,
            height=30,
            font = ("Arial", 14, "bold"),
        )
        self.tutorial_label.pack(
            padx=10,
            pady=(20, 10),
            anchor=W,
        )

        # Creating the keybinds Canvas
        self.controls_canvas = ctk.CTkCanvas(
            master=self,
            width=550,
            height=250,
            bg="#343a40",
            borderwidth=0,
            bd=0,
            highlightthickness=0,
        )
        self.controls_canvas.pack(anchor=CENTER)

        #Rotate Anticlockwise text
        self.controls_canvas.create_text(
            275,
            30,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'UP ARROW' or 'Z' key to rotate the piece anticlockwise!",
        )

        #Rotate Clockwise text
        self.controls_canvas.create_text(
            275,
            60,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'C' key to rotate the piece clockwise!",
        )

        # Soft Drop text
        self.controls_canvas.create_text(
            275,
            90,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'DOWN ARROW' key to soft drop the piece one block!",
        )
        
        # Hard Drop text
        self.controls_canvas.create_text(
            275,
            120,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'SPACE' key to hard drop the piece all the way down!",
        )

        #Move Right text
        self.controls_canvas.create_text(
            275,
            150,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'RIGHT ARROW' key to move the piece right!",
        )

        #Move Lest text
        self.controls_canvas.create_text(
            275,
            180,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'Left ARROW' key to move the piece left!",
        )

        #Pause text
        self.controls_canvas.create_text(
            275,
            210,
            fill="#f1f3f5",
            font = ("Arial", 12),
            text="Press the 'P' key to pause the game!",
        )