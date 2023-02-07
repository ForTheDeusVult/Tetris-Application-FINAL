#imports
import pickle, shelve

#track_int = [file, volume multiplier]

#creates the game_music.dat music file
def create_files():
    #generates music data lists
    track_1 = ["music/music files/Track 1.mp3", 1]
    track_2 = ["music/music files/Track 2.mp3", 1]
    track_3 = ["music/music files/Track 3.mp3", 1]
    track_4 = ["music/music files/Track 4.mp3", 1] 
    track_5 = ["music/music files/Track 5.mp3", 1]
    track_6 = ["music/music files/Track 6.mp3", 1]

    #opensdumps lists into the game_music.dat file
    with open("music/game_music.dat","wb") as f:

        pickle.dump(track_1, f)
        pickle.dump(track_2, f)
        pickle.dump(track_3, f)
        pickle.dump(track_4, f)
        pickle.dump(track_5, f)
        pickle.dump(track_6, f)

    #closes file
    f.close()

#returns the required music track list
def get_files(track):
    
    #loads lists from .dat file via pickle
    with open("music/game_music.dat","rb") as f:

        track_1 = pickle.load(f)
        track_2 = pickle.load(f)
        track_3 = pickle.load(f)
        track_4 = pickle.load(f)
        track_5 = pickle.load(f)
        track_6 = pickle.load(f)

    #closes .dat file
    f.close

    #places lists on shelves
    with shelve.open("music/game_music_shelf") as s:
        s["Track 1"] = track_1
        s["Track 2"] = track_2
        s["Track 3"] = track_3
        s["Track 4"] = track_4 
        s["Track 5"] = track_5
        s["Track 6"] = track_6

        #sets the output to be the value of the dictionary according to the track argument
        output = s[track]
    
    #closes shelf
    s.close()
    return output




