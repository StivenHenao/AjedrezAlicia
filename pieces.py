'''
pieces.py
This module contains the classes for the different chess pieces, as well as the functions to manage the game state.

Elabaroted by:  Manuel Arango   2259571
                Alex Garcia     2259517
                Sebastian Gomez 2259474
                Stiven Henao    2259603

Teacher:        Joshua Triana
Course:         Artificial Intelligence
Date:           2024 December
'''

import board

class Piece:
    def __init__(self, piece_type, color, position, dimension, value):
        self.piece_type = piece_type  # Piece type: "King", "Queen", "Rook", etc.
        self.color = color  # Color: "White" or "Black"
        self.position = position  # Tuple (row, column)
        self.dimension = dimension  # 1 for left board, 2 for right board
        self.value = value
        self.img = None
    
    def legal_moves(self, current_board, opposing_board):
        # This method will be implemented in subclasses. Defines the valid moves based on the piece type.
        raise NotImplementedError

class Pawn(Piece):
    def __init__(self, color, position, dimension, value):
        super().__init__("Pawn", color, position, dimension, value)
    
    def legal_moves(self, current_board, opposing_board):
        moves = []
        row, col = self.position
        if self.color == "White":
            if self.dimension == 1:
                if row + 1 < 8 and current_board[row + 1][col] is None and opposing_board[row + 1][col] is None:
                    moves.append((row + 1, col))
                if row == 1 and current_board[row + 2][col] is None and opposing_board[row + 2][col] is None:
                    moves.append((row + 2, col))
                if row + 1 < 8 and col + 1 < 8 and current_board[row + 1][col + 1] is not None and current_board[row + 1][col + 1].color != self.color:
                    moves.append((row + 1, col + 1))
                if row + 1 < 8 and col - 1 >= 0 and current_board[row + 1][col - 1] is not None and current_board[row + 1][col - 1].color != self.color:
                    moves.append((row + 1, col - 1))
            else:
                if row + 1 < 8 and opposing_board[row + 1][col] is None and current_board[row + 1][col] is None:
                    moves.append((row + 1, col))
                if row == 1 and opposing_board[row + 2][col] is None and current_board[row + 2][col] is None:
                    moves.append((row + 2, col))
                if row + 1 < 8 and col + 1 < 8 and opposing_board[row + 1][col + 1] is not None and opposing_board[row + 1][col + 1].color != self.color:
                    moves.append((row + 1, col + 1))
                if row + 1 < 8 and col - 1 >= 0 and opposing_board[row + 1][col - 1] is not None and opposing_board[row + 1][col - 1].color != self.color:
                    moves.append((row + 1, col - 1))
        else:
            if self.dimension == 1:
                if row - 1 >= 0 and current_board[row - 1][col] is None and opposing_board[row - 1][col] is None:
                    moves.append((row - 1, col))
                if row == 6 and current_board[row - 2][col] is None and opposing_board[row - 2][col] is None:
                    moves.append((row - 2, col))
                if row - 1 >= 0 and col + 1 < 8 and current_board[row - 1][col + 1] is not None and current_board[row - 1][col + 1].color != self.color:
                    moves.append((row - 1, col + 1))
                if row - 1 >= 0 and col - 1 >= 0 and current_board[row - 1][col - 1] is not None and current_board[row - 1][col - 1].color != self.color:
                    moves.append((row - 1, col - 1))
            else:
                if row - 1 >= 0 and opposing_board[row - 1][col] is None and current_board[row - 1][col] is None:
                    moves.append((row - 1, col))
                if row == 6 and opposing_board[row - 2][col] is None and current_board[row - 2][col] is None:
                    moves.append((row - 2, col))
                if row - 1 >= 0 and col + 1 < 8 and opposing_board[row - 1][col + 1] is not None and opposing_board[row - 1][col + 1].color != self.color:
                    moves.append((row - 1, col + 1))
                if row - 1 >= 0 and col - 1 >= 0 and opposing_board[row - 1][col - 1] is not None and opposing_board[row - 1][col - 1].color != self.color:
                    moves.append((row - 1, col - 1))
        return moves

    def promote(self):
        # Check if the pawn is on row 0 or 7
        pass
    
    def en_passant(self):
        # Check if the pawn can perform the en passant move
        pass    

class Rook(Piece):
    def __init__(self, color, position, dimension, value):
        super().__init__("Rook", color, position, dimension, value)
    
    def legal_moves(self, current_board, opposing_board):
        moves = []
        row, col = self.position
        # Vertical moves
        if self.dimension == 1:
            for i in range(row + 1, 8):
                if current_board[i][col] is None:
                    moves.append((i, col))
                elif current_board[i][col].color != self.color:
                    moves.append((i, col))
                    break
                else:
                    break

            for i in range(row - 1, -1, -1):
                if current_board[i][col] is None:
                    moves.append((i, col))
                elif current_board[i][col].color != self.color:
                    moves.append((i, col))
                    break
                else:
                    break

            # Horizontal moves
            for i in range(col + 1, 8):
                if current_board[row][i] is None:
                    moves.append((row, i))
                elif current_board[row][i].color != self.color:
                    moves.append((row, i))
                    break
                else:
                    break

            for i in range(col - 1, -1, -1):
                if current_board[row][i] is None:
                    moves.append((row, i))
                elif current_board[row][i].color != self.color:
                    moves.append((row, i))
                    break
                else:
                    break
        else:
            for i in range(row + 1, 8):
                if opposing_board[i][col] is None:
                    moves.append((i, col))
                elif opposing_board[i][col].color != self.color:
                    moves.append((i, col))
                    break
                else:
                    break

            for i in range(row - 1, -1, -1):
                if opposing_board[i][col] is None:
                    moves.append((i, col))
                elif opposing_board[i][col].color != self.color:
                    moves.append((i, col))
                    break
                else:
                    break

            # Horizontal moves
            for i in range(col + 1, 8):
                if opposing_board[row][i] is None:
                    moves.append((row, i))
                elif opposing_board[row][i].color != self.color:
                    moves.append((row, i))
                    break
                else:
                    break

            for i in range(col - 1, -1, -1):
                if opposing_board[row][i] is None:
                    moves.append((row, i))
                elif opposing_board[row][i].color != self.color:
                    moves.append((row, i))
                    break
                else:
                    break
                
        return moves

class Knight(Piece):
    def __init__(self, color, position, dimension, value):
        super().__init__("Knight", color, position, dimension, value)
    
    def legal_moves(self, current_board, opposite_board):
        moves = []
        row, col = self.position
        possible_moves = [
                (row + 2, col + 1), (row + 2, col - 1),
                (row - 2, col + 1), (row - 2, col - 1),
                (row + 1, col + 2), (row + 1, col - 2),
                (row - 1, col + 2), (row - 1, col - 2)
            ]
        if self.dimension == 1:    
            for move in possible_moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    piece = current_board[move[0]][move[1]]
                    if piece is None or piece.color != self.color:
                        moves.append(move) 
        else:
            for move in possible_moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    piece = opposite_board[move[0]][move[1]]
                    if piece is None or piece.color != self.color:
                        moves.append(move)
        return moves

class Bishop(Piece):
    def __init__(self, color, position, dimension, value):
        super().__init__("Bishop", color, position, dimension, value)
    
    def legal_moves(self, current_board, opposite_board):
        moves = []
        row, col = self.position
        board = current_board if self.dimension == 1 else opposite_board
        # Bishop movement directions: [up-right, up-left, down-right, down-left]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            for i in range(1, 8):  # Maximum of 7 steps on the board
                new_row = row + i * dx
                new_col = col + i * dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:  # Within board limits
                    piece = board[new_row][new_col]
                    if piece is None:  # Empty cell, valid move
                        moves.append((new_row, new_col))
                    elif piece.color != self.color:  # Cell occupied by an enemy piece
                        moves.append((new_row, new_col))
                        break  # Bishop cannot continue after capturing
                    else:  # Cell occupied by an allied piece
                        break  # Cannot continue through allied pieces
                else:
                    break  # Out of board limits

        return moves

class King(Piece):
    def __init__(self, color, position, dimension, value):
        super().__init__("King", color, position, dimension, value)
    
    def legal_moves(self, current_board, opposite_board):
        moves = []
        row, col = self.position
        board = current_board if self.dimension == 1 else opposite_board
        possible_moves = [
                (row + 1, col), (row - 1, col),
                (row, col + 1), (row, col - 1),
                (row + 1, col + 1), (row + 1, col - 1),
                (row - 1, col + 1), (row - 1, col - 1)
            ]
        for move in possible_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                piece = board[move[0]][move[1]]
                if piece is None or piece.color != self.color:
                    moves.append(move)
        return moves

    def castle(self, current_board, opposite_board):
        moves = []
        row, col = self.position

        if self.color == "White":
            if self.dimension == 1 and self.position == (0, 4):
                # Short castle
                if isinstance(current_board[0][7], Rook) and current_board[0][7].dimension == 1:
                    if current_board[0][5] is None and current_board[0][6] is None:
                        moves.append((0, 6))
                # Long castle
                if isinstance(current_board[0][0], Rook) and current_board[0][0].dimension == 1:
                    if current_board[0][1] is None and current_board[0][2] is None and current_board[0][3] is None:
                        moves.append((0, 2))
        else:
            if self.dimension == 1 and self.position == (7, 4):
                # Short castle
                if isinstance(current_board[7][7], Rook) and current_board[7][7].dimension == 1:
                    if current_board[7][5] is None and current_board[7][6] is None:
                        moves.append((7, 6))
                # Long castle
                if isinstance(current_board[7][0], Rook) and current_board[7][0].dimension == 1:
                    if current_board[7][1] is None and current_board[7][2] is None and current_board[7][3] is None:
                        moves.append((7, 2))
        return moves

    def in_check(self, current_board, opposite_board):
        for piece in pieces:
            if piece.color != self.color:
                enemy_moves = piece.legal_moves(current_board, opposite_board)
                if self.position in enemy_moves:
                    return True
        return False

    def checkmate(self, current_board, opposite_board):
        return True

    def stalemate(self):
        pass  # Check if the king is in stalemate

class Queen(Piece):
    def __init__(self, color, position, dimension, value):
        super().__init__("Queen", color, position, dimension, value)
    
    def legal_moves(self, current_board, opposite_board):
        moves = []
        row, col = self.position
        board = current_board if self.dimension == 1 else opposite_board

        # Rook-like moves
        for i in range(row + 1, 8):
            if board[i][col] is None:
                moves.append((i, col))
            elif board[i][col].color != self.color:
                moves.append((i, col))
                break
            else:
                break

        for i in range(row - 1, -1, -1):
            if board[i][col] is None:
                moves.append((i, col))
            elif board[i][col].color != self.color:
                moves.append((i, col))
                break
            else:
                break

        for i in range(col + 1, 8):
            if board[row][i] is None:
                moves.append((row, i))
            elif board[row][i].color != self.color:
                moves.append((row, i))
                break
            else:
                break

        for i in range(col - 1, -1, -1):
            if board[row][i] is None:
                moves.append((row, i))
            elif board[row][i].color != self.color:
                moves.append((row, i))
                break
            else:
                break

        # Bishop-like moves
        for i in range(1, 8):
            if row + i < 8 and col + i < 8:
                if board[row + i][col + i] is None:
                    moves.append((row + i, col + i))
                elif board[row + i][col + i].color != self.color:
                    moves.append((row + i, col + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if row + i < 8 and col - i >= 0:
                if board[row + i][col - i] is None:
                    moves.append((row + i, col - i))
                elif board[row + i][col - i].color != self.color:
                    moves.append((row + i, col - i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if row - i >= 0 and col + i < 8:
                if board[row - i][col + i] is None:
                    moves.append((row - i, col + i))
                elif board[row - i][col + i].color != self.color:
                    moves.append((row - i, col + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if row - i >= 0 and col - i >= 0:
                if board[row - i][col - i] is None:
                    moves.append((row - i, col - i))
                elif board[row - i][col - i].color != self.color:
                    moves.append((row - i, col - i))
                    break
                else:
                    break
            else:
                break

        return moves
def initialize_pieces():
    global board
    global pieces
    
    board = board.Board()
    
    pieces = []
    # Create white pieces
    pieces.append(Rook("White", (0, 0), 1, 5))
    pieces.append(Knight("White", (0, 1), 1, 3))
    pieces.append(Bishop("White", (0, 2), 1, 3))
    pieces.append(Queen("White", (0, 3), 1, 9))
    pieces.append(King("White", (0, 4), 1, 100))
    pieces.append(Bishop("White", (0, 5), 1, 3))
    pieces.append(Knight("White", (0, 6), 1, 3))
    pieces.append(Rook("White", (0, 7), 1, 5))
    for i in range(8):
        pieces.append(Pawn("White", (1, i), 1, 1))
    
    # Create black pieces
    pieces.append(Rook("Black", (7, 0), 1, 5))
    pieces.append(Knight("Black", (7, 1), 1, 3))
    pieces.append(Bishop("Black", (7, 2), 1, 3))
    pieces.append(Queen("Black", (7, 3), 1, 9))
    pieces.append(King("Black", (7, 4), 1, 100))
    pieces.append(Bishop("Black", (7, 5), 1, 3))
    pieces.append(Knight("Black", (7, 6), 1, 3))
    pieces.append(Rook("Black", (7, 7), 1, 5))
    for i in range(8):
        pieces.append(Pawn("Black", (6, i), 1, 1))

    initialize_board(pieces)
    

def initialize_board(pieces):
    for piece in pieces:
        board.add_piece(piece, piece.position)
    

def display_board():
    board.display_boards()

def get_boards():
    return board.white_board, board.black_board

def find_piece(position):
    for piece in pieces:
        if piece.position == position:
            return piece
    return None

def find_piece_in_general(position, pieces_list):
    for piece in pieces_list:
        if piece.position == position:
            return piece
    return None

def move(piece, position, simulate=False):
    if board.white_board[position[0]][position[1]] is not None and board.black_board[position[0]][position[1]] is not None:
        return False
    king = next((p for p in pieces if isinstance(p, King) and p.color == piece.color), None)

    if piece.color != king.color:
        if position in piece.legal_moves(board.white_board, board.black_board):
            if simulate:
                return True
            enemy_piece = find_piece_in_general(position, board.get_opponent_pieces(piece.color, piece.dimension))
            if enemy_piece:
                board._remove_piece(enemy_piece, position)
                print(f"Removed: {enemy_piece.piece_type} {enemy_piece.position} {enemy_piece.color}")
                if enemy_piece in pieces:
                    pieces.remove(enemy_piece)
            board.move_piece(piece, position)
            return True
        else:
            return False

    if king and king.in_check(board.white_board, board.black_board):
        defensive_moves = []
        defensive_pieces = []

        board_to_check = board.white_board if king.dimension == 1 else board.black_board
        moves_to_defend = []
        defensive_pieces = []

        for piece in pieces:
            if piece.color != king.color:
                moves_to_defend.extend(piece.legal_moves(board_to_check, board.black_board))
            else:
                defensive_pieces.extend(piece.legal_moves(board_to_check, board.black_board))

        defensive_diff = set(defensive_pieces).difference(moves_to_defend).intersection(king.legal_moves(board_to_check, board.black_board))
        print(defensive_diff)
        if moves_to_defend == defensive_pieces:
            print("Cannot defend")
            return False
        if piece.color == king.color:
            if piece.piece_type == "King":
                if position in defensive_diff:
                    if simulate:
                        return True
                    board.move_piece(piece, position)
                    return True
                else:
                    return False
            else:
                if position in defensive_diff:
                    if simulate:
                        return True
                    board.move_piece(piece, position)
                    return True
                else:
                    return False

    if not king.in_check(board.white_board, board.black_board):
        if isinstance(piece, King):
            castle_moves = piece.castle(board.white_board, board.black_board)
            if position in castle_moves:
                if simulate:
                    return True
                if position[1] == 6:
                    rook = find_piece((position[0], 7))
                    board.move_piece(rook, (position[0], 5))
                elif position[1] == 2:
                    rook = find_piece((position[0], 0))
                    board.move_piece(rook, (position[0], 3))
                board.move_piece(piece, position)
                return True
        if position in piece.legal_moves(board.white_board, board.black_board):
            if simulate:
                return True
            enemy_piece = find_piece_in_general(position, board.get_opponent_pieces(piece.color, piece.dimension))
            if enemy_piece:
                board._remove_piece(enemy_piece, position)
                print(f"Removed: {enemy_piece.piece_type} {enemy_piece.position} {enemy_piece.color}")
                if enemy_piece in pieces:
                    pieces.remove(enemy_piece)
            board.move_piece(piece, position)
            return True
        else:
            return False
    else:
        return False

def possible_moves(piece):
    print(piece.legal_moves(board.white_board, board.black_board))

def indicate_check():
    for piece in pieces:
        if isinstance(piece, King):
            if piece.in_check(board.white_board, board.black_board):
                print(f"The {piece.color} king is in check.")
                return True
    return False

def indicate_checkmate():
    for piece in pieces:
        if isinstance(piece, King):
            if piece.in_checkmate(board.white_board, board.black_board):
                return True
    return False

def end_game():
    # Check if one of the kings has been eliminated
    kings = [piece for piece in pieces if isinstance(piece, King)]
    if len(kings) < 2:
        return True
    return False

def get_piece_in_check():
    king = next((piece for piece in pieces if isinstance(piece, King)), None)
    pieces_in_check = []
    for piece in pieces:
        if piece.color != king.color:
            enemy_moves = piece.legal_moves(board.white_board, board.black_board)
            if king.position in enemy_moves:
                pieces_in_check.append(piece)
    return pieces_in_check
