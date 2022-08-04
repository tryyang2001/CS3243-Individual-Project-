import enum
import sys
import abc
import string
import math
import random
import copy
from heapq import nsmallest

#Constant defined for better intepretation
EMPTY_SPACE = ' '
GOAL = 'G'
OWN_KING = '♚'
REACHED = '.'
ENEMY_KING = '♔'
ENEMY_KNIGHT = '♘'
ENEMY_BISHOP = '♗'
ENEMY_ROOK = '♖'
ENEMY_QUEEN = '♕'
OBSTACLE = 'X'

"""#######################################################################
The code below includes the helper functions and data structure used in the whole program
#######################################################################"""
col_mapping = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25,
    "0":"a",
    "1":"b",
    "2":"c",
    "3":"d",
    "4":"e",
    "5":"f",
    "6":"g",
    "7":"h",
    "8":"i",
    "9":"j",
    "10":"k",
    "11":"l",
    "12":"m",
    "13":"n",
    "14":"o",
    "15":"p",
    "16":"q",
    "17":"r",
    "18":"s",
    "19":"t",
    "20":"u",
    "21":"v",
    "22":"w",
    "23":"x",
    "24":"y",
    "25":"z"
}
# Global variables for ease of use
obstacles = dict()
reached = dict()

def is_within_board(row, col, total_row, total_col):
    return row < total_row and row >= 0 and col < total_col and col >= 0

def no_obstacle(row, col):
    return (row, col) not in obstacles

def can_travel(board, col, row):
    return (row, col) not in obstacles and (row, col) not in reached

"""#######################################################################
The code below refers to the classes of the chess pieces, including King, Queen, Bishop, Rook and Knight
Each piece class stores information about the movement and generate all the available positions it can move to.
To initialize each piece class, users are expected to provide the total rows and total columns of the game board.
#######################################################################"""


class Piece:
    def __init__(self, rows, cols, curr_pos):
        self.total_rows, self.total_cols = rows, cols
        self.threatened = []
        self.threatening = []
        self.curr_pos = curr_pos

class King(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = list()
        if (self.can_block(row - 1, col, states)):
            states.append((row - 1, col))
        if (self.can_block(row - 1, col + 1, states)):
            states.append((row - 1, col + 1))
        if (self.can_block(row, col + 1, states)):
            states.append((row, col + 1))
        if (self.can_block(row + 1, col + 1, states)):
            states.append((row + 1, col + 1))
        if (self.can_block(row + 1, col, states)):
            states.append((row + 1, col))
        if (self.can_block(row + 1, col - 1, states)):
            states.append((row + 1, col - 1))
        if (self.can_block(row, col - 1, states)):
            states.append((row, col - 1))
        if (self.can_block(row - 1, col - 1, states)):
            states.append((row - 1, col - 1))
        return states

    def can_block(self, row, col, states):
        return (is_within_board(row, col, self.total_rows, self.total_cols) and (row, col) not in obstacles)

    def __repr__(self):
        return "King"

class Queen(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = []
        states.extend(Rook(self.total_rows, self.total_cols, curr_pos).get_blocked_positions(curr_pos))
        states.extend(Bishop(self.total_rows, self.total_cols, curr_pos).get_blocked_positions(curr_pos))
        return states

    def __repr__(self):
        return "Queen"

class Bishop(Piece):
    def get_blocked_positions(self, curr_pos):
        states = []
        row, col = curr_pos[0], curr_pos[1]
        # upper left
        dx, dy = row - 1, col - 1
        while (dx >= 0 and dy >= 0):
            if no_obstacle(dx, dy) or obstacles[(dx, dy)] == (dx, dy, "E"):
                states.append((dx, dy))
            else:
                break
            dx, dy = dx - 1, dy - 1
        # upper right
        dx, dy = row - 1, col + 1
        while (dx >= 0 and dy < self.total_cols):
            if no_obstacle(dx, dy) or obstacles[(dx, dy)] == (dx, dy, "E"):
                states.append((dx, dy))
            else:
                break
            dx, dy = dx - 1, dy + 1
        # lower left
        dx, dy = row + 1, col - 1
        while (dx < self.total_rows and dy >= 0):
            if no_obstacle(dx, dy) or obstacles[(dx, dy)] == (dx, dy, "E"):
                states.append((dx, dy))
            else:
                break
            dx, dy = dx + 1, dy - 1
        # lower right
        dx, dy = row + 1, col + 1
        while (dx < self.total_rows and dy < self.total_cols):
            if no_obstacle(dx, dy) or obstacles[(dx, dy)] == (dx, dy, "E"):
                states.append((dx, dy))
            else:
                break
            dx, dy = dx + 1, dy + 1
        return states

    def __repr__(self):
        return "Bishop"

class Rook(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = []
        # same row
        dy = col - 1
        while dy >= 0:
            if no_obstacle(row, dy) or obstacles[(row, dy)] == (row, dy, "E"):
                states.append((row, dy))
                dy -= 1
            else:
                break
        dy = col + 1
        while dy < self.total_cols:
            if no_obstacle(row, dy) or obstacles[(row, dy)] == (row, dy, "E"):
                states.append((row, dy))
                dy += 1
            else:
                break

        dx = row - 1
        while dx >= 0:
            if no_obstacle(dx, col) or obstacles[(dx, col)] == (dx, col, "E"):
                states.append((dx, col))
                dx -= 1
            else:
                break
        dx = row + 1
        while dx < self.total_rows:
            if no_obstacle(dx, col) or obstacles[(dx, col)] == (dx, col, "E"):
                states.append((dx, col))
                dx += 1
            else:
                break
        return states

    def __repr__(self):
        return "Rook"

class Knight(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
        vertical = [1, 2, 2, 1, -1, -2, -2, -1]
        states = []
        for i in range(8):
            dx, dy = row - horizontal[i], col - vertical[i]
            if is_within_board(dx, dy, self.total_rows, self.total_cols) and (dx, dy) not in obstacles:
                states.append((dx, dy))
        return states

    def __repr__(self):
        return "Knight"

"""#######################################################################
The code below refers to the generation of the game board.
To initialize the board class, users are expected to provide the size of the board (rows * cols), the number of obstacles,
the position of each obstacles (as a list), the enemies information (type and position, represented as a list), the 
starting position of the King piece, and the goal position(s) of the map.
#######################################################################"""

class Board:
    def __init__(this, rows, cols, obstacles, pieces):
        this.rows = rows
        this.cols = cols
        this.map = []
        for i in range(rows):
            col = []
            for j in range(cols):
                col.append(EMPTY_SPACE)
            this.map.append(col)
        this.obstacles = obstacles
        for obstacle in obstacles:
            this.map[obstacle[0]][obstacle[1]] = OBSTACLE
        this.pieces = pieces
        for pos in pieces:
            if type(pieces[pos]) is King:
                this.map[pos[0]][pos[1]] = ENEMY_KING
            elif type(pieces[pos]) is Queen:
                this.map[pos[0]][pos[1]] = ENEMY_QUEEN
            elif type(pieces[pos]) is Bishop:
                this.map[pos[0]][pos[1]] = ENEMY_BISHOP
            elif type(pieces[pos]) is Rook:
                this.map[pos[0]][pos[1]] = ENEMY_ROOK
            elif type(pieces[pos]) is Knight:
                this.map[pos[0]][pos[1]] = ENEMY_KNIGHT


"""#######################################################################
The code below refers to the actual State of the search space. Each state contains
pieces, which is a hash table of the pieces the board contains in the current state,
and value, which represents the current evaluation function of the state.
#######################################################################"""

class State:
    def __init__(self, pieces, value):
        self.pieces = pieces
        self.value = value

    def print_layout(self):
        print = dict()
        for pos in self.pieces:
            new_pos = (col_mapping[str(pos[1])], pos[0])
            if type(self.pieces[pos]) is King:
                print[new_pos] = "King"
            elif type(self.pieces[pos]) is Queen:
                print[new_pos] = "Queen"
            elif type(self.pieces[pos]) is Bishop:
                print[new_pos] = "Bishop"
            elif type(self.pieces[pos]) is Rook:
                print[new_pos] = "Rook"
            elif type(self.pieces[pos]) is Knight:
                print[new_pos] = "Knight"
        return print

def search():
    row_no, col_no, obstacles, min_piece, pieces = read_data_from_file()
    board = Board(row_no, col_no, obstacles, pieces)
    #board.print(True)
    value_sum = 0
    #the value of a state is the negative sum of the no of pieces that a piece p is threatening, for all p in pieces
    for piece in pieces.values():
        value_sum += -len(piece.threatening)
    initial_state = State(pieces, value_sum)
    again = 1
    count = 0
    #random restart
    while again:
        count += 1
        board = Board(row_no, col_no, obstacles, copy.deepcopy(pieces))
        random_pos = random.choice(list(board.pieces.keys()))
        value = -(len(board.pieces[random_pos].threatening) + len(board.pieces[random_pos].threatened))
        # for each piece that the selected piece is threatening, it is no longer be threatened
        for pos in board.pieces[random_pos].threatening:
            board.pieces[pos].threatened.pop(board.pieces[pos].threatened.index(board.pieces[random_pos]))
        # for each piece that originally threatens the selected piece, it is no longer threatening it
        for each in board.pieces[random_pos].threatened:
            each.threatening.pop(each.threatening.index(random_pos))
        board.pieces.pop(random_pos)
        curr = State(board.pieces, initial_state.value - value)
        board.map[random_pos[0]][random_pos[1]] = EMPTY_SPACE
        while True:
            largest_next = select_next_from(board, curr)
            if largest_next is None:
                break
            if largest_next.value < curr.value:
                print(count)
                #board.print(True)
                return curr.print_layout()
            curr = largest_next

def select_next_from(board, curr):
    # heuristic here will be the no of pairs of pieces threatening each other
    max = 0
    value_table = dict()
    for pos in curr.pieces:
        value = -(len(curr.pieces[pos].threatening) + len(curr.pieces[pos].threatened))
        if value < max:
            max = value
        if value not in value_table:
            value_table[value] = []
        value_table[value].append(pos)
    if len(curr.pieces) < min_piece:
        return None
    if max == 0 and len(curr.pieces) == min_piece:
        return State(curr.pieces, curr.value - 1)
    # random pick a position to remove if there are multiple highest heuristic value to remove
    random_pos = random.choice(list(value_table[max]))
    next = State(curr.pieces, curr.value - value)
    for each in next.pieces[random_pos].threatening:
        next.pieces[each].threatened.pop(next.pieces[each].threatened.index(next.pieces[random_pos]))
    for each in next.pieces[random_pos].threatened:
        each.threatening.pop(each.threatening.index(random_pos))
    next.pieces.pop(random_pos)
    board.map[random_pos[0]][random_pos[1]] = EMPTY_SPACE
    return next

def h(piece, board, curr_pos):
    if piece == None:
        return 0
    positions = piece.get_blocked_positions(curr_pos)
    # print("The blocked positions for the piece at",curr_pos,"is:",positions)
    count = 0
    for pos in positions:
        if board.map[pos.curr_row][pos.curr_col] != EMPTY_SPACE:
            count += 1
    return count

def get_piece_type(board, col, row):
    if board.map[row][col] == ENEMY_KING:
        piece = King(board.rows, board.cols)
    elif board.map[row][col] == ENEMY_QUEEN:
        piece = Queen(board.rows, board.cols)
    elif board.map[row][col] == ENEMY_BISHOP:
        piece = Bishop(board.rows, board.cols)
    elif board.map[row][col] == ENEMY_ROOK:
        piece = Rook(board.rows, board.cols)
    elif board.map[row][col] == ENEMY_KNIGHT:
        piece = Knight(board.rows, board.cols)
    else:
        piece = None
    return piece


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    goalState = search()
    return goalState #Format to be returned


def read_data_from_file():
    testfile = sys.argv[1] # Do not remove. This is your input testfile.
    testfile = open(testfile, "r")
    lines = testfile.readlines()
    row_no, col_no = int(lines[0].replace("Rows:", "")), int(lines[1].replace("Cols:", ""))
    obstacles_no = int(lines[2].replace("Number of Obstacles:", ""))
    obstacle_pos = lines[3].replace("Position of Obstacles (space between):", "").split() if not lines[3].__contains__('-') else []
    for obstacle in obstacle_pos:
        obstacle_x = col_mapping[obstacle[0]]
        obstacle_y = int(obstacle[1:len(obstacle)])
        obstacle = (obstacle_y, obstacle_x)
        obstacles[obstacle] = obstacle
    global min_piece
    min_piece = int(lines[4].replace("K (Minimum number of pieces left in goal):", ""))
    piece_amount = lines[5].replace("Number of King, Queen, Bishop, Rook, Knight (space between):", "").split()
    total_piece = 0
    for n in piece_amount:
        total_piece += int(n)
    pieces = dict()
    for i in range(total_piece):
        piece_data = lines[7 + i].replace("[", "").replace("]", "").split(",")
        piece_pos = (int(piece_data[1][1:len(piece_data[1])]), col_mapping[piece_data[1][0]])
        type = piece_data[0]
        if type == "King":
            piece = King(row_no, col_no, piece_pos)
        elif type == "Queen":
            piece = Queen(row_no, col_no, piece_pos)
        elif type == "Bishop":
            piece = Bishop(row_no, col_no, piece_pos)
        elif type == "Rook":
            piece = Rook(row_no, col_no, piece_pos)
        elif type == "Knight":
            piece = Knight(row_no, col_no, piece_pos)
        assert piece is not None
        pieces[piece_pos] = piece
        piece.threatening.extend(x for x in piece.get_blocked_positions(piece_pos) if x not in piece.threatening)
    for each in pieces.values():
        for pos in each.threatening:
            #print(pieces[pos],"at",pieces[pos].curr_pos,"is threatened by",each,"at",each.curr_pos)
            pieces[pos].threatened.append(each)
    return row_no, col_no, obstacles, min_piece, pieces

if __name__ == "__main__":
    print(run_local())