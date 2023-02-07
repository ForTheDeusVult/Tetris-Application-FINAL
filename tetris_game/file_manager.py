#imports
import os, json, sqlite3
from datetime import datetime as dt

#creates app_data.db
def create_database():
    #Connects to the database (creates the database)
    connection = sqlite3.connect("data/app_data.db")
    # Create the Cursor
    cur = connection.cursor()
     
    #Create game_data table
    cur.executescript(
        """CREATE TABLE game_data(
        user_id INT PRIMARY KEY NOT NULL,
        highscore INT NOT NULL,
        time VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user_data(user_id)
        );""")

    #Create user_data table
    cur.executescript(
        """CREATE TABLE user_data(
        user_id INT PRIMARY KEY NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
        );""")

    #commit changes
    connection.commit()
    #close the connection
    connection.close()

def save_to_database(username, score, date):
    try:
        # Connect to the database
        connection = sqlite3.connect("data/app_data.db")
        # Create the cursor
        cur = connection.cursor()

        #fetches user_id from user_data
        cur.execute("SELECT user_id FROM user_data WHERE username=?", (username,))

        #sets user_id to the output of the SQL query
        user_id = cur.fetchone()[0]

        #returns the amount of times user_id appears in the game_data table
        cur.execute("SELECT COUNT(*) FROM game_data WHERE user_id=?", (user_id,))

        #True if SQL query returns anything higher than 0
        existed_user = cur.fetchone()[0] > 0

        if existed_user:

            #fetches user highscore
            cur.execute("""
            SELECT game_data.highscore 
            FROM game_data, user_data
            WHERE game_data.user_id = user_data.user_id
            AND user_data.username=?""", (username,))

            #sets user_highscore to the output of the SQL query
            user_highscore = cur.fetchone()[0]
            if score > user_highscore:
                cur.execute("""
                UPDATE game_data 
                SET highscore=(?), time =(?)
                FROM user_data
                WHERE game_data.user_id = user_data.user_id
                AND user_data.username=(?)""",
                (score, date, username,))

                #commit changes
                connection.commit()
                #close the connection
                connection.close()

            else:
                #commit changes
                connection.commit()
                #close the connection
                connection.close()  

        else:
            #inserts record into game_data table
            cur.execute("""
                INSERT INTO game_data 
                (user_id, highscore, time) 
                VALUES (?, ?, ?)""",
                (user_id, score, date,)
            )

             # Commit the changes
            connection.commit()
            # Close the connection
            connection.close()
    
    #handles exceptions
    except sqlite3.OperationalError or sqlite3.ProgrammingError as e:
        pass

#Parent Class used to generate the JSON file
class file_creator:
    def __init__(self):
        self.file = "data/score_data.json" #JSON file path
        
        #creates the JSON file if it does not exist.
        try:
            with open(self.file, "r") as f:
                data = json.load(f)
                f.close()
        except:
            with open(self.file, "w") as f:
                f.close()

    #creates the first entry in the JSON file
    def create_new_dir(self, username, score, date_time):
        scores = {
            "scores": [
                {"username": username, "high_score": score, "datetime": date_time}
            ]
        }
        #writes to the JSON file
        with open(self.file, "w") as f:
            json.dump(scores, f, indent=5)
        #closes JSON file
        f.close()
        return "new user"

#Child Class, inherits from file_creator
class file_handler(file_creator):
    def __init__(self, parent):
        #initialises parent class constructor, creates a parent object as an attribute
        parent.__init__()
        self.parent = parent

    #loads scores from JSON file
    def load_score(self, username):
        #opens file in read mode
        with open(self.parent.file, "r") as f:
            #checks if JSON file is empty
            if os.path.getsize(self.parent.file) != 0:
                #loads data from the JSON file, then splits the dictionary into a list of dictionaries
                data = json.load(f)
                temp = data["scores"]
                for entry in temp:
                    #checks if username exists in file
                    if entry["username"] == username:
                        high_score = entry["high_score"]
                        #closes file
                        f.close()
                        return high_score
                #closes file
                f.close()
                return "N/A"
            else:
                #closes file
                f.close()
                return "N/A"
    
    #saves score
    def save_score(self, username, score):
        date_time = dt.now().strftime("%H:%M:%S %d/%m/%Y") #takes the current date and time in HH:MM:SS DD/MM/YYYY format
        save_to_database(username, score, date_time) #writes to database first
        #opens file
        with open(self.parent.file) as f:
            try:
                #loads data from the JSON file, then splits the dictionary into a list of dictionaries
                data = json.load(f)
                temp = data["scores"]
                #closes file
                f.close()
                #searches for username
                for entry in temp:
                    if entry["username"] == username:
                        #updates highscore if required
                        if score >= entry["high_score"]:
                            entry["high_score"] = score
                            entry["datetime"] = date_time
                            #writes to JSON file
                            with open(self.parent.file, "w") as fi:
                                json.dump(data, fi, indent=5)
                            #closes file
                            fi.close()
                            return "saved"
                        else:
                            return "not saved"
                #creates new save if username not found
                return self.create_save(data, temp, username, score, date_time)
            #uses an Exception to detect if a 'first' entry needs to be made
            except Exception as e:
                f.close()
                #creates 'first' entry
                return self.parent.create_new_dir(username, score, date_time)

    #creates save
    def create_save(self, data, temp, username, score, date_time):
        #generates a new dictionary for the new user
        x = {"username": username, "high_score": score, "datetime": date_time}
        #appends to the list of dictionaries
        temp.append(x)
        #writes to file
        with open(self.parent.file, "w") as f:
            json.dump(data, f, indent=5)
        #closes file
        f.close()
        return "new user"
