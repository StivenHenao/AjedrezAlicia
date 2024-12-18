'''
app.py
This file contains the main game loop and logic for the chess game.

Elabaroted by:  Manuel Arango   2259571
                Alex Garcia     2259517
                Sebastian Gomez 2259474
                Stiven Henao    2259603

Teacher:        Joshua Triana
Course:         Artificial Intelligence
Date:           2024 December
'''

import time
import os
import pieces
import random

# Initialize pieces
pieces.initialize_pieces()

# Create lists of white and black pieces
white_pieces = [item for row in pieces.board.white_board for item in row if item and item.color == "White"]
white_pieces.extend(item for row in pieces.board.black_board for item in row if item and item.color == "White")
black_pieces = [item for row in pieces.board.black_board for item in row if item and item.color == "Black"]
black_pieces.extend(item for row in pieces.board.white_board for item in row if item and item.color == "Black")

# Cost table for positional evaluation
cost_table = [
    [50, 30, 30, 30, 30, 30, 30, 50],
    [30, 20, 20, 20, 20, 20, 20, 30],
    [30, 20, 10, 10, 10, 10, 20, 30],
    [30, 20, 10,  0,  0, 10, 20, 30],
    [30, 20, 10,  0,  0, 10, 20, 30],
    [30, 20, 10, 10, 10, 10, 20, 30],
    [30, 20, 20, 20, 20, 20, 20, 30],
    [50, 30, 30, 30, 30, 30, 30, 50]
]

def get_legal_moves(piece):
    # Get all legal moves for a given piece, formatted as a list of details.

    moves = piece.legal_moves(pieces.board.white_board, pieces.board.black_board)
    return [[piece.piece_type, piece.position, piece.color, move, piece.dimension] for move in moves]

def select_piece(position, pieces_list):
    # Find a piece at the specified position in the given list of pieces.

    row, col = int(position[0]), int(position[1])
    for piece in pieces_list:
        if piece.position == (row, col):
            return piece
    return None

def move_piece(piece, new_position):
    # Move a piece to a new position.

    return pieces.move(piece, new_position)

def evaluate_board():
    # Evaluate the board's current state using a heuristic function.

    score = 0
    for row in pieces.board.white_board:
        for piece in row:
            if piece:
                base_value = piece.value
                center_control = cost_table[piece.position[0]][piece.position[1]]
                mobility = len(piece.legal_moves(pieces.board.white_board, pieces.board.black_board))
                if piece.color == "White":
                    score -= base_value + center_control + mobility
                else:
                    score += base_value + center_control + mobility
    return score

def minimax(board, depth, alpha, beta, maximizing):
    # Minimax algorithm with alpha-beta pruning.

    if depth == 0:
        return evaluate_board() + random.uniform(-0.5, 0.5)

    if maximizing:
        max_eval = -float('inf')
        for piece in white_pieces:
            moves = piece.legal_moves(board.white_board, board.black_board)
            moves = filter_promising_moves(piece, moves)
            for move in moves:
                board_copy = board.create_copy()
                pieces.move(piece, move, simulate=True)
                eval_score = minimax(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for piece in black_pieces:
            moves = piece.legal_moves(board.white_board, board.black_board)
            moves = filter_promising_moves(piece, moves)
            for move in moves:
                board_copy = board.create_copy()
                pieces.move(piece, move, simulate=True)
                eval_score = minimax(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval

def find_best_move():
    # Find the best move for the black pieces using Minimax.

    best_moves = []
    best_score = float('inf')
    for piece in black_pieces:
        moves = piece.legal_moves(pieces.board.white_board, pieces.board.black_board)
        moves = filter_promising_moves(piece, moves)
        for move in moves:
            board_copy = pieces.board.create_copy()
            pieces.move(piece, move, simulate=True)
            score = minimax(board_copy, 2, -float('inf'), float('inf'), True)
            if score < best_score:
                best_score = score
                best_moves = [(piece, move)]
            elif score == best_score:
                best_moves.append((piece, move))
    return random.choice(best_moves) if best_moves else None

def filter_promising_moves(piece, moves, max_count=5):
    # Filter and sort moves to prioritize promising ones, such as captures or center moves.

    sorted_moves = sorted(moves, key=lambda move: cost_table[move[0]][move[1]], reverse=True)
    return sorted_moves[:max_count]

def semi_random_move():
    # Select a semi-random move for the black pieces.

    possible_moves = []
    for piece in black_pieces:
        moves = piece.legal_moves(pieces.board.white_board, pieces.board.black_board)
        for move in moves:
            possible_moves.append((piece, move))
    return random.choice(possible_moves) if possible_moves else None

# Main game loop
SEMI_RANDOM_TURNS = 5
current_turn = 0
white_turn = True

while not pieces.end_game():
    os.system("cls")
    pieces.display_board()

    if white_turn:
        while True:
            if pieces.is_check():
                time.sleep(1)
            try:
                position = input("Enter the position of the piece to move (e.g., '12'): ")
                row, col = int(position[0]), int(position[1])
            except ValueError:
                print("Error: Please enter a valid position.")
                continue
            piece = select_piece((row, col), white_pieces)
            if piece:
                moves = get_legal_moves(piece)
                if moves:
                    print("Possible moves: ", [move[3] for move in moves])
                    try:
                        new_position = input("Enter the new position (e.g., '12'): ")
                        row, col = int(new_position[0]), int(new_position[1])
                    except ValueError:
                        print("Error: Please enter a valid position.")
                        continue
                    if move_piece(piece, (row, col)):
                        print(f"Piece moved to {(row, col)}")
                        break
                    else:
                        print("Invalid move.")
                else:
                    print("No legal moves for this piece.")
            else:
                print("Piece not found.")
    else:
        print("Machine's turn.")
        best_move = semi_random_move() if current_turn < SEMI_RANDOM_TURNS else find_best_move()
        if best_move:
            piece, move = best_move
            if move_piece(piece, move):
                print(f"Machine moved {piece.piece_type} to {move}")

    current_turn += 1
    white_turn = not white_turn
    time.sleep(4)

print("Game over.")
