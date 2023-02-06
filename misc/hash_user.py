#takes username string input and hashes the result

def hash_user(string):
    hash_value = 0
    count = 0
    for char in string:
        count +=1
        #increases hash_value by the int value of the character multiplied by character position
        hash_value += ord(char)*count
    #mods hash val by 1000 to produce the hash key
    hash_value %= 1000
    return hash_value


