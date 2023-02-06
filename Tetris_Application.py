#imports
import customtkinter as ctk
import sqlite3, hashlib
from customtkinter import *
from tkinter import messagebox
from pathlib import Path
from misc.app_vars import CYPHER_SALT
from misc.hash_user import *
from misc.input_validation import *
from just_playback import Playback
from tetris_game.Tetris_Game import TetrisGame
from tetris_game.file_manager import create_database
from TKObjects.screens.leaderboard_screen import LeaderboardScreen
from TKObjects.screens.tutorial_screen import TutorialScreen
from music.music_file_generator import create_files
from music.music_file_generator import get_files

#Main App Class
class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        #initliases CTk
        super().__init__(*args, **kwargs)

        self.logged_in = False
        self.logged_in_username = ""

        #plays menu music
        self.playback = Playback()
        self.playback.load_file('music/music files/Menu.mp3')
        self.playback.loop_at_end(True)
        self.playback.play()

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Screen properties
        self.title("Tetris")
        self.geometry("480x380")
        self.resizable(False, False)

        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frames
        self.main_frame = ctk.CTkFrame(
            master=self,
        )
        self.main_frame.grid_rowconfigure((0, 7), weight=1)
        self.main_frame.grid_columnconfigure((0, 2), weight=1)

        # Labels
        self.logged_in_label = ctk.CTkLabel(
            master=self.main_frame,
            text="Logged in as:",
            width=40,
            height=20,
        )
        self.logged_in_label.grid(
            row=5,
            column=0,
            padx=20,
            sticky="nsew",
        )

        self.logged_in_username_label = ctk.CTkLabel(
            master=self.main_frame,
            text="",
            font = ("Arial", 14, "bold"),
            width=40,
            height=25,
        )
        self.logged_in_username_label.grid(
            row=6,
            column=0,
            pady = 0,
            sticky="nsew",
        )

        self.title_label = ctk.CTkLabel(
            master=self.main_frame,
            text="TETRIS!",
            width=40,
            height=30,
            corner_radius=8,
            font = ("Arial", 40, "bold")
        )
        self.title_label.grid(
            row=0,
            column=1,
            pady=(40, 20),
        )

        # Buttons
        self.play_button = ctk.CTkButton(
            master=self.main_frame,
            text="Play!",
            width=40,
            height=25,
            font = ("Arial", 14, "bold"),
            border_width=0,
            corner_radius=7,
            hover=True,
            command=self.play_game,
        )
        self.play_button.grid(
            row=1,
            column=1,
            padx=0,
            pady=10,
            sticky="nsew",
        )

        self.leader_board_button = ctk.CTkButton(
            master=self.main_frame,
            text="Leaderboard",
            width=40,
            height=25,
            font = ("Arial", 14, "bold"),
            border_width=0,
            corner_radius=7,
            hover=True,
            command=self.display_LD,
        )
        self.leader_board_button.grid(
            row=2,
            column=1,
            padx=0,
            pady=10,
            sticky="nsew",
        )

        self.tutorial_button = ctk.CTkButton(
            master=self.main_frame,
            text="Tutorial",
            width=40,
            height=25,
            font = ("Arial", 14, "bold"),
            border_width=0,
            corner_radius=7,
            hover=True,
            command=self.display_tutorial
        )
        self.tutorial_button.grid(
            row=3,
            column=1,
            padx=0,
            pady=10,
            sticky="nsew",
        )

        self.register_button = ctk.CTkButton(
            master=self.main_frame,
            text="Register",
            width=40,
            height=25,
            font = ("Arial", 12, "bold"),
            fg_color="#495057",
            corner_radius=7,
            hover=True,
            hover_color="#343a40",
            command=self.display_register,
        )
        self.register_button.grid(
            row=4,
            column=2,
            padx=20,
            pady=(10, 0),
            sticky="nsew",
        )

        self.login_button = ctk.CTkButton(
            master=self.main_frame,
            text="Login",
            width=40,
            height=25,
            font = ("Arial", 12, "bold"),
            border_width=0,
            corner_radius=7,
            hover=True,
            command=self.display_login,
        )
        self.login_button.grid(
            row=5,
            column=2,
            pady=10,
            padx=20,
            sticky="nsew",
        )

        self.logout_button = ctk.CTkButton(
            master=self.main_frame,
            text="Logout",
            width=40,
            height=25,
            font = ("Arial", 12, "bold"),
            border_width=0,
            corner_radius=7,
            hover=True,
            command=self.log_out,
        )
        self.logout_button.grid(
            row=6,
            column=2,
            pady = 0,
            padx=20,
            sticky="nsew",
        )

        #Option menu config
        self.music_choice = ctk.StringVar(value = "Track 1")
        self.music_menu = ctk.CTkOptionMenu(
            master = self.main_frame,
            values = ["Track 1","Track 2","Track 3","Track 4", "Track 5", "Track 6", "None"],
            font = ("Arial", 12, "bold"),
            corner_radius=7,
            width = 100,
            height = 20,
            dropdown_fg_color = "#495057",
            dropdown_hover_color = "#343a40",
            variable = self.music_choice, #updates self.music_choice depending on which option is clicked
            hover=True,
            anchor = "center",
            )
        
        self.music_menu.grid(
            row=0,
            column=0,
            columnspan = 1,
            pady = 10,
            padx = 10,
            sticky="n, nw, ne",
        )

        self.main_frame.grid(
            row=0,
            column=0,
            columnspan=4,
            rowspan=7,
            padx=10,
            pady=10,
            sticky="nsew",
        )

    #Logs user out 
    def log_out(self):
        if self.logged_in:
            self.logged_in_username = ""
            self.update_data(False, self.logged_in_username)
            messagebox.showinfo(title="Logout successful!", message="You have logged out successfully!")
        #displays error if no user is logged in
        else:
            messagebox.showinfo(title="Logout error", message="No user is logged in!")

    def check_user_existence(self, username_entered):
        try:
            # Connect to database
            connection = sqlite3.connect("data/app_data.db")
            # Create the cursor
            cur = connection.cursor()

            #check and return the number of instances of the username from user_data table
            cur.execute(
                "SELECT COUNT(*) FROM user_data WHERE username=?", (username_entered,)
            )

            #False if user is not found, True otherwise
            existed_user = cur.fetchone()[0] > 0

            # Commit Changes
            connection.commit()
            # Close connection
            connection.close()
            return existed_user
        #returns if an error occurs while interacting with the database
        except sqlite3.OperationalError or sqlite3.ProgrammingError:
            return False


    def add_user(self, username_entered, password_entered):

        # Prepare the password to store it in the database
        encoded_password = password_entered.encode()
        hashed_password = hashlib.sha256(encoded_password + CYPHER_SALT).hexdigest()

        #Hashes username to form user_id
        new_user_id = hash_user(username_entered)

        # Connect to database
        connection = sqlite3.connect("data/app_data.db")
        # Create the cursor
        cur = connection.cursor()

        #checks if new_user_id already exists
        collision = True
        while collision:
            cur.execute(
                    "SELECT COUNT(*) FROM user_data WHERE user_id=?", (new_user_id,)
                )
            if cur.fetchone()[0] > 0:
               new_user_id += 1 #corrects collision
            else:
                collision = False
        
        #inserts data
        cur.execute(
            "INSERT INTO user_data (user_id, username, password) VALUES (?, ?, ?)",
            (new_user_id, username_entered, hashed_password),
        )

        # Commit Changes
        connection.commit()

        # Close connection
        connection.close()

        self.update_data(True, username_entered)
        self.register_screen.destroy()
        messagebox.showinfo(
            title="Registered", message="You have registered successfully!"
        )

    #checks the users inputs for registration
    def check_register(self):
        #gets inputs from entry fields
        username_entered = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        #runs a series of validation checks for existing usernames, username/password length etc

        if input_validate(username_entered, "username") == "empty":
            messagebox.showerror(
                title="Registration Error",
                message="Username box empty. Please enter a username.",
            )

        elif input_validate(username_entered, "username") == "out of range":
            messagebox.showerror(
                title="Registration Error",
                message="Username is either too long or too short. Please enter a username between 4 and 15 characters.",
            )

        elif self.check_user_existence(username_entered):
            messagebox.showerror(
                title="Registration Error",
                message="The username is already taken. Please enter a new username.",
            )

        elif input_validate(password, "password") == "empty":
            messagebox.showerror(
                title="Registration Error",
                message="Password box empty. Please enter a password.",
            )

        elif input_validate(password, "password") == "invalid":
            messagebox.showerror(
                title="Registration Error",
                message="Password is invalid. Please enter a different password.",
            )
        elif input_validate(password, "password") == "out of range":
            messagebox.showerror(
                title="Registration Error",
                message="Password is either too long or too short. Please enter a password between 7 and 15 characters.",
            )

        elif confirm_password != password:
            messagebox.showerror(
                title="Registration Error",
                message="The entered passwords do not match. Please try again.",
            )
        else:
            self.add_user(username_entered, password)

    #checks login data vs data in user_data table
    def check_user_data(self, username_entered, password_entered):
        try:
            # Create connection to the database
            connection = sqlite3.connect("data/app_data.db")
            # Create the cursor
            cur = connection.cursor()

            cur.execute(
                "SELECT password FROM user_data WHERE username=?",
                (username_entered,),
            )

            #hashes user input password and checks vs hashed password in database
            try:
                hashed_user_password = cur.fetchone()[0]
                if (
                    hashed_user_password
                    and hashlib.sha256(
                        password_entered.encode() + CYPHER_SALT
                    ).hexdigest()
                    == hashed_user_password
                ):
                    return True
            except TypeError:
                return False
        except sqlite3.OperationalError or sqlite3.ProgrammingError:
            return False

    #attempts user login
    def login(self):
        #gets inputs from entry fields
        username_entered = self.username_entry.get()
        password_entered = self.password_entry.get()

        if self.check_user_data(username_entered, password_entered):
            self.update_data(True, username_entered)
            self.login_screen.destroy()
            messagebox.showinfo(title="Login successful!", message="You have signed in!")

        else:
            messagebox.showerror(
                title="Login Error",
                message="The username or password you have entered is incorrect. Please try again.",
            )

    #updates onscreen login data + login status within the code
    def update_data(self, bool, current_username):
        self.logged_in = bool
        self.logged_in_username = current_username
        self.logged_in_username_label.configure(text=self.logged_in_username)

    #play game function
    def play_game(self):
        #pauses menu music
        self.playback.pause()

        #gets music list for the game
        track = self.music_menu.get()
        if track != "None":
            music = get_files(track)
        else:
            music = "None"
        
       #hides menu
        self.withdraw()

        #runs Tetris Game
        self.tetris_game = TetrisGame(self.logged_in_username, music)
        self.tetris_game.run()

        #after tetris game window is closed
        self.playback.seek(0)
        self.playback.resume()
        self.deiconify() #redisplays menu

    #displays leaderboard
    def display_LD(self):
        self.leader_board_screen = LeaderboardScreen(self)

    #displays tutorials
    def display_tutorial(self):
        self.tutorial_screen = TutorialScreen(self)

    #displays login screen
    def display_login(self):
        #initliases login screen as a child of CTkToplevel
        self.login_screen = ctk.CTkToplevel(self)

        # Screen properties
        self.login_screen.title("Login!")
        self.login_screen.geometry("340x360")
        self.login_screen.config(padx=10, pady=10)
        self.login_screen.grab_set()
        self.login_screen.resizable(False, False)

        # Frames
        login_frame = ctk.CTkFrame(
            master=self.login_screen
            )
        # Labels and Entries
        self.intro_label = ctk.CTkLabel(
            master=login_frame,
            text="Login",
            width=100,
            height=50,
            font = ("Arcadia", 32, "bold")
        )
        self.intro_label.pack(anchor=ctk.CENTER, pady=30)

        self.username_label = ctk.CTkLabel(
            master=login_frame,
            text="Username:",
            width=40,
            height=20,
            corner_radius=8,
            font = ("Arial", 14, "bold")
        )
        self.username_label.pack(padx=38, pady=(0, 3), anchor=ctk.W)

        self.username_entry = ctk.CTkEntry(
            master=login_frame,
            width=230,
            height=28,
            corner_radius=7,
            border_width=2,
            placeholder_text="username",
        )
        self.username_entry.pack(padx=45, pady=(0, 10), anchor=ctk.W)

        self.password_label = ctk.CTkLabel(
            master=login_frame,
            text="Password:",
            width=40,
            height=20,
            corner_radius=8,
            font = ("Arial", 14, "bold")
        )
        self.password_label.pack(padx=38, pady=(0, 3), anchor=ctk.W)

        self.password_entry = ctk.CTkEntry(
            master=login_frame,
            placeholder_text="password",
            width=230,
            height=28,
            corner_radius=7,
            border_width=2,
            show="*",
        )
        self.password_entry.pack(padx=45, pady=(0, 5), anchor=ctk.W)

        # Buttons
        self.login_button = ctk.CTkButton(
            master=login_frame,
            text="Login!",
            width=75,
            height=30,
            font = ("Arial", 12, "bold"),
            border_width=0,
            corner_radius=8,
            hover=True,
            command=self.login,
        )
        self.login_button.pack(anchor=ctk.CENTER, pady=40)

        login_frame.grid(
            row=0,
            column=0,
            rowspan=1,
            columnspan=1,
            sticky="nsew",
        )

    #display register screen
    def display_register(self):
        self.register_screen = ctk.CTkToplevel(self)
        self.register_screen.grab_set()

        #Screen Properties
        self.register_screen.title("Register!")
        self.register_screen.geometry("340x400")
        self.register_screen.config(padx=10, pady=10)
        self.register_screen.resizable(False, False)

        #Creates frame
        register_frame = ctk.CTkFrame(
            master=self.register_screen,
            width=0,
            height=0,
        )

        #Labels and Entries
        self.intro_label = ctk.CTkLabel(
            master=register_frame,
            text="Register Account",
            width=100,
            height=50,
            font = ("Arcadia", 26, "bold")
        )
        self.intro_label.pack(
            anchor=ctk.CENTER,
            padx=20,
            pady=25,
        )

        self.username_label = ctk.CTkLabel(
            master=register_frame,
            text="Username:",
            font = ("Arial", 14, "bold"),
            width=40,
            height=20,
            corner_radius=8,
        )
        self.username_label.pack(padx=38, pady=(0, 3), anchor=ctk.W)

        self.username_entry = ctk.CTkEntry(
            master=register_frame,
            placeholder_text="Username",
            width=230,
            height=28,
            corner_radius=7,
            border_width=2,
        )
        self.username_entry.pack(padx=45, pady=(0, 10), anchor=ctk.W)

        self.password_label = ctk.CTkLabel(
            master=register_frame,
            text="Password:",
            font = ("Arial", 14, "bold"),
            width=40,
            height=20,
            corner_radius=8,
        )
        self.password_label.pack(padx=38, pady=(0, 3), anchor=ctk.W)

        self.password_entry = ctk.CTkEntry(
            master=register_frame,
            placeholder_text="password",
            width=230,
            height=28,
            corner_radius=7,
            border_width=2,
            show="*",
        )
        self.password_entry.pack(padx=45, pady=(0, 10), anchor=ctk.W)

        self.confirm_password_label = ctk.CTkLabel(
            master=register_frame,
            text="Confirm Password:",
            font = ("Arial", 14, "bold"),
            width=40,
            height=20,
            corner_radius=8,
        )
        self.confirm_password_label.pack(padx=40, pady=(0, 3), anchor=ctk.W)

        self.confirm_password_entry = ctk.CTkEntry(
            master=register_frame,
            placeholder_text="confirm password",
            width=230,
            height=28,
            corner_radius=7,
            border_width=2,
            show="*",
        )
        self.confirm_password_entry.pack(padx=45, pady=(0, 5), anchor=ctk.W)

        #Buttons
        self.sign_up_button = ctk.CTkButton(
            master=register_frame,
            text="Register",
            font = ("Arial", 12, "bold"),
            border_width=0,
            corner_radius=7,
            width=75,
            height=30,
            hover=True,
            command=self.check_register,
        )
        self.sign_up_button.pack(
            anchor=ctk.CENTER,
            padx=(10, 0),
            pady=(30, 40),
        )

        register_frame.grid(
            row=0,
            column=0,
            rowspan=1,
            columnspan=1,
            sticky="nsew",
        )

#starts the main loop
if __name__ == "__main__":
    #checks for database existence, creates if it doesn't exist
    path = Path("data/app_data.db")
    if not path.is_file():
        create_database()
    #checks for music data file, creates if it doesn't exist
    path = Path("music/game_music.dat")
    if not path.is_file():
        create_files
    #runs the main menu loop
    app = MainApp()
    app.mainloop()
