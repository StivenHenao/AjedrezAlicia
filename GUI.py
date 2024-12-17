'''
GUI class
This class is responsible for the graphical user interface of the chess game.

Elabaroted by:  Manuel Arango   2259571
                Alex Garcia     2259517
                Sebastian Gomez 2259474
                Stiven Henao    2259603

Teacher:        Joshua Triana
Course:         Artificial Intelligence
Date:           2024 December
'''

import tkinter as tk
from tkinter import messagebox
import pieces  # Ensure you import your "pieces" module
import random

# Initialize pieces
pieces.initialize_pieces()

# Boards
board1 = pieces.board.white_board
board2 = pieces.board.black_board

# Create the main window
root = tk.Tk()
root.title("Chess with Two Boards")

# Cell size configuration
CELL_SIZE = 50

# Board colors
COLOR1 = "white"
COLOR2 = "lightgray"
HIGHLIGHT_COLOR = "lightgreen"  # Highlight possible moves

# Canvases for the two boards
canvas1 = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE)
canvas1.grid(row=0, column=0, padx=10, pady=10)

canvas2 = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE)
canvas2.grid(row=0, column=1, padx=10, pady=10)

# Area to display messages
info_label = tk.Label(root, text="", font=("Arial", 14), padx=10, pady=5, anchor='w')
info_label.grid(row=1, column=0, columnspan=2, sticky="w")

# Dictionary of Unicode symbols for chess pieces
PIECE_SYMBOLS = {
    "King": {"White": "♔", "Black": "♚"},
    "Queen": {"White": "♕", "Black": "♛"},
    "Rook": {"White": "♖", "Black": "♜"},
    "Bishop": {"White": "♗", "Black": "♝"},
    "Knight": {"White": "♘", "Black": "♞"},
    "Pawn": {"White": "♙", "Black": "♟"}
}

def draw_board(canvas, board, highlighted_moves=None):
    canvas.delete("all")  # Clear the canvas
    for row in range(8):
        for col in range(8):
            # Determine the color of the cell
            if highlighted_moves and (row, col) in highlighted_moves:
                color = HIGHLIGHT_COLOR  # Highlight possible moves
            else:
                color = COLOR1 if (row + col) % 2 == 0 else COLOR2

            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            # Draw rectangle
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            # Draw pieces (if present)
            piece = board[row][col]
            if piece:
                symbol = PIECE_SYMBOLS[piece.piece_type][piece.color]  # Get Unicode symbol
                canvas.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2,
                    text=symbol,
                    fill="black" if piece.color == "Black" else "red",
                    font=("Arial", 28, "bold")
                )

# Update boards and display messages
def update_boards(highlighted_moves=None):
    # Updates both boards. Can receive highlighted moves for one board.

    draw_board(canvas1, board1, highlighted_moves if current_board == board1 else None)
    draw_board(canvas2, board2, highlighted_moves if current_board == board2 else None)

# Selection and movement logic
selected_piece = None  # Selected piece
white_turn = True  # Initial turn
current_board = None  # Identifies which board is active
highlighted_moves = []  # List of possible moves to highlight

def board_click(event, board, canvas):
    # Handles clicks on a specific board.

    global selected_piece, white_turn, current_board, highlighted_moves
    if not white_turn:
        return  # Do not allow moves if it's not the player's turn

    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE
    if selected_piece is None:
        # Select piece
        selected_piece = board[row][col]
        current_board = board  # Save the current board
        if selected_piece and selected_piece.color == "White":
            info_label.config(text=f"🔹 Selected piece: {selected_piece.piece_type} at position ({row}, {col}).")
            highlighted_moves = selected_piece.legal_moves(board1, board2)
            update_boards(highlighted_moves)  # Highlight moves
        else:
            info_label.config(text="⚠️ No selectable piece at that position.")
            selected_piece = None
    else:
        # Attempt to move the piece
        if (row, col) in highlighted_moves and pieces.move(selected_piece, (row, col)):
            captured = pieces.move(selected_piece, (row, col))
            if captured:
                info_label.config(text=f"🗑️ Captured piece: {PIECE_SYMBOLS[captured.piece_type][captured.color]} removed from the board.")
            else:
                info_label.config(text=f"✅ Moving {selected_piece.piece_type} to position ({row}, {col}) on board "
                                       f"{'1' if board is board1 else '2'}.")
            selected_piece = None  # Reset selection
            highlighted_moves = []  # Clear highlighted moves
            update_boards()
            white_turn = False
            root.after(1000, robot_turn)  # Wait 1 second and give the turn to the robot
        else:
            info_label.config(text="❌ Invalid move. Try another position.")
            selected_piece = None
            highlighted_moves = []  # Clear highlighted moves
            update_boards()


# Robot's turn
def robot_turn():
    # Logic for the robot's turn. Plays on both boards.

    global white_turn
    info_label.config(text="\n🤖 Robot's turn...")

    # Determine possible moves on both boards
    best_move_1 = semi_random_move(board1)
    best_move_2 = semi_random_move(board2)

    # Choose a move randomly between the two boards
    if best_move_1 and best_move_2:
        best_move = random.choice([best_move_1, best_move_2])
    else:
        best_move = best_move_1 or best_move_2

    if best_move:
        piece, move, board = best_move
        if pieces.move(piece, move):
            info_label.config(text=f"🛠️ Robot moved {piece.piece_type} to position {move} on board "
                                   f"{'1' if board is board1 else '2'}.")
            update_boards()
        else:
            info_label.config(text="⚠️ Robot could not make the move.")
    else:
        info_label.config(text="⚠️ No possible moves for the robot.")

    white_turn = True  # Return the turn to the player
    info_label.config(text="🔄 White player's turn.\n")

# Semi-random move for the robot
def semi_random_move(board):
    # Selects a semi-random move on a board.

    black_pieces = [item for sublist in board for item in sublist if item and item.color == "Black"]
    possible_moves = []
    for piece in black_pieces:
        moves = piece.legal_moves(board1, board2)
        for move in moves:
            possible_moves.append((piece, move, board))
    if possible_moves:
        return random.choice(possible_moves)
    return None

# Bind clicks to boards
canvas1.bind("<Button-1>", lambda event: board_click(event, board1, canvas1))
canvas2.bind("<Button-1>", lambda event: board_click(event, board2, canvas2))

# Draw the boards initially
update_boards()

# Run the main loop
root.mainloop()
