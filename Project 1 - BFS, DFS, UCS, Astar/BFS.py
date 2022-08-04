import enum
import os
import sys
import abc
import string
import math
from queue import Queue
# Helper functions to aid in your implementation. Can edit/remove
EMPTY_SPACE = '0'
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
    "z": 25
}
#Global variables for ease of use
obstacles = dict()
reached = dict()
cost_matrix = list()

def is_within_board(row, col, total_row, total_col):
    return row  < total_row and row  >= 0 and col < total_col and col >= 0

def no_obstacle(row, col):
    return (row, col) not in obstacles

def can_travel(board, col, row):
    return ((row, col) not in board.obstacles and (row, col) not in reached)

"""#######################################################################
The code below refers to the classes of the chess pieces, including King, Queen, Bishop, Rook and Knight
Each piece class stores information about the movement and generate all the available positions it can move to.
To initialize each piece class, users are expected to provide the total rows and total columns of the game board.
#######################################################################"""

class Piece:
    def __init__(self, rows, cols):
        self.total_rows, self.total_cols = rows, cols

class King(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = list()
        if (is_within_board(row - 1, col, self.total_rows, self.total_cols) and no_obstacle(row - 1, col)):
            states.append(State((row - 1, col)))
        if (is_within_board(row - 1, col + 1, self.total_rows, self.total_cols) and no_obstacle(row - 1, col + 1)):
            states.append(State((row - 1, col + 1)))
        if (is_within_board(row, col + 1, self.total_rows, self.total_cols) and no_obstacle(row, col + 1)):
            states.append(State((row, col + 1)))
        if (is_within_board(row + 1, col + 1, self.total_rows, self.total_cols) and no_obstacle(row + 1, col + 1)):
            states.append(State((row + 1, col + 1)))
        if (is_within_board(row + 1, col, self.total_rows, self.total_cols) and no_obstacle(row + 1, col)):
            states.append(State((row + 1, col)))
        if (is_within_board(row + 1, col - 1, self.total_rows, self.total_cols) and no_obstacle(row + 1, col - 1)):
            states.append(State((row + 1, col - 1)))
        if (is_within_board(row , col - 1, self.total_rows, self.total_cols) and no_obstacle(row, col - 1)):
            states.append(State((row, col - 1)))
        if (is_within_board(row - 1, col - 1, self.total_rows, self.total_cols) and no_obstacle(row - 1, col - 1)):
            states.append(State((row - 1, col - 1)))
        return states

    def get_next(self, board, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = list()
        if (is_within_board(row - 1, col, self.total_rows, self.total_cols) and can_travel(board, col, row - 1)):
            states.append(Node(State((row - 1, col))))
        if (is_within_board(row - 1, col + 1, self.total_rows, self.total_cols) and can_travel(board, col + 1, row - 1)):
            states.append(Node(State((row - 1, col + 1))))
        if (is_within_board(row, col + 1, self.total_rows, self.total_cols) and can_travel(board, col + 1, row)):
            states.append(Node(State((row, col + 1))))
        if (is_within_board(row + 1, col + 1, self.total_rows, self.total_cols) and can_travel(board, col + 1, row + 1)):
            states.append(Node(State((row + 1, col + 1))))
        if (is_within_board(row + 1, col, self.total_rows, self.total_cols) and can_travel(board, col, row + 1)):
            states.append(Node(State((row + 1, col))))
        if (is_within_board(row + 1, col - 1, self.total_rows, self.total_cols) and can_travel(board, col - 1, row + 1)):
            states.append(Node(State((row + 1, col - 1))))
        if (is_within_board(row , col - 1, self.total_rows, self.total_cols) and can_travel(board, col - 1, row)):
            states.append(Node(State((row, col - 1))))
        if (is_within_board(row - 1, col - 1, self.total_rows, self.total_cols) and can_travel(board, col - 1, row - 1)):
            states.append(Node(State((row - 1, col - 1))))
        return states

class Queen(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = []
        states.extend(Rook(self.total_rows, self.total_cols).get_blocked_positions(curr_pos))
        states.extend(Bishop(self.total_rows, self.total_cols).get_blocked_positions(curr_pos))
        return states

    def get_next(self, board, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = []
        states.extend(Rook(self.total_rows, self.total_cols).get_next(board, curr_pos))
        states.extend(Bishop(self.total_rows, self.total_cols).get_next(board, curr_pos))
        return states


class Bishop(Piece):
    def get_blocked_positions(self, curr_pos):
        states = []
        row, col = curr_pos[0], curr_pos[1]
        #upper left
        dx, dy = row - 1, col - 1
        while (dx >= 0 and dy >= 0):
            if (no_obstacle(dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx - 1, dy - 1
        #upper right
        dx, dy = row - 1, col + 1
        while (dx >= 0 and dy < self.total_cols):
            if (no_obstacle(dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx - 1, dy + 1
        #lower left
        dx, dy = row + 1, col - 1
        while (dx < self.total_rows and dy >= 0):
            if (no_obstacle(dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx + 1, dy - 1
        #lower right
        dx, dy = row + 1, col + 1
        while (dx < self.total_rows and dy < self.total_cols):
            if (no_obstacle(dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx + 1, dy + 1
        return states

    def get_next(self, board, curr_pos):
        states = []
        row, col = curr_pos[0], curr_pos[1]
        # upper left
        dx, dy = row - 1, col - 1
        while (dx >= 0 and dy >= 0):
            if (can_travel(board, dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx - 1, dy - 1
        # upper right
        dx, dy = row - 1, col + 1
        while (dx >= 0 and dy < self.total_cols):
            if (can_travel(board, dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx - 1, dy + 1
        # lower left
        dx, dy = row + 1, col - 1
        while (dx < self.total_rows and dy >= 0):
            if (can_travel(board, dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx + 1, dy - 1
        # lower right
        dx, dy = row + 1, col + 1
        while (dx < self.total_rows and dy < self.total_cols):
            if (can_travel(board, dx, dy)):
                states.append(State((dx, dy)))
            else:
                break
            dx, dy = dx + 1, dy + 1
        return states

class Rook(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = []
        #same row
        dy = col - 1
        while dy >= 0:
            if no_obstacle(row, dy):
                states.append(State((row, dy)))
                dy -= 1
            else:
                break
        dy = col + 1
        while dy < self.total_cols:
            if no_obstacle(row, dy):
                states.append(State((row, dy)))
                dy += 1
            else:
                break

        dx = row - 1
        while dx >= 0:
            if no_obstacle(dx, col):
                states.append(State((dx, col)))
                dx -= 1
            else:
                break
        dx = row + 1
        while dx < self.total_rows:
            if no_obstacle(dx, col):
                states.append(State((dx, col)))
                dx += 1
            else:
                break
        return states

    def get_next(self, board, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        states = []
        for i in range(self.total_cols):
            if (row, i) == curr_pos:
                continue
            if (can_travel(board, row, i)):
                states.append(State((row, i)))
            else:
                break
        for i in range(self.total_rows):
            if (i, col) == curr_pos:
                continue
            if (can_travel(board, i, col)):
                states.append(State((i, col)))
            else:
                break
        return states

class Knight(Piece):
    def get_blocked_positions(self, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
        vertical = [1, 2, 2, 1, -1, -2, -2, -1]
        states = []
        for i in range(len(horizontal)):
            dx, dy = row - horizontal[i], col - vertical[i]
            if is_within_board(dx, dy, self.total_rows, self.total_cols) and no_obstacle(dx, dy):
                states.append(State((dx, dy)))
        return states
    def get_next(self, board, curr_pos):
        row, col = curr_pos[0], curr_pos[1]
        horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
        vertical = [1, 2, 2, 1, -1, -2, -2, -1]
        states = []
        for i in range(len(horizontal)):
            dx, dy = row - horizontal[i], col - vertical[i]
            if is_within_board(dx, dy, self.total_rows, self.total_cols) and can_travel(board, dx, dy):
                states.append(State((dx, dy)))
        return states

"""#######################################################################
The code below refers to the generation of the game board.
To initialize the board class, users are expected to provide the size of the board (rows * cols), the number of obstacles,
the position of each obstacles (as a list), the enemies information (type and position, represented as a list), the 
starting position of the King piece, and the goal position(s) of the map.
#######################################################################"""

class Board:
    def __init__(this, rows, cols, obstacle_no, obstacles, enemies, start_pos, goal_pos):
        this.rows = rows
        this.cols = cols
        this.obstacle_no = obstacle_no
        this.map = []
        for i in range(rows):
            col = []
            for j in range(cols):
                col.append(EMPTY_SPACE)
            this.map.append(col)
        this.obstacles = obstacles
        for obstacle in obstacles:
            this.map[obstacle[0]][obstacle[1]] = OBSTACLE
        for i in range(len(enemies)):
            type = enemies[i][0]
            if type == "King":
                this.map[enemies[i][1]][enemies[i][2]] = ENEMY_KING
            elif type == "Queen":
                this.map[enemies[i][1]][enemies[i][2]] = ENEMY_QUEEN
            elif type == "Rook":
                this.map[enemies[i][1]][enemies[i][2]] = ENEMY_ROOK
            elif type == "Bishop":
                this.map[enemies[i][1]][enemies[i][2]] = ENEMY_BISHOP
            elif type == "Knight":
                this.map[enemies[i][1]][enemies[i][2]] = ENEMY_KNIGHT
        this.map[start_pos[0]][start_pos[1]] = OWN_KING
        this.start_pos = (start_pos[0], start_pos[1])
        this.goal_pos = goal_pos
        if goal_pos != None:
            for i in range(len(goal_pos)):
                this.map[goal_pos[i][0]][goal_pos[i][1]] = GOAL

    def print(this, show_curs=False):
        if show_curs:
            for i in range(this.rows + 1):
                if i + 1 == this.rows + 1:
                    for length in range(int(math.log(i + 1))):
                        print(" ", end="")
                    print(" | ", end = "")
                    count = 0
                    for c in string.ascii_lowercase:
                        if count >= this.cols:
                            break
                        print(c, end = " | ")
                        count += 1
                    print()
                else:
                    if i < 10:
                        print("",i, end = " | ")
                    else:
                        print(i, end = " | ")
                if i < this.rows:
                    for j in range(this.cols):
                        print(this.map[i][j], end=" | ")
                    print()
        else:
            for i in range(this.rows):
                for j in range(this.cols):
                    print(this.map[i][j], end=" | ")
                print()
        print()

"""#######################################################################
The code below refers to the node of the graph when launching the algorithm, instead of state.
Each state (node) stores the current position of the piece to escape, its parent node (for tracing), and its state (which
is just current position in tuple format)
#######################################################################"""
class State:
    def __init__(self, curr_pos):
        self.curr_row = curr_pos[0]
        self.curr_col = curr_pos[1]
        self.parent = None
    def __repr__(self):
        return "(" + str(chr(97 + self.curr_col)) + "," + str(self.curr_row) + ")"

class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.curr_pos = (state.curr_row, state.curr_col)
    def __repr__(self):
        return "(" + str(chr(97 + self.curr_pos[1])) + "," + str(self.curr_pos[0]) + ")"


"""#######################################################################
The code below refers to the actual searching algorithm adopted in the program
#######################################################################"""

def search():
    board = read_file_and_init_variables()
    #board.print(True)
    frontier, actions, expands = Queue(), list(), list()
    king = King(board.rows, board.cols)
    curr = Node(State(board.start_pos))
    frontier.put(curr)  #push the initial node to frontier
    reached[curr.curr_pos]= True
    nodesExplored = 0
    if curr.curr_pos in board.goal_pos:
        temp = []
        curr_pos = (chr(97 + curr.curr_pos[1]), curr.curr_pos[1])
        temp.append(curr_pos)
        temp.append(curr_pos)
        actions.append(temp)
        nodesExplored += 1
        return actions, nodesExplored
    while not frontier.empty(): #m
        curr = frontier.get()
        board.map[curr.curr_pos[0]][curr.curr_pos[1]] = '@'
        #board.print()
        nodesExplored += 1
        expand = king.get_next(board, curr.curr_pos)
        for node in expand:   #b
            node.parent = curr
            if node.curr_pos in reached:
                continue
            if node.curr_pos in board.goal_pos:
                board.map[node.curr_pos[0]][node.curr_pos[1]] = OWN_KING
                while node.parent is not None:
                    temp = []
                    curr_pos = (chr(97 + node.parent.curr_pos[1]), node.parent.curr_pos[0])
                    next_pos = (chr(97 + node.curr_pos[1]), node.curr_pos[0])
                    temp.append(curr_pos)
                    temp.append(next_pos)
                    actions.append(temp)
                    node = node.parent
                    if node is not None:
                        board.map[node.curr_pos[0]][node.curr_pos[1]] = REACHED
                actions.reverse()
                #board.print(True)
                return actions, nodesExplored
            if node not in reached:
                reached[node.curr_pos] = True
                frontier.put(node)
    #show(obstacles)
    return actions, nodesExplored

def show(obstacles):
    for pos in obstacles:
        print((chr(pos[0] + 97), pos[1]), end = " ")
    print()

def read_file_and_init_variables():
    try:
        filename = sys.argv[1]
        file = open(filename, "r")
        row_no, col_no, obstacle_no, obstacles, enemies, start_pos, goal_pos, cost_matrix = read_board_data(file)
        board = Board(row_no, col_no, obstacle_no, obstacles, enemies, start_pos, goal_pos)
        assert board.start_pos not in board.obstacles
        for goal in board.goal_pos:
            assert goal not in board.obstacles
    except (FileNotFoundError):
        print("File cannot be found")
    except (FileExistsError):
        print("File does not exist1.txt")
    return board


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
#return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type
    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

"""#######################################################################
The code below refers to the reading of the input text file.
It is assume that the input text file is always in a correct input format.
#######################################################################"""

def read_board_data(file):
    lines = file.readlines()
    col_no, obstacle_no, obstacles, row_no = read_board_size_and_obstacles(lines)
    idx, cost_matrix = read_cost(col_no, lines, row_no)
    enemies = read_enemies_data(idx, lines, row_no, col_no, obstacles)
    for enemy in enemies:
        assert (enemy[1], enemy[2]) in obstacles
    start_pos, goal_pos = read_start_and_goal(lines, obstacles)
    return row_no, col_no, obstacle_no, obstacles, enemies, start_pos, goal_pos, cost_matrix

def read_start_and_goal(lines, obstacles):
    idx = -1
    goal_pos = []
    for i in range(4, len(lines)):
        if lines[i].__contains__("Starting Position of Pieces [Piece, Pos]:"):
            idx = i + 1
    if idx != -1:
        str = lines[idx]
        start_pos = (int(str[str.index(',') + 2: str.index(']')]), col_mapping[str[str.index(',') + 1]])
        if start_pos in obstacles:
            obstacles.pop(start_pos)
    else:
        start_pos = None
    if lines[-1].__contains__("Goal Positions (space between):"):
        str = lines[-1].replace("Goal Positions (space between):", "")
        if (str == "-"):
            goal_pos = None
        else:
            str = str.split()
            for goal in str:
                goal = (int(goal[1:len(goal)]), col_mapping[goal[0]])
                goal_pos.append(goal)
                if goal in obstacles:
                    obstacles.pop(goal)
    else:
        goal_pos = None #no goal
    return start_pos, goal_pos

def read_enemies_data(idx, lines, row_no, col_no, obstacles):
    enemy_count = lines[idx].replace("Number of Enemy King, Queen, Bishop, Rook, Knight (space between):", "").split()
    total_enemy = 0
    enemies = []
    idx += 2
    for i in range(len(enemy_count)):
        total_enemy += int(enemy_count[i])
    #mark enemy positions as obstacles
    for num in range(total_enemy):
        data = lines[idx].replace('[', "").replace(']', "").split(',')
        data_piece = data[0]
        data_pos = data[1]
        data_row = int(data_pos[1:len(data_pos)])
        data_col = col_mapping[data_pos[0]]
        enemies.append((data_piece, data_row, data_col))
        obstacles[(data_row, data_col)] = (data_row, data_col)
        assert (data_row, data_col) in obstacles
        idx += 1

    # according to type of piece, set position as obstacle
    for enemy in enemies:
        curr_row, curr_col = enemy[1], enemy[2]
        enemy = get_piece(enemy[0], row_no, col_no)
        cannot_go = []
        cannot_go = enemy.get_blocked_positions((curr_row, curr_col))
        if cannot_go is not None:
            for block in cannot_go:
                tuple = (block.curr_row, block.curr_col)
                obstacles[tuple] = tuple
    return enemies

def get_piece(piece, rows, cols):
    if piece == "King":
        return King(rows, cols)
    elif piece == "Queen":
        return Queen(rows, cols)
    elif piece == "Rook":
        return Rook(rows, cols)
    elif piece == "Bishop":
        return Bishop(rows, cols)
    elif piece == "Knight":
        return Knight(rows, cols)

def print_cost_matrix():
    for i in range(len(cost_matrix)):
        print(cost_matrix[i])

def read_cost(col_no, lines, row_no):
    cost_matrix = init_cost_matrix(col_no, row_no)
    for i in range(len(lines)):
        curr = i + 5
        if (lines[curr].__contains__("Number of Enemy King, Queen, Bishop, Rook, Knight (space between):")):
            idx = curr
            break
        data = lines[curr].replace('[', "").replace(']', "").split(',')
        data_row = int(data[0][1:len(data[0])])
        data_col = int(col_mapping[data[0][0]])
        cost_matrix[data_row][data_col] = int(data[1])
    return idx, cost_matrix


def init_cost_matrix(col_no, row_no):
    cost_matrix = []
    for i in range(row_no):
        cost_cols = []
        for j in range(col_no):
            cost_cols.append(1)
        cost_matrix.append(cost_cols)
    return cost_matrix


def read_board_size_and_obstacles(lines):
    row_no = int(lines[0].replace("Rows:", ""))
    col_no = int(lines[1].replace("Cols:", ""))
    obstacle_no = int(lines[2].replace("Number of Obstacles:", ""))
    str = lines[3].replace("Position of Obstacles (space between):", "").split()
    for pos in str:
        obstacle = (int(pos[1:len(pos)]), col_mapping[pos[0]])
        obstacles[obstacle] = obstacle
    return col_no, obstacle_no, obstacles, row_no

"""#######################################################################
The code below is the main code to execute the program. It is assume that the directory exists and the file(s) can be found.
#######################################################################"""

if __name__ == "__main__":
    print(run_BFS())

"""
for filename in os.listdir("Public Testcases"):
    file = open("Public Testcases/" + filename)
    row_no, col_no, obstacle_no, obstacles, enemies, start_pos, goal_pos = read_board_data(file)
    board = Board(row_no, col_no, obstacle_no, obstacles, enemies, start_pos, goal_pos)
    board.print(True)
    print()
"""


