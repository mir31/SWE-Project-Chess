import pygame

chessboard = [[None for i in range(8)] for i in range(8)]
turn_cnt = 0
turn_color = 'white'
selected_role = None
selected_piece = None
x = None
y = None
in_check = False
game_over = False

# Set up the Piece class
class Piece:
    def __init__(self, role, color, pos, moved, sprite, checked):
            self.role = role
            self.color = color
            self.pos = pos
            self.moved = False
            self.sprite = sprite
            self.checked = False

    def move(self, moved_pos):
        chessboard[self.pos[0]][self.pos[1]] = None
        self.pos = moved_pos
        chessboard[moved_pos[0]][moved_pos[1]] = self
        self.moved = True


# Pawn subclass
wpsprite = pygame.image.load("white-pawn.png")
bpsprite = pygame.image.load("black-pawn.png")
class Pawn(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('pawn', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []

        # A pawn can move 1 square vertically, or 1-2 if they have not moved yet
        if chessboard[self.pos[0]][self.pos[1]].color == 'white':
            if on_board(self.pos[0] - 1, self.pos[1]):
                if (chessboard[self.pos[0] - 1][self.pos[1]] is None):
                    valid.append((self.pos[0] - 1, self.pos[1]))
                    if (chessboard[self.pos[0] - 2][self.pos[1]] is None) and (self.moved == False):
                        valid.append((self.pos[0] - 2, self.pos[1]))

            # Unlike other pieces, pawns can capture squares where they can not normally move (diagonal, adjacent, in front)
            if on_board(self.pos[0] - 1, self.pos[1] - 1):
                if (chessboard[self.pos[0] - 1][self.pos[1] - 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] - 1].color == 'black'):
                    valid.append((self.pos[0] - 1, self.pos[1] - 1))
            if on_board(self.pos[0] - 1, self.pos[1] + 1):
                if (chessboard[self.pos[0] - 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] + 1].color == 'black'):
                    valid.append((self.pos[0] - 1, self.pos[1] + 1))
        else:
            # The same code but for black pawns
            if on_board(self.pos[0] + 1, self.pos[1]):
                if (chessboard[self.pos[0] + 1][self.pos[1]] is None):
                    valid.append((self.pos[0] + 1, self.pos[1]))
                    if (chessboard[self.pos[0] + 2][self.pos[1]] is None) and (self.moved == False):
                        valid.append((self.pos[0] + 2, self.pos[1]))

            if on_board(self.pos[0] + 1, self.pos[1] - 1):
                if (chessboard[self.pos[0] + 1][self.pos[1] - 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] - 1].color == 'white'):
                    valid.append((self.pos[0] + 1, self.pos[1] - 1))
            if on_board(self.pos[0] + 1, self.pos[1] + 1):
                if (chessboard[self.pos[0] + 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] + 1].color == 'white'):
                    valid.append((self.pos[0] + 1, self.pos[1] + 1))

        return valid

    # The pawn's capture rules works differently from its movement rules
    # This function determines what squares the pawn can capture, and which ones it contests (used for king check)
    def pawn_capture(self):
        can_capture = []
        contests = []

        if chessboard[self.pos[0]][self.pos[1]].color == 'white':
            if on_board(self.pos[0] - 1, self.pos[1] - 1):
                contests.append((self.pos[0] - 1, self.pos[1] - 1))
                if (chessboard[self.pos[0] - 1][self.pos[1] - 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] - 1].color == 'black'):
                    can_capture.append((self.pos[0] - 1, self.pos[1] - 1))
                    
            if on_board(self.pos[0] - 1, self.pos[1] + 1):
                contests.append((self.pos[0] - 1, self.pos[1] + 1))
                if (chessboard[self.pos[0] - 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] + 1].color == 'black'):
                    can_capture.append((self.pos[0] - 1, self.pos[1] + 1))
        else:
            if on_board(self.pos[0] + 1, self.pos[1] - 1):
                contests.append((self.pos[0] + 1, self.pos[1] - 1))
                if (chessboard[self.pos[0] + 1][self.pos[1] - 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] - 1].color == 'white'):
                    can_capture.append((self.pos[0] + 1, self.pos[1] - 1))
                    
            if on_board(self.pos[0] + 1, self.pos[1] + 1):
                contests.append((self.pos[0] + 1, self.pos[1] + 1))
                if (chessboard[self.pos[0] + 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] + 1].color == 'white'):
                    can_capture.append((self.pos[0] + 1, self.pos[1] + 1))

        return [can_capture, contests]

# Rook subclass
wrsprite = pygame.image.load("white-rook.png")
brsprite = pygame.image.load("black-rook.png")
class Rook(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('rook', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        contests = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for d in directions:
            x1 = self.pos[0]
            y1 = self.pos[1]
            while True:
                x1 += d[0]
                y1 += d[1]
                
                if not on_board(x1, y1):
                    break

                contests.append((x1, y1))
                if chessboard[x1][y1] is None:
                    valid.append((x1, y1))
                elif chessboard[x1][y1] is not None and chessboard[self.pos[0]][self.pos[1]].color != chessboard[x1][y1].color:
                    valid.append((x1, y1))
                    break
                else:
                    break

        return [valid, contests]

# Bishop subclass
wbsprite = pygame.image.load("white-bishop.png")
bbsprite = pygame.image.load("black-bishop.png")
class Bishop(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('bishop', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        contests = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d in directions:
            x1 = self.pos[0]
            y1 = self.pos[1]
            while True:
                x1 += d[0]
                y1 += d[1]

                if not on_board(x1, y1):
                    break

                contests.append((x1, y1))
                if chessboard[x1][y1] is None:
                    valid.append((x1, y1))
                elif chessboard[x1][y1] is not None and chessboard[self.pos[0]][self.pos[1]].color != chessboard[x1][y1].color:
                    valid.append((x1, y1))
                    break
                else:
                    break

        return [valid, contests]

# Knight subclass
wknsprite = pygame.image.load("white-knight.png")
bknsprite = pygame.image.load("black-knight.png")
class Knight(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('knight', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        contests = []
        possible = [(self.pos[0]-2, self.pos[1]-1), (self.pos[0]-2, self.pos[1]+1),
                    (self.pos[0]+2, self.pos[1]-1), (self.pos[0]+2, self.pos[1]+1),
                    (self.pos[0]-1, self.pos[1]-2), (self.pos[0]+1, self.pos[1]-2),
                    (self.pos[0]-1, self.pos[1]+2), (self.pos[0]+1, self.pos[1]+2)]
        
        for i in possible:
            if on_board(i[0], i[1]):
                contests.append(i)
                if chessboard[self.pos[0]][self.pos[1]].color == 'white':
                    if (chessboard[i[0]][i[1]] is None or chessboard[i[0]][i[1]].color == 'black'):
                        valid.append(i)
                else:
                    if (chessboard[i[0]][i[1]] is None or chessboard[i[0]][i[1]].color == 'white'):
                        valid.append(i)

        return [valid, contests]

# King subclass
wksprite = pygame.image.load("white-king.png")
bksprite = pygame.image.load("black-king.png")
class King(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('king', color, pos, moved, sprite, checked)

    def contests_squares(self):
        contests = []
        possible = [(self.pos[0] + 1, self.pos[1]), (self.pos[0] - 1, self.pos[1]),
                    (self.pos[0], self.pos[1] + 1), (self.pos[0], self.pos[1] - 1),
                    (self.pos[0] - 1, self.pos[1] - 1), (self.pos[0] + 1, self.pos[1] + 1),
                    (self.pos[0] - 1, self.pos[1] + 1), (self.pos[0] + 1, self.pos[1] - 1)]

        for i in possible:
            if on_board(i[0], i[1]):
                contests.append(i)

        return contests
        

    def valid_moves(self):
        contested = find_contested()
        contests = King.contests_squares(self)
        
        valid = []
        
        for i in contests:
            if not contested[i[0]][i[1]]:
                if chessboard[i[0]][i[1]] is None:
                        valid.append(i)
                elif chessboard[i[0]][i[1]] is not None and chessboard[self.pos[0]][self.pos[1]].color != chessboard[i[0]][i[1]].color:
                        valid.append(i)

        return valid

# Queen subclass
wqsprite = pygame.image.load("white-queen.png")
bqsprite = pygame.image.load("black-queen.png")
class Queen(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('queen', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        contests = []
        directions = [(1, -1), (1, 0), (1, 1), (0, -1),
                      (0, 1), (-1, -1), (-1, 0), (-1, 1)]

        for d in directions:
            x1 = self.pos[0]
            y1 = self.pos[1]
            while True:
                x1 += d[0]
                y1 += d[1]

                if not on_board(x1, y1):
                    break

                contests.append((x1, y1))
                if chessboard[x1][y1] is None:
                    valid.append((x1, y1))
                elif chessboard[x1][y1] is not None and chessboard[self.pos[0]][self.pos[1]].color != chessboard[x1][y1].color:
                    valid.append((x1, y1))
                    break
                else:
                    break

        return [valid, contests]

# Setting up the pieces on the board
def original_state():
    global game_over, turn_cnt, turn_color, chessboard, in_check
    
    # Creating the chessboard
    chessboard = [[None for i in range(8)] for i in range(8)]
    
    for i in range(8):
        chessboard[1][i] = Pawn('black', (1, i), False, bpsprite, False)
        chessboard[6][i] = Pawn('white', (6, i), False, wpsprite, False)

    chessboard[0][0] = Rook('black', (0, 0), False, brsprite, False)
    chessboard[0][7] = Rook('black', (0, 7), False, brsprite, False)
    chessboard[7][0] = Rook('white', (7, 0), False, wrsprite, False)
    chessboard[7][7] = Rook('white', (7, 7), False, wrsprite, False)

    chessboard[0][1] = Knight('black', (0, 1), False, bknsprite, False)
    chessboard[0][6] = Knight('black', (0, 6), False, bknsprite, False)
    chessboard[7][1] = Knight('white', (7, 1), False, wknsprite, False)
    chessboard[7][6] = Knight('white', (7, 6), False, wknsprite, False)

    chessboard[0][2] = Bishop('black', (0, 2), False, bbsprite, False)
    chessboard[0][5] = Bishop('black', (0, 5), False, bbsprite, False)
    chessboard[7][2] = Bishop('white', (7, 2), False, wbsprite, False)
    chessboard[7][5] = Bishop('white', (7, 5), False, wbsprite, False)

    chessboard[0][3] = Queen('black', (0, 3), False, bqsprite, False)
    chessboard[0][4] = King('black', (0, 4), False, bksprite, False)
    chessboard[7][3] = Queen('white', (7, 3), False, wqsprite, False)
    chessboard[7][4] = King('white', (7, 4), False, wksprite, False)

    game_over = False
    in_check = False
    turn_cnt = 0
    turn_color = 'white'

original_state()

# Set up the dimensions of the window
window_width = 800
window_height = 800

# Set up the dimensions of the board
board_width = 8
board_height = 8
square_size = 100

# Set up the colors
white = (212, 238, 188)
black = (118, 164, 83)
w_highlight = (212, 243, 255)
b_highlight = (109, 158, 191)
w_selected = (241, 244, 201)
b_selected = (180, 203, 89)
attack = (38, 128, 189)
wrong_turn = (79, 79, 79)
check_red = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the font
font_size = 50
font = pygame.font.Font(None, font_size)

# Create the game window
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Chessboard")

# Function for displaying a square
def draw_square(row, col, white_color, black_color):
    x_pos = col * square_size
    y_pos = row * square_size
    if (row + col) % 2 == 0:
        pygame.draw.rect(game_display, white_color, [x_pos, y_pos, square_size, square_size])
    else:
        pygame.draw.rect(game_display, black_color, [x_pos, y_pos, square_size, square_size])

# Highlighting valid moves
def highlight_moves():
    if selected_piece is not None and selected_piece.color == turn_color:
        moves = selected_piece.valid_moves()

        for row in range(board_height):
            for col in range(board_width):
                if on_board(row, col):
                    if (selected_piece.role != 'pawn' and selected_piece.role != 'king' and (row, col) in moves[0]) \
                    or (selected_piece.role == 'pawn' and (row, col) in moves) \
                    or (selected_piece.role == 'king' and (row, col) in moves):
                        if chessboard[row][col] is not None and chessboard[row][col].color != selected_piece.color:
                            draw_square(row, col, attack, attack)
                        else:
                            draw_square(row, col, w_highlight, b_highlight)
                    elif (row, col) == (x, y):
                        draw_square(row, col, w_selected, b_selected)

    # Grays out square if it's not that user's turn to move
    elif selected_piece is not None and selected_piece.color != turn_color:
        for row in range(board_height):
            for col in range(board_width):
                if chessboard[row][col] is selected_piece:
                    draw_square(row, col, wrong_turn, wrong_turn)

    # Highlights king in red if under check
    elif in_check:
        for row in range(board_height):
            for col in range(board_width):
                if chessboard[row][col] is not None:
                    if chessboard[row][col].role == 'king' and chessboard[row][col].color == turn_color:
                        draw_square(row, col, check_red, check_red)
    

# Visualising the chessboard
def draw_board():
    for row in range(board_height):
        for col in range(board_width):
            draw_square(row, col, white, black)

    if (x is not None and y is not None):
        highlight_moves()

    for row in range(board_height):
        for col in range(board_width):
            if chessboard[row][col] is not None:
                x_pos = col * square_size
                y_pos = row * square_size
                game_display.blit(chessboard[row][col].sprite, (x_pos, y_pos))

# Functions for finding what the user clicked
def square_clicked(pos):
    row_clicked = pos[0] / 100
    col_clicked = pos[1] / 100
    return (int(col_clicked), int(row_clicked))

def piece_clicked(row_clicked, col_clicked):
    if chessboard[row_clicked][col_clicked] is not None:
        return chessboard[row_clicked][col_clicked].role
    else:
        pass

# Determines whether a square exists on the 8x8 board
def on_board(xcoord, ycoord):
    if (xcoord > -1 and xcoord < 8) and (ycoord > -1 and ycoord < 8):
        return True
    else:
        return False

# Maps which squares can be attacked by the opponent
def find_contested():
    contested_squares = [[False for i in range(8)] for i in range(8)]
    
    # Iterate through each of opponent's pieces
    for row in range(board_height):
        for col in range(board_width):
            if chessboard[row][col] is not None and chessboard[row][col].color != turn_color:
                # Set all squares which the opponent can attack to True in the contested_squares 2D array
                if chessboard[row][col].role == 'king':
                    moves = chessboard[row][col].contests_squares()
                    for square in moves:
                        contested_squares[square[0]][square[1]] = True
                    continue
                
                elif chessboard[row][col].role == 'pawn':
                    moves = chessboard[row][col].pawn_capture()
                    for square in moves[1]:
                        contested_squares[square[0]][square[1]] = True
                    continue
                
                else:
                    moves = chessboard[row][col].valid_moves()
                    for square in moves[1]:
                        contested_squares[square[0]][square[1]] = True
                
    return contested_squares

# Determines whether the king is in check after a move
def is_check(x, y, board):
    global in_check
    in_check = False

    contested = find_contested()
    for row in range(board_height):
        for col in range(board_width):
            if board[row][col] is not None:
                if board[row][col].role == 'king' and board[row][col].color == turn_color:
                    # If the king's square can be attacked (is True in contested), the king is in check
                    if contested[row][col]:
                        in_check = True
                        board[row][col].checked = in_check
                    else:
                        board[row][col].checked = in_check

    return in_check

# Determines whether a move would put the king in check, thus being illegal
def would_check(x, y, last_x, last_y, last_status, board):
    global in_check

    # Create a copy of the board to simulate the move
    board_copy = board
    piece_copy = board_copy[last_x][last_y]
    piece_copy1 = board_copy[x][y]

    if piece_copy is not None:
        # Simulate the move
        piece_copy.move((x, y))

        # Check if the moved piece was pinned (would put the king in check)
        in_check = is_check(x, y, board_copy)

        # Revert back to the real board state
        piece_copy.move((last_x, last_y))
        piece_copy.moved = last_status
        board[x][y] = piece_copy1
    
    return in_check

# Finds the number of legal moves a player can make
# Used to find game end conditions, such as checkmate/stalemate
def legal_moves(last_check_status):
    global in_check
    
    # Number of pieces which can make a legal move
    piece_cnt = 0
    
    # Iterate through every piece of the player in turn
    for row in range(board_height):
        for col in range(board_width):
            if chessboard[row][col] is not None:
                if chessboard[row][col].color == turn_color:
                    
                    # For every piece, find its moveset and increment piece_cnt
                    piece_cnt += 1
                    invalid_moves = []
                    piece_moves = chessboard[row][col].valid_moves()

                    # If a move in a piece's moveset would put the king in check, append that to invalid_moves
                    if chessboard[row][col].role == 'pawn' or chessboard[row][col].role == 'king':
                        for move in piece_moves:
                            if would_check(move[0], move[1], row, col, chessboard[row][col].moved, chessboard):
                                invalid_moves.append(move)
                    else:
                        for move in piece_moves[0]:
                            if would_check(move[0], move[1], row, col, chessboard[row][col].moved, chessboard):
                                invalid_moves.append(move)

                    # If all of a piece's moves are invalid, decrement piece_cnt
                    if chessboard[row][col].role == 'pawn' or chessboard[row][col].role == 'king':
                        if invalid_moves == piece_moves:
                            piece_cnt -= 1
                    else:
                        if invalid_moves == piece_moves[0]:
                            piece_cnt -= 1

    in_check = last_check_status
    
    return piece_cnt

# Main game loop
def game_loop():
    global x, y, selected_role, selected_piece, turn_cnt, turn_color, in_check, game_over
    
    game_exit = False
    
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # On user click
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # If the user has selected a piece
                if selected_role is not None:
                    if (selected_piece.color == turn_color):
                        moves = chessboard[x][y].valid_moves()

                        # Variables necessary when testing for pinned pieces
                        last_x, last_y = x, y
                        last_status = selected_piece.moved
                        in_check = False

                        mouse_coords = pygame.mouse.get_pos()
                        x, y = square_clicked(mouse_coords)
                                    
                        # Checks if the move abides to the piece's moveset
                        if (selected_piece.role != 'pawn' and selected_piece.role != 'king' and (x, y) in moves[0]) \
                           or (selected_piece.role == 'pawn' and (x, y) in moves) \
                           or (selected_piece.role == 'king' and (x, y) in moves):

                            # Checks if the move would result in a king in check
                            if not would_check(x, y, last_x, last_y, last_status, chessboard):
                                selected_piece.move((x,y))
                                selected_role = None
                                selected_piece = None

                                # After a move, the turn goes to the other player
                                turn_cnt += 1
                                if turn_cnt % 2 == 0:
                                    turn_color = 'white'
                                else:
                                    turn_color = 'black'

                                # After the turn changes, determine whether the king is in check
                                in_check = is_check(x, y, chessboard)

                                # Check for game end conditions.
                                # Checkmate happens when the king is in check and the player can not make any moves.
                                if in_check and legal_moves(in_check) == 0:
                                    print("Checkmate!")
                                    if turn_cnt % 2 == 0:
                                        print("Black wins.")
                                    else:
                                        print("White wins.")
                                    game_over = True

                                # Stalemate happens when the king is not in check, but the player can not make any moves.
                                elif not in_check and legal_moves(in_check) == 0:
                                    print("Stalemate.")
                                    game_over = True
 
                            # If the move puts king in check, get another one
                            else:
                                selected_role = None
                                selected_piece = None

                        # If move is not legal/the same piece is clicked, removes the selection
                        elif selected_piece == chessboard[x][y]:
                            selected_role = None
                            selected_piece = None
                        else:
                            selected_role = piece_clicked(x, y)
                            selected_piece = chessboard[x][y]

                    # If the piece is selected is not the color's turn to go, removes the selection
                    else:
                        selected_role = None
                        selected_piece = None
                            
                # If no piece has been selected, get input until one is
                else:
                    mouse_coords = pygame.mouse.get_pos()
                    x, y = square_clicked(mouse_coords)
                            
                    selected_role = piece_clicked(x, y)
                    selected_piece = chessboard[x][y]
                
        # Draw the board
        draw_board()

        # Update the screen
        pygame.display.update()

        # Ask user to play again if game is over
        while game_over:
            print("Game over.")
            rematch = input("Play again? (Y/N): ")
            if rematch == "Y":
                original_state()
            elif rematch == "N":
                game_exit = True
                game_over = False
            else:
                print("Invalid input.")
        

    pygame.quit()
    quit()

# Start the game
game_loop()
