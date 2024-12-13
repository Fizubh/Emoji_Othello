import pytest
import random

from project import opposite_disc, game_board, find_position_ID, find_direction, find_next_empty, find_playable_moves, bot
from project import choose_color, choose_move, flip_opponent, remove_playable, set_playable


#For my own testing. Not project requirement.
def test_class_game_board():
    board = game_board()

    #Confirm board.setup_othell()
    board.setup_othello()
    assert board.board[3][3] == board.white
    assert board.board[3][4] == board.black
    assert board.board[4][3] == board.black
    assert board.board[4][4] == board.white

    #Confirm board.clear()
    board.clear()
    assert board.board[3][3] == board.empty
    assert board.board[3][4] == board.empty
    assert board.board[4][3] == board.empty
    assert board.board[4][4] == board.empty

    #Confirm board.count(emoji)
    board.setup_othello()
    assert board.count(board.black) == 2
    assert board.count(board.white) == 2

    #Confirm board.find_emoji(emoji)
    assert board.find_emoji(board.black) == [[3,4],[4,3]]
    assert board.find_emoji(board.white) == [[3,3],[4,4]]

    #Confirm board.find_ID(row, column)
    assert board.find_ID(0, 0) == 'A8'
    assert board.find_ID(7, 7) == 'H1'
    with pytest.raises(IndexError):
        board.find_ID(8,8)

    #Confirm board.find_position(ID)
    assert board.find_position('A8') == [0,0]
    assert board.find_position('H1') == [7,7]
    assert board.find_position('H9') == None

    #Confirm board.place(row, column, emoji)
    board.place(0, 0, board.black)
    board.place(7, 7, board.white)
    assert board.board[0][0] == board.black
    assert board.board[7][7] == board.white


def test_bot():
    board = game_board()
    board.place(3, 3, board.white)
    board.place(3, 4, board.black)
    #Logic for bot opponent
    #Places a move on board for color. Returns [row, column] for where it placed move.
    #Function stub: bot(board, color) -> list:
    assert bot(board, board.black) == [3, 2]
    board.place(3, 2, board.empty) #Reset
    assert bot(board, board.white) == [3, 5]


def test_choose_color(monkeypatch):
    #Selects the player's disc emoji color
    #function stub: choose_color():

    # Simulate user input
    monkeypatch.setattr('builtins.input', lambda _: 'w')
    assert choose_color() == "⚪"

    monkeypatch.setattr('builtins.input', lambda _: 'b')
    assert choose_color() == "⚫"


def test_choose_move(monkeypatch):
    board = game_board()
    board.setup_othello()
    #Places a disc (color) on a given board_positions, "A1" through "H8"; Returns the [row, column] of the board_positions choosen
    #Function stub: choose_move(board, color) -> list:
    monkeypatch.setattr('builtins.input', lambda _: 'd6') #Note: choose_move does not flip the opponent's pieces
    assert choose_move(board, "⚫") == [2, 3] #d6 is at location [2, 3]
    assert board.board[2][3] == "⚫" #at location [2, 3] there exists an appropriate colored disc emoji

    monkeypatch.setattr('builtins.input', lambda _: 'c5')
    assert choose_move(board, "⚫") == [3, 2]
    assert board.board[3][2] == "⚫"

    monkeypatch.setattr('builtins.input', lambda _: 'f4')
    assert choose_move(board, "⚫") == [4, 5]
    assert board.board[4][5] == "⚫"

    monkeypatch.setattr('builtins.input', lambda _: 'e3')
    assert choose_move(board, "⚫") == [5, 4]
    assert board.board[5][4] == "⚫"

    board.clear()
    board.setup_othello()

    monkeypatch.setattr('builtins.input', lambda _: 'e6')
    assert choose_move(board, "⚪") == [2, 4]
    assert board.board[2][4] == "⚪"

    monkeypatch.setattr('builtins.input', lambda _: 'f5')
    assert choose_move(board, "⚪") == [3, 5]
    assert board.board[3][5] == "⚪"

    monkeypatch.setattr('builtins.input', lambda _: 'c4')
    assert choose_move(board, "⚪") == [4, 2]
    assert board.board[4][2] == "⚪"

    monkeypatch.setattr('builtins.input', lambda _: 'd3')
    assert choose_move(board, "⚪") == [5, 3]
    assert board.board[5][3] == "⚪"


def test_find_direction():
    board = game_board()
    board.setup_othello()
    #Returns the direction, board.direction, from a position where opposing neighbors of color are located
    #Function stub: find_direction(board, row, column, color) -> str:
    #Note: It checks in the order of: up down left right up_left up_right down_left down_right
    assert find_direction(board, 3, 3, board.white) == "down right"
    assert find_direction(board, 4, 4, board.white) == "up left"

    board.place(4, 4, board.empty)
    board.place(2, 3, board.black)
    board.place(3, 2, board.black)
    assert find_direction(board, 3, 3, board.white) == "up down left right" #Diamond formation

    board.clear()
    board.place(3, 3, board.white)
    board.place(2, 2, board.black)
    board.place(2, 4, board.black)
    board.place(4, 2, board.black)
    board.place(4, 4, board.black)
    assert find_direction(board, 3, 3, board.white) == "up_left up_right down_left down_right" #X formation

    board.place(3, 2, board.black)
    board.place(3, 4, board.black)
    board.place(2, 3, board.black)
    board.place(4, 3, board.black)
    assert find_direction(board, 3, 3, board.white) == "up down left right up_left up_right down_left down_right" #Surrounded

    board.clear()
    board.place(3, 3, board.white)
    assert find_direction(board, 3, 3, board.white) == "" #No neighbors. Note: this should never be the case

    board.place(1, 3, board.black)
    board.place(3, 4, board.white)
    assert find_direction(board, 3, 3, board.white) == "" #Only actual neighbors, and not distant ones, as well as opposite colored only


def test_find_next_empty():
    table = game_board()
    table.setup_othello()
    #Returns the next available empty coordinate on the board from starting position and direction to search
    #find_next_empty(board, start_coordinate, direction)
    assert find_next_empty(table, [3, 3], "up") == [2, 3]
    assert find_next_empty(table, [3, 3], "down") == [5, 3]
    assert find_next_empty(table, [3, 3], "left") == [3, 2]
    assert find_next_empty(table, [3, 3], "right") == [3, 5]
    assert find_next_empty(table, [3, 3], "up_left") == [2, 2]
    assert find_next_empty(table, [3, 3], "up_right") == [2, 4]
    assert find_next_empty(table, [3, 3], "down_left") == [4, 2]
    assert find_next_empty(table, [3, 3], "down_right") == None
    #assert find_next_empty(table, [3, 3], "down_right") == [5, 5]


def test_find_playable_moves():
    board = game_board()
    board.setup_othello()
    #Returns the coordinate(s) of playable moves
    #find_playable_moves(board, color) -> list:
    #This function implements: find_positions, find_direction, find_next_empty
    assert find_playable_moves(board, board.black) == [[5, 4], [3, 2], [2, 3], [4, 5]]
    assert find_playable_moves(board, board.white) == [[5, 3], [3, 5], [2, 4], [4, 2]]

    for row in range(8):
        for column in range(8):
            board.board[row][column] = random.choice(["⚪","⚫"])
    assert find_playable_moves(board, board.black) == [] #There are no playable moves


def test_find_position_ID():
    #Returns a list of the position(s) ID "A1" through "H8" given a coordinate [x,y] where x is the row and y is the column on the board
    #Accepts a single [x, y] or a list of [[x1,y1],[x2,y2],...]
    #Function stub: find_position_ID(list) -> str:
    assert find_position_ID([0,0]) == "A8"
    assert find_position_ID([[0,0], [1,0], [0,1]]) == "A8 A7 B8"


def test_flip_opponent():
    #Changes the opponent's pieces based on the last_move and color of the opponent.
    #Function stub: flip_opponent(board, last_move, color)
    board = game_board()

    board.setup_othello()
    board.place(3,5,board.white)
    flip_opponent(board, [3, 5], board.black)
    assert board.board[3][4] == board.white

    board.clear()
    board.setup_othello()
    board.place(2,3,board.black)
    flip_opponent(board, [2, 3], board.white)
    assert board.board[3][3] == board.black

    #Check for horizonal wrapping (Which is not suppose to happen. Pieces should not be flipped)
    #This can occur as a result of python's negative indices being valid. Example, [-1,-1] is...
    #the same as [7, 7]. -8 however will throw an IndexError.
    board.clear()
    board.place(3, 0, board.black)
    board.place(3, 1, board.black)
    board.place(3, 2, board.white)
    board.place(3, 7, board.black)
    board.place(3, 6, board.black)
    board.place(3, 5, board.white)
    flip_opponent(board, [3, 2], board.black)
    assert board.board[3][1] == board.black
    assert board.board[3][6] == board.black

    #Check for vertical wrapping
    board.clear()
    board.place(0, 3, board.black)
    board.place(1, 3, board.black)
    board.place(2, 3, board.white)
    board.place(7, 3, board.black)
    board.place(6, 3, board.black)
    board.place(5, 3, board.white)
    flip_opponent(board, [2, 3], board.black)
    assert board.board[1][3] == board.black
    assert board.board[6][3] == board.black

    #Check for diagonal wrapping
    board.clear()
    board.place(0,2,board.white)
    board.place(7,1,board.white)
    board.place(6,0,board.black)
    board.place(1,3,board.white)
    board.place(2,4,board.white)
    board.place(3,5,board.white)
    board.place(4,6,board.black)
    flip_opponent(board, [4,6], board.white)
    assert board.board[1][3] == board.white
    assert board.board[7][1] == board.white


def test_opposite_disc():
    #Returns opposite disc emoji
    #Function stub: opposite_disc(color):
    assert opposite_disc("⚫") == "⚪"
    assert opposite_disc("⚪") == "⚫"
    assert opposite_disc("Moo") == "🔴"


def test_remove_playable():
    #Places board.empty where board.green emoji found
    #Function stub: remove_playable(board):
    board = game_board()
    board.board[3][3] = board.green
    board.board[4][4] = board.green
    remove_playable(board)
    assert board.board[3][3] == board.empty
    assert board.board[4][4] == board.empty


def test_set_playable():
    #Places board.green emoji on playable locations. Accepts [x, y] or [[x1, y1], [x2, y2],...]
    #Function stub: set_playable(board, list):
    board = game_board()
    set_playable(board, [3,3])
    assert board.board[3][3] == board.green

    set_playable(board,[[4,5],[5,5]])
    assert board.board[4][5] == board.green
    assert board.board[5][5] == board.green
