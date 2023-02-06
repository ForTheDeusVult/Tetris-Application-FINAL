#imports
from tkinter import messagebox
from customtkinter import *
import customtkinter as ctk
import sqlite3
from misc.app_vars import (
    CANVAS_NAME_XAXIS,
    CANVAS_SCORE_XAXIS,
    CANVAS_TIME_XAXIS,
    ALL_CANVAS_YAXIS,
)

#LeaderboardFrame Class
class LeaderboardFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        #initialises CTkFrame
        super().__init__(*args, **kwargs)

        #Grid configuration
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        # Canvas properties
        self.canvas_width = 500
        self.canvas_height = 500

        # Labels
        self.intro_label = ctk.CTkLabel(
            master=self,
            text="Leaderboard",
            width=50,
            height=30,
            font = ("Arial", 24, "bold")
        )
        self.intro_label.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=20,
            sticky="nsew",
        )

        #Search button properties
        self.search_button = ctk.CTkButton(
            master=self, 
            text="Search", 
            width = 10,
            height = 30,
            font = ("Arial", 14, "bold"),
            border_width=0,
            corner_radius=8,
            hover=True,
            command=self.search,
        )

        self.search_button.grid(
            row=1,
            column=0,
            columnspan=1,
            padx=165,
            pady=10,
            sticky="w",
        )

        #Username Entry Field properties
        self.username_entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=28,
            corner_radius=7,
            border_width=2,
            placeholder_text="username"
        )

        self.username_entry.grid(
            row=1,
            column=0,
            columnspan=1,
            padx=(15, 120),
            pady=6, 
            sticky="e"
            )

        # Creating the Canvas
        self.main_canvas = ctk.CTkCanvas(
            master=self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#343a40",
            borderwidth=0,
            bd=0,
            highlightthickness=0,
        )

        # Displaying text on the Canvas
        self.main_canvas.create_text(
            100,
            50,
            fill="#f1f3f5",
            font = ("Arial", 10, "bold"),
            text="Name",
        )

        self.main_canvas.create_text(
            300,
            50,
            fill="#f1f3f5",
            font = ("Arial", 10, "bold"),
            text="Score",
        )

        self.main_canvas.create_text(
            500,
            50,
            fill="#f1f3f5",
            font = ("Arial", 10, "bold"),
            text="Time",
        )

        self.main_canvas.grid(
            row=2,
            column=0,
            rowspan=3,
            columnspan=3,
            padx=15,
            pady=10,
            sticky="nsew",
        )



        # Drawing lines on the Canvas
        self.main_canvas.create_line(
            200,
            70,
            200,
            470,
            fill="#f1f3f5",
        )

        self.main_canvas.create_line(
            400,
            70,
            400,
            470,
            fill="#f1f3f5",
        )

        self.display_LD_data()
    
    #Returns and Displays Leaderboard data
    def display_LD_data(self):
        try:
            # Connect to the database
            connection = sqlite3.connect("data/app_data.db")
            # Create the cursor
            cur = connection.cursor()

            #Checks and returns top 10 users ordered by highscore
            cur.execute("""
            SELECT user_data.username, game_data.highscore, game_data.time
            FROM user_data, game_data
            WHERE user_data.user_id = game_data.user_id
            ORDER BY highscore DESC
            LIMIT 10"""
            )

            all_game_data = cur.fetchall()

            #displays leaderboard data
            data_yaxis = ALL_CANVAS_YAXIS
            for game_data in all_game_data:
                data_yaxis += 40
                self.main_canvas.create_text(
                    CANVAS_NAME_XAXIS,
                    data_yaxis,
                    fill="#f1f3f5",
                    font = ("Arial", 10, "bold"),
                    text=game_data[0],
                )

                self.main_canvas.create_text(
                    CANVAS_SCORE_XAXIS,
                    data_yaxis,
                    fill="#f1f3f5",
                    font = ("Arial", 10, "bold"),
                    text=game_data[1],
                )

                self.main_canvas.create_text(
                    CANVAS_TIME_XAXIS,
                    data_yaxis,
                    fill="#f1f3f5",
                    font = ("Arial", 10, "bold"),
                    text=game_data[2],
                )

            # Commiting the changes
            connection.commit()
            # Close our connnection
            connection.close()
        except sqlite3.OperationalError or sqlite3.ProgrammingError:
            #
            messagebox.showerror(
                title="Database Error",
                message="Database Error has occured. Please try again.",
            )

    #searches for user
    def search(self):
        #gets username from user entry field
        username_entered = self.username_entry.get()
        #connects to database
        connection = sqlite3.connect("data/app_data.db")
        #creates the cursor
        cur = connection.cursor()

        #checks for instances of the searched username inside the database
        cur.execute("""
        SELECT COUNT(*)
        FROM user_data
        WHERE username = ?""",
        (username_entered,))

        #Set to True if the username was found
        existed_user = cur.fetchone()[0] > 0

        if existed_user:

            #Checks and Returns users game data (null if data not found)
            cur.execute("""
            SELECT user_data.username, game_data.highscore, game_data.time
            FROM user_data, game_data
            WHERE user_data.user_id = game_data.user_id
            AND user_data.username =?""",
            (username_entered,)
            )

            user = cur.fetchone()
            #True if data is found, False otherwise

            if user:

                #displays searched users results
                #creates a new window
                self.result_screen = ctk.CTkToplevel(self)

                #screen properties
                self.result_screen.title("User found!")
                self.result_screen.geometry("250x190")
                self.result_screen.config(padx=10, pady=10)
                self.result_screen.resizable(False, False)

                #frame properties
                result_frame = ctk.CTkFrame(
                    master = self.result_screen
                    )

                result_frame.grid_rowconfigure((0,1), weight = 1)
                result_frame.grid_columnconfigure((0,2), weight = 1)

                #heading label config
                self.intro_label = ctk.CTkLabel(
                    master = result_frame,
                    text = str(user[0]),
                    width=230,
                    height=30,
                    font = ("Arcadia", 25, "bold")
                )

                self.intro_label.pack(anchor = ctk.CENTER, pady = 30)

                #score label config
                self.score_label = ctk.CTkLabel(
                    master = result_frame,
                    text = ("Score:",user[1]),
                    width = 230,
                    height = 30,
                    font = ("Arcadia", 14 ,"bold")
                    )

                self.score_label.pack(anchor = ctk.CENTER, pady = 0)
                self.date_label = ctk.CTkLabel(
                    master = result_frame,
                    text = ("Time: "+str(user[2])),
                    width = 230,
                    height = 30,
                    font = ("Arcadia", 14, "bold")
                    )

                #date label config
                self.date_label.pack(anchor = ctk.CENTER, pady = (0, 20))

                result_frame.grid(
                row=0,
                column=0,
                rowspan=1,
                columnspan=1,
                sticky="nsew",
            )
                #commits changes to database
                connection.commit()
                #closes connection
                connection.close()
            else:
                #displays 'Score data not found' message
                messagebox.showerror(
                    title="Score not found!",
                    message="The user does not have a saved score.",
                )
                #commits changes to database
                connection.commit()
                #closes connection
                connection.close()

        else:
            #displays 'User not found' message
            messagebox.showerror(
                title="User not found!",
                message="The user does not exist!",
            )
            #commits changes to database
            connection.commit()
            #closes connection
            connection.close()




