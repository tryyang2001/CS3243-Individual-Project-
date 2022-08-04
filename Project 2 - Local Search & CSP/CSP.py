import sys
import math
import string
import copy
import time
import random
from queue import PriorityQueue

#Constant defined for better interpretation
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

obstacles = dict()

def is_within_board(row, col, total_row, total_col):
    return row < total_row and row >= 0 and col < total_col and col >= 0

def no_obstacle(row, col):
    return (row, col) not in obstacles

"""#######################################################################
The code below refers to the classes of the chess pieces, including King, Queen, Bishop, Rook and Knight
Each piece class stores information about the movement and generate all the available positions it can move to.
To initialize each piece class, users are expected to provide the total rows and total columns of the game board.
#######################################################################"""

class Piece:
    def __init__(self, rows, cols):
        self.total_rows, self.total_cols = rows, cols
        self.pos = None
        self.threatening = list()

    def __gt__(self, other):
        return other < self

class King(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = set()
        if (self.can_block(row - 1, col, states)):
            states.add((row - 1, col))
        if (self.can_block(row - 1, col + 1, states)):
            states.add((row - 1, col + 1))
        if (self.can_block(row, col + 1, states)):
            states.add((row, col + 1))
        if (self.can_block(row + 1, col + 1, states)):
            states.add((row + 1, col + 1))
        if (self.can_block(row + 1, col, states)):
            states.add((row + 1, col))
        if (self.can_block(row + 1, col - 1, states)):
            states.add((row + 1, col - 1))
        if (self.can_block(row, col - 1, states)):
            states.add((row, col - 1))
        if (self.can_block(row - 1, col - 1, states)):
            states.add((row - 1, col - 1))
        return states

    def can_block(self, row, col, states):
        return (is_within_board(row, col, self.total_rows, self.total_cols) and (row, col) not in obstacles)

    def __repr__(self):
        return "King"

    def get_type(self):
        return "King"

    def __lt__(self, other):
        return True if type(other) is Knight else False

class Queen(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = set()
        states.update(Rook(self.total_rows, self.total_cols).get_blocked_positions(curr_pos))
        states.update(Bishop(self.total_rows, self.total_cols).get_blocked_positions(curr_pos))
        return states

    def __repr__(self):
        return "Queen"

    def get_type(self):
        return "Queen"

    def __lt__(self, other):
        return True

class Bishop(Piece):
    def get_blocked_positions(self, curr_pos):
        states = set()
        row, col = curr_pos[0], curr_pos[1]
        # upper left
        dx, dy = row - 1, col - 1
        while (dx >= 0 and dy >= 0):
            if no_obstacle(dx, dy):
                states.add((dx, dy))
            else:
                break
            dx, dy = dx - 1, dy - 1
        # upper right
        dx, dy = row - 1, col + 1
        while (dx >= 0 and dy < self.total_cols):
            if no_obstacle(dx, dy):
                states.add((dx, dy))
            else:
                break
            dx, dy = dx - 1, dy + 1
        # lower left
        dx, dy = row + 1, col - 1
        while (dx < self.total_rows and dy >= 0):
            if no_obstacle(dx, dy):
                states.add((dx, dy))
            else:
                break
            dx, dy = dx + 1, dy - 1
        # lower right
        dx, dy = row + 1, col + 1
        while (dx < self.total_rows and dy < self.total_cols):
            if no_obstacle(dx, dy):
                states.add((dx, dy))
            else:
                break
            dx, dy = dx + 1, dy + 1
        return states

    def __repr__(self):
        return "Bishop"

    def get_type(self):
        return "Bishop"

    def __lt__(self, other):
        return type(other) is not Queen

class Rook(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = set()
        # same row
        dy = col - 1
        while dy >= 0:
            if no_obstacle(row, dy):
                states.add((row, dy))
                dy -= 1
            else:
                break
        dy = col + 1
        while dy < self.total_cols:
            if no_obstacle(row, dy):
                states.add((row, dy))
                dy += 1
            else:
                break

        dx = row - 1
        while dx >= 0:
            if no_obstacle(dx, col):
                states.add((dx, col))
                dx -= 1
            else:
                break
        dx = row + 1
        while dx < self.total_rows:
            if no_obstacle(dx, col):
                states.add((dx, col))
                dx += 1
            else:
                break
        return states

    def __repr__(self):
        return "Rook"

    def get_type(self):
        return "Rook"

    def __lt__(self, other):
        return type(other) is Knight or type(other) is King

class Knight(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
        vertical = [1, 2, 2, 1, -1, -2, -2, -1]
        states = set()
        for i in range(8):
            dx, dy = row - horizontal[i], col - vertical[i]
            if is_within_board(dx, dy, self.total_rows, self.total_cols) and (dx, dy) not in obstacles:
                states.add((dx, dy))
        return states

    def __repr__(self):
        return "Knight"

    def __lt__(self, other):
        return True if type(other) is King else False

    def get_type(self):
        return "Knight"

"""#######################################################################
The code below refers to the generation of the game board.
To initialize the board class, users are expected to provide the size of the board (rows * cols), the number of obstacles,
the position of each obstacles (as a list), the enemies information (type and position, represented as a list), the 
starting position of the King piece, and the goal position(s) of the map.
#######################################################################"""

class Board:
    def __init__(this, rows, cols, obstacles):
        this.rows = rows
        this.cols = cols
        this.obstacles = obstacles
        this.map = []
        this.size = this.rows * this.cols

class State:
    def __init__(self, obstacles, rows, cols, pieces):
        self.var = pieces
        self.available = set()
        for row in range(rows):
            for col in range(cols):
                if (row, col) in obstacles:
                    continue
                self.available.add((row, col))
def search():
    row_no, col_no, obstacles, pieces = read_data_from_textfile()
    initial_state = State(obstacles, row_no, col_no, pieces)
    return backtracking(initial_state, pieces, dict())

def backtracking_2(state, unassigned, assignment):
    var = select_unassigned_var(unassigned, assignment)
    for value in order_domain_values(state, var, assignment):
        removed_pos = assign(state,var,value[2],unassigned,assignment)
        if len(unassigned) == 0:
            return assignment
        if can_continue(state, unassigned, assignment):
            result = backtracking_2(state, unassigned, assignment)
            if result is not None:
                return result
        remove_assignment(assignment, state, unassigned, var, value[2], removed_pos)
    return None

def can_continue(state, unassigned, assignment):
    next_var = unassigned.pop()
    unassigned.append(next_var)
    return len(order_domain_values(state, next_var, assignment)) > 0

def backtracking(state, unassigned, assignment):
    if len(unassigned) == 0:
        return assignment
    var = select_unassigned_var(unassigned, assignment)
    for value in order_domain_values(state, var, assignment):
        removed_pos = assign(state, var, value[2], unassigned, assignment)
        if forward_checking(state, unassigned):
            result = backtracking(state, unassigned, assignment) #continues with recursion
            if result is not None:
                return result
        #print("Fail assignment for",var)
        remove_assignment(assignment, state, unassigned, var, value[2], removed_pos)
    return None

def remove_assignment(assignment, state, unassigned, var, value, removed_pos):
    pos = (col_mapping[str(value[1])], value[0])
    assignment.pop(pos)
    for pos in removed_pos:
        state.available.add(pos)
    unassigned.append(var)
    state.available.add(value)

def select_unassigned_var(unassigned, assignment):
    selected_var = unassigned.pop()
    unassigned.append(selected_var)
    return selected_var

def order_domain_values(state, var, assignment):
    if len(assignment) == 0:
        return ((0,0,x) for x in state.available)
    lcv_queue = PriorityQueue()
    # for all the available positions to assign, find the one that leads to the least threatening positions
    for pos in state.available:
        threatening = var.get_blocked_positions(pos)
        isAvailable = True
        for each in threatening:
            p = (col_mapping[str(each[1])], each[0])
            if p in assignment:
                isAvailable = False
                break
        if isAvailable:
            lcv = len(threatening)
            tryLater = 0
            if type(var) is Queen and pos[0] == pos[1] == 0:
                tryLater = 1
            lcv_queue.put((lcv, tryLater, pos))
    return lcv_queue.queue


def assign(state, var, value, unassigned, assignment):
    unassigned.pop()
    removed_pos = list()
    pos = (col_mapping[str(value[1])], value[0])
    assignment[pos] = var.get_type()
    state.available.remove(value)
    removed_pos.append(value)
    var.threatening = var.get_blocked_positions(value)
    for pos in var.threatening:
        if pos in state.available:
            state.available.remove(pos)
            removed_pos.append(pos)
    return removed_pos

def forward_checking(state, unassigned):
    if len(state.available) < len(unassigned):
        return False
    return True

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    goalState = search()
    return goalState #Format to be returned


def read_data_from_textfile():
    testfile = sys.argv[1]  # Do not remove. This is your input testfile.
    testfile = open(testfile, 'r')
    lines = testfile.readlines()
    row_no = int(lines[0].replace("Rows:", ""))
    col_no = int(lines[1].replace("Cols:", ""))
    obstacle_no = int(lines[2].replace("Number of Obstacles:", ""))
    obstacle_pos = lines[3].replace("Position of Obstacles (space between):", "").split()
    for i in range(obstacle_no):
        pos = (int(obstacle_pos[i][1:len(obstacle_pos[i])]), col_mapping[obstacle_pos[i][0]])
        obstacles[pos] = pos
    piece_data = lines[4].replace("Number of King, Queen, Bishop, Rook, Knight (space between):", "").split()
    pieces = list()
    for i in range(int(piece_data[4])):
        pieces.append(Knight(row_no, col_no))
    for i in range(int(piece_data[0])):
        pieces.append(King(row_no, col_no))
    random.shuffle(pieces)
    for i in range(int(piece_data[3])):
        pieces.append(Rook(row_no, col_no))
    for i in range(int(piece_data[2])):
        pieces.append(Bishop(row_no, col_no))
    for i in range(int(piece_data[1])):
        pieces.append(Queen(row_no, col_no))
    return row_no, col_no, obstacles, pieces

if __name__ == "__main__":
    start = time.time()
    print(run_CSP())
    #board.print(True)
    print("Time:",time.time()-start)