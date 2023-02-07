#imports
from tetris_game.game_vars import *
from tetris_game.file_manager import *
from just_playback import Playback
import pygame, time, random

#seven bag class
class seven_bag():
    def __init__(self):
        self.bag = [1, 2, 3, 4, 5, 6, 7]
        self.val = -1

    def jumble(self):
        random.shuffle(self.bag)

    #increments and returns the current item in the bag list
    def value(self):
        if self.val == -1:
            self.jumble()

        self.val += 1
        #shuffles bag if end of bag is reached, and returns indexed item from list
        if self.val == 7:
            self.jumble()
            self.val = 0
            return self.bag[self.val]
        else:
            return self.bag[self.val]

#piece class
class piece():
    def __init__(self, seven_bag):
        self.shape = shapes[seven_bag - 1] #shape matrix using current seven_bag position
        self.val = seven_bag 
        self.max_off_set = self.get_off_set()
        self.piece_x = 0
        self.piece_y = 0
    
    #generates pieces max offset value from seven bag value
    def get_off_set(self):
        if self.val == 6:
            return 3
        elif self.val == 7:
            return 0
        else:
            return 1
   
    #clockwise rotations reverses the shape list before applying the rotation function
    #anticlockwise rotations reverses the shape list after
    def rotate(self, direction):
        new_piece = self.shape
        if direction == "clock":
            new_rotation = list(
                map(list, 
                    map(reversed,
                        zip(*new_piece)
                        )
                    )
                )
        elif direction == "anti":
            new_rotation = list(
                    map(list,
                        zip(*new_piece) #reforms the shape matrix into tuples according to their index positions in the original lists
                        ) #converts each tuple into a list
                    ) #maps all lists into one master list to form thew new matrix
            new_rotation.reverse()
        return new_rotation

#Tetris Game class
class TetrisGame():
    def __init__(self, username, music):
        #initiates pygame with key repeat intervals
        pygame.init()
        pygame.key.set_repeat(250, 40)

        self.username = username

        #creates width and height of screen
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.rlim = cell_size * cols  #creates the right-hand limit distance of the game board

        #generates grid for background
        self.grid = self.new_grid()

        self.default_font = pygame.font.SysFont("Arial", 14)
        self.default_font_2 = pygame.font.SysFont("Arial", 16)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tetris!')

        #sets music list
        self.music = music

        #initialises file objects
        self.file = file_creator()
        self.file_handler = file_handler(self.file)

    #Initialises game
    def init_game(self):
        #initialises and jumbles the seven_bag object
        self.seven_bag = seven_bag()
        self.seven_bag.jumble()
        
        #creates new board
        self.board = self.new_board()

        #initialises the first 'next piece' (first piece of the game)
        self.next_piece = piece(self.seven_bag.value())
        self.new_piece()
        
        self.level = 1
        self.score = 0
        self.lines = 0
        if self.username != "":
            self.high_score = self.file_handler.load_score(self.username)
        else:
            self.high_score = "N/A"
        
        #creates custom pygame event for keeping track of game speed
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    
    #generates checkered background grid
    def new_grid(self):
        self.grid = []
        for y in range(rows):
            line = []
            for x in range(cols):
                if (x%2 == y%2):
                    line.append(8)
                else:
                    line.append(0)
            self.grid.append(line)
        return self.grid

    #Generates a new board matrix
    def new_board(self):
        board = [[0 for x in range(cols)] for y in range(rows)]
        board += [[1 for x in range(cols)]]
        return board

    #Starts game via Key Actuation
    def start_game(self):
        if self.gameover:
            self.init_game()
            #plays music if required
            if self.music != "None":
                self.playback = Playback()
                self.playback.load_file(self.music[0])
                self.playback.loop_at_end(True)
                self.playback.set_volume(self.music[1])
                self.playback.play()
            self.gameover = False
    
    #displays location based text via top left X/Y co-ords
    def text(self, text, top_left, off_set_y):
        x, y = top_left
        for line in text.splitlines():
            self.screen.blit(
                self.default_font.render(line, False, colors[9], colors[0]), (x, y)
            )
            y += off_set_y
    
    #displays text at the center of the screen
    def center_text(self, text):
        for i, line in enumerate(text.splitlines()):
            message = self.default_font_2.render(line, False, colors[9], colors[8])

            message_center_x, message_center_y = message.get_size()
            message_center_x //= 2
            message_center_y //= 2

            self.screen.blit(
                message,
                (
                    self.width // 2 - message_center_x,
                    self.height // 2 - message_center_y + i * 22,
                ),
            )
        
    #checks for collisions between current shape and board
    def check_collision(self, shape, offset):
        if shape == "null":
            shape = self.piece.shape
        #XY coordinate of top left piece of the shape mapped onto the game board matrix
        off_x, off_y = offset
        temp_list = []
        #generates a temp-list of each cell's local YX position, with the value of each cell
        for cy, row in enumerate(shape):
            for cx, val in enumerate(row):
                temp_list.append([cy, cx, val])
                pass
        #checks each cell in the temp list
        for cell in temp_list:
            try:
                if (cell[2] and self.board[cell[0] + off_y][cell[1]+ off_x]) or cell[1] < 0: #checks if the two coords are the same (collision), or if cell is too far left
                    return True
            except IndexError: #checks if XY coord is out of range of the board
                return True
        return False

    #Generates new piece and checks for game over
    def new_piece(self):
        self.piece = self.next_piece 
        self.next_piece = piece(self.seven_bag.value()) #generates a new next piece
        self.piece.piece_x = int(cols / 2 - len(self.piece.shape[0]) / 2) #sets piece's X coordinate to the center of the grid (left adjusted if the piece has an odd length)
        self.piece.piece_y = 0
        #checks if new piece being placed causes a collision
        if self.check_collision("null", (self.piece.piece_x, self.piece.piece_y)):
            if self.music != "None":
                self.playback.stop()
            self.gameover = True
            if self.username != "":
                self.status = self.file_handler.save_score(self.username, self.score)
            else: 
                self.status = "not saved"
    
    #manages soft dropping caused via hard drop or Key Actuation
    def soft_drop(self, manual):
        if not self.gameover and not self.paused:
            #increments score if soft-drop was caused by user
            if manual:
                self.score += 1
            self.piece.piece_y += 1
            #checks for collisions caused by the piece falling
            if self.check_collision("null", (self.piece.piece_x, self.piece.piece_y)):
                self.board = self.join_mats((self.piece.piece_x, self.piece.piece_y))
                self.new_piece()
                cleared_lines = 0
                #checks each row on the grid to see if any lines are completely filled
                for i, line in enumerate(self.board[:-1]):
                    if 0 not in line:
                        self.board = self.remove_line(i) 
                        cleared_lines += 1
                #calculates scores from lines cleared
                self.add_cleared_lines(cleared_lines)
                return True
            else:
                return False
        return False

    #Manages Hard Drop via Key Actuation - loops Soft Drop
    def hard_drop(self):
        if not self.gameover and not self.paused:
            while not self.soft_drop(True):
                pass
    
    #Calculates score added from line clears
    def add_cleared_lines(self, n):
        line_vals = [0, 40, 100, 300, 1200]
        old_mod = self.lines % 10
        self.lines += n
        new_mod = self.lines % 10
        self.score += line_vals[n] * self.level
        #checks if level needs to be incremented
        if old_mod > new_mod:
            self.level += 1
        #updates game speed
        new_delay = 1000 - 50 * (self.level - 1)
        if new_delay < 100:
            new_delay = 100
        pygame.time.set_timer(pygame.USEREVENT + 1, new_delay)

    #Removes line(s) from the board
    def remove_line(self, line):
        del self.board[line]
        #adds clear lines to the top of the board
        self.board = [[0 for i in range(cols)]] + self.board
        return self.board
    
    #Draws the blocks onto the screen to represent the game
    def draw_mats(self, item, offset):
        #distance of top left cell in shape matrix from the top left of the tetris board
        temp_list = []
        off_x, off_y = offset
        #generates a temp-list of each cell's local YX position, with the value of each cell
        for cy, row in enumerate(item):
            for cx, val in enumerate(row):
                temp_list.append([cy, cx, val])
        #draws each cell of the shape onto the display
        for cell in temp_list:
            if cell[2]:
                pygame.draw.rect(
                    self.screen,
                    colors[cell[2]],
                    pygame.Rect(
                        (cell[1] + off_x) * cell_size,
                        (cell[0] + off_y) * cell_size,
                        cell_size,
                        cell_size,
                    ),
                    0,
                )
    
    #Connects the shape matrix to the board matrix
    def join_mats(self, off_set):
        #XY position of top left cell in shape matrix mapped to the game board matrix
        temp_list = []
        off_x, off_y = off_set
        #generates a temp-list of each cell's local YX position, with the value of each cell
        for cy, row in enumerate(self.piece.shape):
            for cx, val in enumerate(row):
                temp_list.append([cy, cx, val])
        #checks each cell of the shape
        for cell in temp_list:
            self.board[cell[0] + off_y - 1][cell[1] + off_x] += cell[2] #converts board cell to piece cell
        return self.board
    
    #Manages horizontal movement via key actuation
    def move(self, dx):
        if not self.gameover and not self.paused:
            new_x = self.piece.piece_x + dx
            #checks for horizontal collisions
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.piece.shape[0]):
                new_x = cols - len(self.piece.shape[0])
            if not self.check_collision("null", (new_x, self.piece.piece_y)):
                self.piece.piece_x = new_x

     #Manages the rotation procedure
    def rotate_piece(self, direction):
        if not self.gameover and not self.paused:
            temp = self.piece
            new_piece = piece.rotate(self.piece, direction)
            off_set = 0
            if not self.check_collision(
                new_piece, (self.piece.piece_x, self.piece.piece_y)
            ):
                self.piece.shape = new_piece
                return
            else:
                #piece is offset and checked in both left and right directions until a legal rotation is found, or until the piece has maxed out its offset value
                for i in range(0, self.piece.get_off_set()):
                    off_set += 1
                    if (self.piece.piece_x - off_set) < 0:
                        return
                    if not self.check_collision(
                        new_piece,
                        (self.piece.piece_x - off_set, self.piece.piece_y), #left offset
                    ):
                        self.piece.piece_x -= off_set
                        self.piece.shape = new_piece
                        return
                    elif not self.check_collision(
                        new_piece,
                        (self.piece.piece_x + off_set, self.piece.piece_y), #right offset
                    ):
                        self.piece.piece_x += off_set
                        self.piece.shape = new_piece
                        return
                self.piece = temp
                return
        else:
            return

    #Quits game
    def quit(self):
        try:
            if self.music != "None":
                self.playback.stop()
        except:
            pass
        self.run = False
        self.screen.fill(colors[8])
        self.center_text("Quitting...")
        pygame.display.update()
        time.sleep(1)
        pygame.display.quit()
        pygame.quit()
     
     #Manages pause toggling
    def toggle_pause(self):
        if not self.paused:
            self.playback.pause()
        else:
            self.playback.resume()
        self.paused = not self.paused


    #runs game
    def run(self):
        #binds each key to an action
        keybinds = {
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': lambda: self.soft_drop(True),
            'UP': lambda: self.rotate_piece("anti"),
            "z": lambda: self.rotate_piece("anti"),
            "c": lambda: self.rotate_piece("clock"),
            'p': self.toggle_pause,
            'RETURN': self.start_game,
            'SPACE': self.hard_drop
            }

        self.gameover = True
        self.paused = False
        self.status = "start"

        if self.username == "":
            username = "Guest Account"
        else:
            username = self.username
        
        #initiates pygame clock to use as FPS limit
        clock = pygame.time.Clock()

        self.run = True

        while self.run:
            try:
                self.screen.fill(colors[0])
                #Following section displays a different splash screen dependant on the state of game.
                if self.gameover:
                    self.screen.fill(colors[8])
                    if self.status == "start":
                        self.center_text("""Press ENTER to start!\nPress ESCAPE to quit at any time!""")
                    if self.status == "new user":
                        self.center_text(
                            """Game over!\nYour score: %d\n\nNew user - your score has been saved!\nPress ENTER to play again!\nPress ESCAPE to quit at any time!"""
                            % self.score
                        )
                    if self.status == "saved":
                        self.center_text(
                            """Game over!\nYour score: %d\n\nNew high score - your score has been saved!\nPress ENTER to play again!\nPress ESCAPE to quit at any time!"""
                            % self.score
                        )
                    if self.status == "not saved":
                        self.center_text(
                            """Game over!\nYour score: %d\nPress ENTER to play again!\nPress ESCAPE to quit at any time!"""
                            % self.score
                        )
                
                else:
                    #Pause screen
                    if self.paused:
                        self.screen.fill(colors[8])
                        self.center_text("Paused")

                    #Gameplay loop
                    else:
                        pygame.draw.line(
                            self.screen,
                            colors[9],
                            (self.rlim + 1, self.height - 1),
                            (self.rlim + 1, self.height - 600),
                        )
                        
                        #Writes info text
                        self.text(
                            "User: \n{0}\n\nScore: \n{1}\nHigh Score: \n{2}\n\nLevel: {3}\nLines: {4}".format(
                                username,
                                self.score,
                                self.high_score,
                                self.level,
                                self.lines,
                            ),
                            (self.rlim + cell_size, cell_size * 5),
                            18,
                        )
                        self.text(
                            "Next Shape:", (self.rlim + cell_size, cell_size - 10), 0 
                        )
                        self.draw_mats(self.grid, (0, 0))   #Draws the background grid
                        self.draw_mats(self.board, (0, 0))  #Draws the game grid, where the pieces are placed
                        self.draw_mats(
                            self.piece.shape, (self.piece.piece_x, self.piece.piece_y) #Draws the current piece that is falling
                        )
                        self.draw_mats(self.next_piece.shape, (cols + 1, 2)) #Draws the 'next piece' using the required offset
                pygame.display.update() #updates Pygame

                #Handles pygame events
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT + 1:
                        self.soft_drop(False)
                    elif event.key == pygame.K_ESCAPE:
                        return(self.quit())
                    #checks if a keybind has been actuated.
                    elif event.type == pygame.KEYDOWN: 
                        for key in keybinds:
                            if event.key == eval("pygame.K_" + key):
                                keybinds[key]()

                #runs pygame at the stated FPS
                clock.tick(maxfps)
            except:
                pass
