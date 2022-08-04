import sys
import math
import string
import enum
import random

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Constant defined for better interpretation
EMPTY_SPACE = ' '
WHITE_KING = '♔'
WHITE_QUEEN = '♕'
WHITE_BISHOP = '♗'
WHITE_ROOK = '♖'
WHITE_KNIGHT = '♘'
WHITE_PAWN = '♙'
BLACK_KING = '♚'
BLACK_QUEEN = '♛'
BLACK_BISHOP = '♝'
BLACK_ROOK = '♜'
BLACK_KNIGHT = '♞'
BLACK_PAWN = '♟'

POS_INF = sys.maxsize
NEG_INF = -sys.maxsize - 1
DLS_DEPTH = 2

# The heuristic used is all white pieces value - all black pieces value +/- checking value
KING_VALUE = 100000;
QUEEN_VALUE = 2200; #2000
BISHOP_VALUE = 1000; #650
ROOK_VALUE = 1200; #1000
KNIGHT_VALUE = 800; #600
PAWN_VALUE = 150; #200
CHECKING_VALUE = 150

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
    "0": "a",
    "1": "b",
    "2": "c",
    "3": "d",
    "4": "e",
    "5": "f",
    "6": "g",
    "7": "h",
    "8": "i",
    "9": "j",
    "10": "k",
    "11": "l",
    "12": "m",
    "13": "n",
    "14": "o",
    "15": "p",
    "16": "q",
    "17": "r",
    "18": "s",
    "19": "t",
    "20": "u",
    "21": "v",
    "22": "w",
    "23": "x",
    "24": "y",
    "25": "z"
}

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    def __init__(self, pos, colour):
        self.total_rows, self.total_cols = 5, 5
        self.curr_pos = pos
        self.colour = colour

    def is_within_board(self, row, col):
        return row >= 0 and row < self.total_rows and col >= 0 and col < self.total_cols

    def can_occupy(self, pos):
        return pos not in state.own_occupied and pos not in state.enemy_occupied

class Knight(Piece):
    def get_attack_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
        vertical = [1, 2, 2, 1, -1, -2, -2, -1]
        states = set()
        for i in range(8):
            dx, dy = row - horizontal[i], col - vertical[i]
            if self.colour == "White":
                if super().is_within_board(dx, dy) and (dx, dy) in state.enemy_occupied:
                    states.add((dx, dy))
            else:
                if super().is_within_board(dx, dy) and (dx, dy) in state.own_occupied:
                    states.add((dx, dy))
        return states

    def get_next_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
        vertical = [1, 2, 2, 1, -1, -2, -2, -1]
        states = set()
        for i in range(8):
            dx, dy = row - horizontal[i], col - vertical[i]
            if super().is_within_board(dx, dy) and super().can_occupy((dx, dy)):
                states.add((dx, dy))
        return states

    def value(self):
        return KNIGHT_VALUE if self.colour == "White" else -KNIGHT_VALUE

    def __repr__(self):
        return self.colour + " Knight"

class Rook(Piece):
    def get_attack_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        states = set()
        if self.colour == "White":
            # same row
            dy = col - 1
            while dy >= 0:
                if (row, dy) in state.enemy_occupied:
                    states.add((row, dy))
                    break
                elif  (row, dy) in state.own_occupied:
                    break
                else:
                    dy -= 1
            dy = col + 1
            while dy < self.total_cols:
                if (row, dy) in state.enemy_occupied:
                    states.add((row, dy))
                    break
                elif (row, dy) in state.own_occupied:
                    break
                else:
                    dy += 1
            #same col
            dx = row - 1
            while dx >= 0:
                if (dx, col) in state.enemy_occupied:
                    states.add((dx, col))
                    break
                elif (dx, col) in state.own_occupied:
                    break
                else:
                    dx -= 1
            dx = row + 1
            while dx < self.total_rows:
                if (dx, col) in state.enemy_occupied:
                    states.add((dx, col))
                    break
                elif (dx, col) in state.own_occupied:
                    break
                else:
                    dx += 1
            return states
        else:
            # same row
            dy = col - 1
            while dy >= 0:
                if (row, dy) in state.own_occupied:
                    states.add((row, dy))
                    break
                elif (row, dy) in state.enemy_occupied:
                    break
                else:
                    dy -= 1
            dy = col + 1
            while dy < self.total_cols:
                if (row, dy) in state.own_occupied:
                    states.add((row, dy))
                    break
                elif (row, dy) in state.enemy_occupied:
                    break
                else:
                    dy += 1
            #same col
            dx = row - 1
            while dx >= 0:
                if (dx, col) in state.own_occupied:
                    states.add((dx, col))
                    break
                elif (dx, col) in state.enemy_occupied:
                    break
                else:
                    dx -= 1
            dx = row + 1
            while dx < self.total_rows:
                if (dx, col) in state.own_occupied:
                    states.add((dx, col))
                    break
                elif (dx, col) in state.enemy_occupied:
                    break
                else:
                    dx += 1
            return states

    def get_next_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        states = set()
        # same row
        dy = col - 1
        while dy >= 0:
            if (row, dy) not in state.own_occupied and (row, dy) not in state.enemy_occupied:
                states.add((row, dy))
                dy -= 1
            else:
                break
        dy = col + 1
        while dy < self.total_cols:
            if (row, dy) not in state.own_occupied and (row, dy) not in state.enemy_occupied:
                states.add((row, dy))
                dy += 1
            else:
                break
        # same col
        dx = row - 1
        while dx >= 0:
            if (dx, col) not in state.own_occupied and (dx, col) not in state.enemy_occupied:
                states.add((dx, col))
                dx -= 1
            else:
                break
        dx = row + 1
        while dx < self.total_rows:
            if (dx, col) not in state.own_occupied and (dx, col) not in state.enemy_occupied:
                states.add((dx, col))
                dx += 1
            else:
                break
        return states

    def value(self):
        return ROOK_VALUE if self.colour == "White" else -ROOK_VALUE

    def __repr__(self):
        return self.colour + " Rook"

class Bishop(Piece):
    def get_attack_positions(self):
        states = set()
        row, col = self.curr_pos[0], self.curr_pos[1]
        # upper left
        dx, dy = row - 1, col - 1
        if self.colour == "White":
            while (dx >= 0 and dy >= 0):
                if (dx, dy) in state.enemy_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.own_occupied:
                    break
                dx, dy = dx - 1, dy - 1
            # upper right
            dx, dy = row - 1, col + 1
            while (dx >= 0 and dy < self.total_cols):
                if (dx, dy) in state.enemy_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.own_occupied:
                    break
                dx, dy = dx - 1, dy + 1
            # lower left
            dx, dy = row + 1, col - 1
            while (dx < self.total_rows and dy >= 0):
                if (dx, dy) in state.enemy_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.own_occupied:
                    break
                dx, dy = dx + 1, dy - 1
            # lower right
            dx, dy = row + 1, col + 1
            while (dx < self.total_rows and dy < self.total_cols):
                if (dx, dy) in state.enemy_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.own_occupied:
                    break
                dx, dy = dx + 1, dy + 1
            return states
        else:
            while (dx >= 0 and dy >= 0):
                if (dx, dy) in state.own_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.enemy_occupied:
                    break
                dx, dy = dx - 1, dy - 1
            # upper right
            dx, dy = row - 1, col + 1
            while (dx >= 0 and dy < self.total_cols):
                if (dx, dy) in state.own_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.enemy_occupied:
                    break
                dx, dy = dx - 1, dy + 1
            # lower left
            dx, dy = row + 1, col - 1
            while (dx < self.total_rows and dy >= 0):
                if (dx, dy) in state.own_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.enemy_occupied:
                    break
                dx, dy = dx + 1, dy - 1
            # lower right
            dx, dy = row + 1, col + 1
            while (dx < self.total_rows and dy < self.total_cols):
                if (dx, dy) in state.own_occupied:
                    states.add((dx, dy))
                    break
                elif (dx, dy) in state.enemy_occupied:
                    break
                dx, dy = dx + 1, dy + 1
            return states

    def get_next_positions(self):
        states = set()
        row, col = self.curr_pos[0], self.curr_pos[1]
        # upper left
        dx, dy = row - 1, col - 1
        while (dx >= 0 and dy >= 0):
            if (dx, dy) not in state.own_occupied and (dx, dy) not in state.enemy_occupied:
                states.add((dx, dy))
            else:
                break
            dx, dy = dx - 1, dy - 1
        # upper right
        dx, dy = row - 1, col + 1
        while (dx >= 0 and dy < self.total_cols):
            if (dx, dy) not in state.own_occupied and (dx, dy) not in state.enemy_occupied:
                states.add((dx, dy))
            else:
                break
            dx, dy = dx - 1, dy + 1
        # lower left
        dx, dy = row + 1, col - 1
        while (dx < self.total_rows and dy >= 0):
            if (dx, dy) not in state.own_occupied and (dx, dy) not in state.enemy_occupied:
                states.add((dx, dy))
            else:
                break
            dx, dy = dx + 1, dy - 1
        # lower right
        dx, dy = row + 1, col + 1
        while (dx < self.total_rows and dy < self.total_cols):
            if (dx, dy) not in state.own_occupied and (dx, dy) not in state.enemy_occupied:
                states.add((dx, dy))
            else:
                break
            dx, dy = dx + 1, dy + 1
        return states

    def value(self):
        return BISHOP_VALUE if self.colour == "White" else -BISHOP_VALUE

    def __repr__(self):
        return self.colour + " Bishop"

class Queen(Piece):
    def get_attack_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        states = set()
        states.update(Rook(self.curr_pos, self.colour).get_attack_positions())
        states.update(Bishop(self.curr_pos, self.colour).get_attack_positions())
        return states

    def get_next_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        states = set()
        states.update(Rook(self.curr_pos, self.colour).get_next_positions())
        states.update(Bishop(self.curr_pos, self.colour).get_next_positions())
        return states

    def value(self):
        return QUEEN_VALUE if self.colour == "White" else -QUEEN_VALUE

    def __repr__(self):
        return self.colour + " Queen"

class King(Piece):
    def get_attack_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        states = set()
        if self.colour == "White":
            if super().is_within_board(row - 1, col) and (row - 1, col) in state.enemy_occupied:
                states.add((row - 1, col))
            if super().is_within_board(row - 1, col + 1) and (row - 1, col + 1) in state.enemy_occupied:
                states.add((row - 1, col + 1))
            if super().is_within_board(row, col + 1) and (row, col + 1) in state.enemy_occupied:
                states.add((row, col + 1))
            if super().is_within_board(row + 1, col + 1) and (row + 1, col + 1) in state.enemy_occupied:
                states.add((row + 1, col + 1))
            if super().is_within_board(row + 1, col) and (row + 1, col) in state.enemy_occupied:
                states.add((row + 1, col))
            if super().is_within_board(row + 1, col - 1) and (row + 1, col - 1) in state.enemy_occupied:
                states.add((row + 1, col - 1))
            if super().is_within_board(row, col - 1) and (row, col - 1) in state.enemy_occupied:
                states.add((row, col - 1))
            if super().is_within_board(row - 1, col - 1) and (row - 1, col - 1) in state.enemy_occupied:
                states.add((row - 1, col - 1))
        else:
            if super().is_within_board(row - 1, col) and (row - 1, col) in state.own_occupied:
                states.add((row - 1, col))
            if super().is_within_board(row - 1, col + 1) and (row - 1, col + 1) in state.own_occupied:
                states.add((row - 1, col + 1))
            if super().is_within_board(row, col + 1) and (row, col + 1) in state.own_occupied:
                states.add((row, col + 1))
            if super().is_within_board(row + 1, col + 1) and (row + 1, col + 1) in state.own_occupied:
                states.add((row + 1, col + 1))
            if super().is_within_board(row + 1, col) and (row + 1, col) in state.own_occupied:
                states.add((row + 1, col))
            if super().is_within_board(row + 1, col - 1) and (row + 1, col - 1) in state.own_occupied:
                states.add((row + 1, col - 1))
            if super().is_within_board(row, col - 1) and (row, col - 1) in state.own_occupied:
                states.add((row, col - 1))
            if super().is_within_board(row - 1, col - 1) and (row - 1, col - 1) in state.own_occupied:
                states.add((row - 1, col - 1))
        return states

    def get_next_positions(self):
        row, col = self.curr_pos[0], self.curr_pos[1]
        states = set()
        if super().is_within_board(row - 1, col) and super().can_occupy((row - 1, col)):
            states.add((row - 1, col))
        if super().is_within_board(row - 1, col + 1) and super().can_occupy((row - 1, col + 1)):
            states.add((row - 1, col + 1))
        if super().is_within_board(row, col + 1) and super().can_occupy((row, col + 1)):
            states.add((row, col + 1))
        if super().is_within_board(row + 1, col + 1) and super().can_occupy((row + 1, col + 1)):
            states.add((row + 1, col + 1))
        if super().is_within_board(row + 1, col) and super().can_occupy((row + 1, col)):
            states.add((row + 1, col))
        if super().is_within_board(row + 1, col - 1) and super().can_occupy((row + 1, col - 1)):
            states.add((row + 1, col - 1))
        if super().is_within_board(row, col - 1) and super().can_occupy((row, col - 1)):
            states.add((row, col - 1))
        if super().is_within_board(row - 1, col - 1) and super().can_occupy((row - 1, col - 1)):
            states.add((row - 1, col - 1))
        return states

    def value(self):
        return KING_VALUE if self.colour == "White" else -KING_VALUE

    def __repr__(self):
        return self.colour + " King"

class Pawn(Piece):
    def get_attack_positions(self):
        states = set()
        row, col = self.curr_pos[0], self.curr_pos[1]
        if self.colour == "White":
            if super().is_within_board(row + 1, col - 1) and (row + 1, col - 1) in state.enemy_occupied:
                states.add((row + 1, col - 1))
            if super().is_within_board(row + 1, col + 1) and (row + 1, col + 1) in state.enemy_occupied:
                states.add((row + 1, col + 1))
        elif self.colour == "Black":
            if super().is_within_board(row - 1, col - 1) and (row - 1, col - 1) in state.own_occupied:
                states.add((row - 1, col - 1))
            if super().is_within_board(row - 1, col + 1) and (row - 1, col + 1) in state.own_occupied:
                states.add((row - 1, col + 1))
        return states

    def get_next_positions(self):
        states = set()
        row, col = self.curr_pos[0], self.curr_pos[1]
        if self.colour == "White":
            if super().is_within_board(row + 1, col) and super().can_occupy((row + 1, col)):
                states.add((row + 1, col))
        elif self.colour == "Black":
            if super().is_within_board(row - 1, col) and super().can_occupy((row - 1, col)):
                states.add((row - 1, col))
        return states

    def value(self):
        return PAWN_VALUE if self.colour == "White" else -PAWN_VALUE

    def __repr__(self):
        return self.colour + " Pawn"

class Move:
    def __init__(self, curr, next, piece):
        self.from_pos = curr
        self.to_pos = next
        self.piece = piece

    def __repr__(self):
        return self.piece.__repr__() + "(" + str(self.from_pos[0]) + "," + str(self.from_pos[1]) + \
               ")->(" + str(self.to_pos[0]) + "," + str(self.to_pos[1]) + ")"

class Game:
    pass

class State:
    def __init__(self, gameboard):
        self.total_rows = self.total_cols = 5
        self.gameboard = gameboard
        self.own_pieces = set()
        self.enemy_pieces = set()
        self.own_occupied = set()
        self.enemy_occupied = set()
        #represent gameboard for better debugging, can remove later...
        self.map = list()
        for i in range(5):
            self.map.append([])
            for j in range(5):
                self.map[i].append(EMPTY_SPACE)
        for pos in gameboard:
            piece_type = gameboard[pos][0]
            piece_color = gameboard[pos][1]
            if piece_type == "King":
                self.map[pos[0]][pos[1]] = BLACK_KING if piece_color == "Black" else WHITE_KING
            elif piece_type == "Queen":
                self.map[pos[0]][pos[1]] = BLACK_QUEEN if piece_color == "Black" else WHITE_QUEEN
            elif piece_type == "Bishop":
                self.map[pos[0]][pos[1]] = BLACK_BISHOP if piece_color == "Black" else WHITE_BISHOP
            elif piece_type == "Rook":
                self.map[pos[0]][pos[1]] = BLACK_ROOK if piece_color == "Black" else WHITE_ROOK
            elif piece_type == "Knight":
                self.map[pos[0]][pos[1]] = BLACK_KNIGHT if piece_color == "Black" else WHITE_KNIGHT
            elif piece_type == "Pawn":
                self.map[pos[0]][pos[1]] = BLACK_PAWN if piece_color == "Black" else WHITE_PAWN
        for pos in gameboard:
            piece_type = gameboard[pos][0]
            piece_color = gameboard[pos][1]
            piece = None
            if piece_color == "Black":
                self.enemy_occupied.add(pos)
                if piece_type == "King":
                    piece = King(pos, "Black")
                    self.enemy_king = piece
                elif piece_type == "Queen":
                    piece = Queen(pos, "Black")
                elif piece_type == "Bishop":
                    piece = Bishop(pos, "Black")
                elif piece_type == "Rook":
                    piece = Rook(pos, "Black")
                elif piece_type == "Knight":
                    piece = Knight(pos, "Black")
                elif piece_type == "Pawn":
                    piece = Pawn(pos, "Black")
                self.enemy_pieces.add(piece)
            else:
                self.own_occupied.add(pos)
                if piece_type == "King":
                    piece = King(pos, "White")
                    self.own_king = piece
                elif piece_type == "Queen":
                    piece = Queen(pos, "White")
                elif piece_type == "Bishop":
                    piece = Bishop(pos, "White")
                elif piece_type == "Rook":
                    piece = Rook(pos, "White")
                elif piece_type == "Knight":
                    piece = Knight(pos, "White")
                elif piece_type == "Pawn":
                    piece = Pawn(pos, "White")
                self.own_pieces.add(piece)
            self.gameboard[pos] = piece

    def is_checking_enemy_king(self, action):
        if action.to_pos == self.enemy_king.curr_pos:
            return True
        return False

    def is_checking_own_king(self, action):
        if action.to_pos == self.own_king.curr_pos:
            return True
        return False

    def get_actions(self, is_max_turn):
        actions = list()
        if is_max_turn:
            for piece in self.own_pieces:
                positions = piece.get_attack_positions()
                positions.update(piece.get_next_positions())
                for pos in positions:
                    action = Move(piece.curr_pos, pos, piece)
                    actions.append(action)
            return actions
        else:
            for piece in self.enemy_pieces:
                positions = piece.get_attack_positions()
                positions.update(piece.get_next_positions())
                for pos in positions:
                    action = Move(piece.curr_pos, pos, piece)
                    actions.append(action)
            return actions

    def perform_action(self, move, is_max_turn):
        removed_piece = None
        piece = self.gameboard[move.from_pos]
        piece.curr_pos = move.to_pos
        if is_max_turn:
            self.own_occupied.remove(move.from_pos)
            self.own_occupied.add(move.to_pos)
            if move.to_pos in self.enemy_occupied:
                self.enemy_occupied.remove(move.to_pos)
                removed_piece = self.gameboard[move.to_pos]
                self.enemy_pieces.remove(self.gameboard[move.to_pos])
        else:
            self.enemy_occupied.remove(move.from_pos)
            self.enemy_occupied.add(move.to_pos)
            if move.to_pos in self.own_occupied:
                self.own_occupied.remove(move.to_pos)
                removed_piece = self.gameboard[move.to_pos]
                self.own_pieces.remove(self.gameboard[move.to_pos])
        self.gameboard[move.to_pos] = piece
        self.gameboard.pop(move.from_pos)
        return removed_piece

    def undo_action(self, move, removed_piece, is_max_turn):
        piece = self.gameboard[move.to_pos]
        piece.curr_pos = move.from_pos
        if is_max_turn:
            self.own_occupied.remove(move.to_pos)
            self.own_occupied.add(move.from_pos)
            if removed_piece is not None:
                self.enemy_occupied.add(move.to_pos)
                self.enemy_pieces.add(removed_piece)
                self.gameboard[move.to_pos] = removed_piece
        else:
            self.enemy_occupied.remove(move.to_pos)
            self.enemy_occupied.add(move.from_pos)
            if removed_piece is not None:
                self.own_occupied.add(move.to_pos)
                self.own_pieces.add(removed_piece)
                self.gameboard[move.to_pos] = removed_piece
        self.gameboard[move.from_pos] = piece
        return None

    def get_state_value(self):
        value = 0
        for piece in self.own_pieces:
            value += piece.value()
        for piece in self.enemy_pieces:
            value += piece.value()
        return value


# Implement your minimax with alpha-beta pruning algorithm here.
def ab():
    is_max_turn = True
    depth = DLS_DEPTH
    best_action = None
    possible_actions = state.get_actions(is_max_turn)
    best_value = NEG_INF
    alpha, beta = NEG_INF, POS_INF
    for action in possible_actions:
        # do the action
        removed_piece = state.perform_action(action, is_max_turn)
        miniMax_value = get_minimax_value(not is_max_turn, depth - 1, alpha, beta)
        # undo the action
        state.undo_action(action, removed_piece, is_max_turn)
        if miniMax_value >= best_value:
            best_value = miniMax_value
            best_action = action
    return best_action

def get_minimax_value(is_max_turn, depth, alpha, beta):
    if depth == 0:
        return state.get_state_value()
    possible_actions = state.get_actions(is_max_turn)
    if is_max_turn:
        best_value = NEG_INF
        for action in possible_actions:
            #perform the action first
            removed_piece = state.perform_action(action, is_max_turn)
            curr_minimax_value = get_minimax_value(not is_max_turn, depth - 1, alpha, beta)
            if state.is_checking_enemy_king(action):
                curr_minimax_value += CHECKING_VALUE
            if curr_minimax_value > best_value:
                best_value = curr_minimax_value
            elif curr_minimax_value == best_value:
                to_change = random.randint(0,1)
                if to_change == 1:
                    best_value = curr_minimax_value
            #undo the action
            state.undo_action(action, removed_piece, is_max_turn)
            if curr_minimax_value > alpha:
                alpha = curr_minimax_value
            elif curr_minimax_value == alpha:
                to_change = random.randint(0,1)
                if to_change == 1:
                    alpha = curr_minimax_value
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = POS_INF
        for action in possible_actions:
            # do action
            removed_piece = state.perform_action(action, is_max_turn)
            curr_minimax_value = get_minimax_value(not is_max_turn, depth - 1, alpha, beta)
            if state.is_checking_own_king(action):
                curr_minimax_value -= CHECKING_VALUE
            if curr_minimax_value < best_value:
                best_value = curr_minimax_value
            elif curr_minimax_value == best_value:
                to_change = random.randint(0,1)
                if to_change == 1:
                    best_value = curr_minimax_value
            # undo action
            state.undo_action(action, removed_piece, is_max_turn)
            if curr_minimax_value < beta:
                beta = curr_minimax_value
            elif curr_minimax_value == beta:
                to_change = random.randint(0,1)
                if to_change == 1:
                    beta = curr_minimax_value
            if beta <= alpha:
                break
        return best_value

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    processed_gameboard = dict()
    for pos in gameboard:
        std_pos = (pos[1], col_mapping[pos[0]])
        processed_gameboard[std_pos] = gameboard[pos]
    global state
    state = State(processed_gameboard)
    best_move = ab()
    move = ((col_mapping[str(best_move.from_pos[1])], best_move.from_pos[0]),
            (col_mapping[str(best_move.to_pos[1])], best_move.to_pos[0]))
    return move  # Format to be returned (('a', 0), ('b', 3))
