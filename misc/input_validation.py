#user_input = username or password string
#input_type = whether the check is for a username or password

def input_validate(user_input, input_type):
    if user_input == "": #checks if user input is empty
        return "empty"
    if input_type == "password":
        if len(user_input) < 7 or len(user_input) > 15: #checks if password length is invalid
            return "out of range"
    if input_type == "username":
        if len(user_input) < 4 or len(user_input) > 15: #checks if username length is invalid
            return "out of range"
    return True
