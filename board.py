'''
Board class
The Board class is responsible for managing the state of the game boards. It keeps track of the pieces on both boards,
allows pieces to be added, moved, or removed, and provides methods to display the boards in the console.

Elabaroted by:  Manuel Arango   2259571
                Alex Garcia     2259517
                Sebastian Gomez 2259474
                Stiven Henao    2259603

Teacher:        Joshua Triana
Course:         Artificial Intelligence
Date:           2024 December
'''

class Board:
    def __init__(self):
        # Initializes the matrices representing the boards for white and black pieces
        self.white_board = [[None] * 8 for _ in range(8)]
        self.black_board = [[None] * 8 for _ in range(8)]

    def display_boards(self):
        # Prints the boards in the console with a clear visual representation, including row and column labels.

        columns = "01234567"
        border = "  +" + "-" * 17 + "+"
        
        # Column headers
        print("    " + " ".join(columns) + "         " + "".join(columns))
        print(border + "" + border)

        for row in range(8):
            # Build the rows for both boards
            white_pieces = ' '.join(self._display_cell(cell) for cell in self.white_board[row])
            black_pieces = ' '.join(self._display_cell(cell) for cell in self.black_board[row])
            
            # Print the row with side labels
            print(f"{row} | {white_pieces} |    {row} | {black_pieces} |")

        # Board footer
        print(border + "#    #" + border)

    @staticmethod
    def _display_cell(cell):
        # Visually represents a cell on the board. If there's a piece, it shows its symbol with color; otherwise, it displays a dot.
        if cell:
            if cell.color == "White":
                return f"\033[97m{cell.type[0]}\033[0m"  # White color for white pieces
            elif cell.color == "Black":
                return f"\033[91m{cell.type[0]}\033[0m"  # Red color for black pieces
        return "."  # Empty cell

    def add_piece(self, piece, position):
        # Places a piece at the specified position on the corresponding board.

        row, column = position
        if piece.dimension == 1:
            self.white_board[row][column] = piece
        elif piece.dimension == 2:
            self.black_board[row][column] = piece

    def move_piece(self, piece, new_position):
        # Moves a piece from its current location to a new position, ensuring its state is updated and removing any piece at the destination.

        row, column = new_position

        if not self._valid_position(new_position):
            return  # Do not move if the position is invalid

        # Remove the piece from its current location
        self._remove_piece(piece, position=piece.position)

        # Update the board based on the piece's dimension
        if piece.dimension == 1:
            if not self.black_board[row][column] or self.black_board[row][column].color != piece.color:
                piece.dimension = 2
                self.black_board[row][column] = piece
        elif piece.dimension == 2:
            if not self.white_board[row][column] or self.white_board[row][column].color != piece.color:
                piece.dimension = 1
                self.white_board[row][column] = piece

        piece.position = new_position

    def create_copy(self):
        #Generates a copy of the current state of both boards.

        copy = Board()
        copy.white_board = [row[:] for row in self.white_board]
        copy.black_board = [row[:] for row in self.black_board]
        return copy

    def _remove_piece(self, piece, position):
        # Removes a piece from its current board (in both dimensions, if necessary).

        for board in [self.white_board, self.black_board]:
            for row in board:
                if piece in row:
                    row[row.index(piece)] = None

    def remove_piece_at(self, position):
        # Removes a piece from a specific position, if it exists.

        row, column = position
        if self.white_board[row][column]:
            self.white_board[row][column] = None
        elif self.black_board[row][column]:
            self.black_board[row][column] = None

    def get_opponent_pieces(self, color, dimension):
        # Returns a list of all opponent pieces on the specified board.

        board = self.black_board if dimension == 2 else self.white_board
        return [cell for row in board for cell in row if cell and cell.color != color]

    def _valid_position(self, position):
        #Checks if a position is within the board boundaries.

        row, column = position
        return 0 <= row < 8 and 0 <= column < 8
