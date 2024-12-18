import random
import string #ascii_uppercase
import sys


class GameBoard:
    def __init__(self):
        self.white = "⚪"
        self.black = "⚫"
        self.empty = "⬜"
        self.green = "🟢"
        self.red = "🔴"

        self.board_positions = [
                ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"],
                ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"],
                ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6"],
                ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5"],
                ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4"],
                ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"],
                ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
                ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"],
        ]

        self.board = [
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
                ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"],
        ]

        self.direction = {"up": [-1,0],"down": [1,0],"left": [0,-1],"right": [0,1],
            "up_left": [-1,-1],"up_right": [-1,1],"down_left": [1,-1],"down_right": [1,1],
        }


    def __str__(self):
        output = ""
        row_number = 8

        #Print row ID (8-1) and the row
        for row in self.board:
            output += f"\n{row_number} " #row ID
            row_number -= 1
            for position in row:
                output += f"{position}" #the row

        #Print column ID (A-H)
        output += "\n  "
        for letter in string.ascii_uppercase[:8]:
            output += f"{letter} "

        return output


    def clear(self):
        for row in range(8):
            for column in range(8):
                self.board[row][column] = self.empty


    def count(self, emoji) -> int:
        amount = 0
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == emoji:
                    amount += 1
        return amount


    def find_emoji(self, emoji) -> list:
        output = []
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == emoji:
                    output.append([row, column])
        return output


    def find_ID(self, row, column) -> str:
            return self.board_positions[row][column]


    def find_position(self, ID) -> list:
        for row in range(8):
            for column in range(8):
                if ID == self.board_positions[row][column]:
                    return [row, column]


    def place(self, row, column, emoji):
        self.board[row][column] = emoji


    def setup_othello(self):
        self.board[3][3] = self.white
        self.board[3][4] = self.black
        self.board[4][3] = self.black
        self.board[4][4] = self.white


#Game loop
def main():
    print("\n\nWelcome to Emoji OTHELLO!\nFlip your opponent's pieces!\nGame ends when BOTH players have no playable moves.\nPlayer with the most pieces wins!\nGood Luck!")

    #Game setup
    board = GameBoard()
    board.setup_othello()
    print(board)

    #Player setup
    color = choose_color()
    bot_color = opposite_disc(color)
    player_can_move = True
    bot_can_move = True
    player_first = (color == board.black)

    #Start of game loop
    while player_can_move or bot_can_move:
        if player_first: #This should only be false once. If player chooses white.
            #Player moves
            last_move = choose_move(board, color)
            if not last_move: #If no moves. (If not [] or an empty list. Meaning if this has something in it, it values to False. If nothing, True.)
                player_can_move = False
            else:
                bot_can_move = True #For rechecking if board changes.
                flip_opponent(board, last_move, bot_color)
                print(board)

        #Bot moves
        last_move = bot(board, bot_color)
        if not last_move:
            bot_can_move = False
        else:
            player_can_move = True
            flip_opponent(board, last_move, color)
            print(board)
            print(f"Your opponent plays {bot_color} on: {board.find_ID(last_move[0],last_move[1])}")

        player_first = True
        #End of game loop

    #Game over
    print(board)
    print("Looks like there are no move playable moves...")
    player_score = board.count(color)
    bot_score = board.count(bot_color)
    print(f"Player {color} has {player_score} pieces, Player {bot_color} has {bot_score}.")

    if player_score > bot_score:
        print("Congratulations, you've won!")
    else:
        print("So sorry, you've lost...")


#Logic for bot opponent
#Places a move on board for color. Returns [row, column] for where it placed move.
def bot(board, color) -> list:
    playable_moves = find_playable_moves(board, color)
    if not playable_moves: #If empty
        return list()
    random.shuffle(playable_moves)
    move = random.choice(playable_moves)
    board.place(move[0],move[1], color)
    return move


#Selects the player's disc emoji color
def choose_color():
    while True:
        try:
            color = input("Choose your color. B for black. W for white (Black moves first): ").upper()
        except KeyboardInterrupt:
            sys.exit("\nGame Stopped")
        if color == "B":
            return "⚫"
        elif color == "W":
            return "⚪"


#Places a disc (color) on a given board_positions, "A1" through "H8"; Returns the [row, column] of the board_positions choosen
def choose_move(board, color) -> list:
    playable = find_playable_moves(board, color)
    if not playable: #If empty
        return list()

    set_playable(board, playable)
    print(board) #Remove maybe?
    turn = True
    while turn:
        try:
            move = input("Choose your move 🟢 are playable positions (Ctrl + C to stop): ").upper()
        except KeyboardInterrupt:
            sys.exit("\nGame Stopped")
        if move == '':
            continue
        for row in range(8):
            for column in range(8): #linear search. Should change?
                if move in board.board_positions[row][column] and [row, column] in playable:
                    board.place(row, column, color)
                    remove_playable(board)
                    return [row, column]


#Changes the opponent's pieces based on the last_move and color of the opponent.
def flip_opponent(board, last_move, color):
    my_color = opposite_disc(color)
    directions = find_direction(board, last_move[0], last_move[1], my_color).split()
    flip_list = []
    check = last_move.copy() #To prevent the last_move from being modified.
    for direction in directions:
        while True:
            try:
                check[0] += board.direction[direction][0]
                check[1] += board.direction[direction][1]

                if check[0] > 7 or check[0] < 0:
                    raise IndexError
                elif check[1] > 7 or check[1] < 0:
                    raise IndexError

                if board.board[check[0]][check[1]] == color:
                    flip_list.append([check[0], check[1]])
                elif board.board[check[0]][check[1]] == board.empty:
                    check = last_move.copy() #Reset to original position
                    flip_list = []
                    break
                else:
                    check = last_move.copy()
                    break
            except IndexError:
                check = last_move.copy()
                flip_list = []
                break

        for position in flip_list:
            board.place(position[0], position[1], my_color)

        flip_list = []


#Returns the direction, board.direction, from a position where opposing neighbors of color are located
def find_direction(board, row, column, color) -> str:
    look_for = opposite_disc(color)
    output = ""
    for move, offset in board.direction.items():
        try:
            if board.board[row + offset[0]][column + offset[1]] == look_for:
                output += f"{move} "
        except IndexError:
            continue
    return output.strip()


#Returns the next available board.empty coordinate on the board from starting position and direction
def find_next_empty(board, start_coordinate, direction):
    x = start_coordinate[0]
    y = start_coordinate[1]
    color = board.board[x][y]
    next_move = board.direction[direction]
    while board.board[x][y] != board.empty:
        x += next_move[0]
        y += next_move[1]
        if x > 7 or x < 0: #If the search runs off he board
            return None
        elif y > 7 or y < 0:
            return None
        elif board.board[x][y] == color:
            return None
    return [x, y]


#Returns a list of the position(s) ID "A1" through "H8" given a coordinate [x,y] where x is the row and y is the column on the board
#Accepts a single [x, y] or a list of [[x1,y1],[x2,y2],...]
def find_position_ID(list) -> str:
    table = GameBoard()
    output = ""
    if is_list_of_lists(list):
        for position in list:
            row = position[0]
            column = position[1]
            output += f"{table.board_positions[row][column]} "
    else:
        output = f"{table.board_positions[list[0]][list[1]]}"
    return output.strip()


#Returns the coordinate(s) of playable moves
def find_playable_moves(board, color) -> list:
    output = list()
    positions = board.find_emoji(color)
    for pos in positions:
        #Determine search direction(s)
        search_for = find_direction(board, pos[0], pos[1], color).split()
        for direction in search_for:
            found = find_next_empty(board, pos, direction) #Returns None if none found
            if found: #If not None add the position to list
                output.append(found)
    return output


#Utility. Returns true if lst is a list with lists. Applied in function find_position_ID, set_playable
def is_list_of_lists(lst) -> bool:
    return all(isinstance(item, list) for item in lst)


#Returns opposite disc emoji
def opposite_disc(color):
    if color == "⚫":
        return "⚪"
    elif color == "⚪":
        return "⚫"
    else:
        return "🔴" #Instead of raising an error


#Places board.empty where board.green emoji found
def remove_playable(board):
    for row in range(8):
        for column in range(8):
            if board.board[row][column] == board.green:
                board.place(row, column, board.empty)


#Places board.green emoji on playable locations. Accepts [x, y] or [[x1, y1], [x2, y2],...]
def set_playable(board, list):
    if is_list_of_lists(list):
        for position in list:
            board.board[position[0]][position[1]] = board.green
    else:
        board.board[list[0]][list[1]] = board.green


if __name__ == "__main__":
    main()
