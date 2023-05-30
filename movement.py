import pygame

selected_role = None
selected_piece = None
x = None
y = None

    
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
        can_capture = []

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
                    can_capture.append((self.pos[0] - 1, self.pos[1] - 1))
            if on_board(self.pos[0] - 1, self.pos[1] + 1):
                if (chessboard[self.pos[0] - 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] + 1].color == 'black'):
                    valid.append((self.pos[0] - 1, self.pos[1] + 1))
                    can_capture.append((self.pos[0] - 1, self.pos[1] + 1))
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
                    can_capture.append((self.pos[0] + 1, self.pos[1] - 1))
            if on_board(self.pos[0] + 1, self.pos[1] + 1):
                if (chessboard[self.pos[0] + 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] + 1].color == 'white'):
                    valid.append((self.pos[0] + 1, self.pos[1] + 1))
                    can_capture.append((self.pos[0] + 1, self.pos[1] + 1))

        return valid

    def pawn_capture(self):
        can_capture = []

        if chessboard[self.pos[0]][self.pos[1]].color == 'white':
            if on_board(self.pos[0] - 1, self.pos[1] - 1):
                if (chessboard[self.pos[0] - 1][self.pos[1] - 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] - 1].color == 'black'):
                    can_capture.append((self.pos[0] - 1, self.pos[1] - 1))
                    
            if on_board(self.pos[0] - 1, self.pos[1] + 1):
                if (chessboard[self.pos[0] - 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] - 1][self.pos[1] + 1].color == 'black'):
                    can_capture.append((self.pos[0] - 1, self.pos[1] + 1))
        else:
            if on_board(self.pos[0] + 1, self.pos[1] - 1):
                if (chessboard[self.pos[0] + 1][self.pos[1] - 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] - 1].color == 'white'):
                    can_capture.append((self.pos[0] + 1, self.pos[1] - 1))
                    
            if on_board(self.pos[0] + 1, self.pos[1] + 1):
                if (chessboard[self.pos[0] + 1][self.pos[1] + 1] is not None and chessboard[self.pos[0] + 1][self.pos[1] + 1].color == 'white'):
                    can_capture.append((self.pos[0] + 1, self.pos[1] + 1))

        return can_capture

# Rook subclass
wrsprite = pygame.image.load("white-rook.png")
brsprite = pygame.image.load("black-rook.png")
class Rook(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('rook', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for d in directions:
            x1 = self.pos[0]
            y1 = self.pos[1]
            while True:
                x1 += d[0]
                y1 += d[1]
                
                if not on_board(x1, y1):
                    break
                
                if chessboard[x1][y1] is None:
                    valid.append((x1, y1))
                elif chessboard[x1][y1] is not None and chessboard[x][y].color != chessboard[x1][y1].color:
                    valid.append((x1, y1))
                    break
                else:
                    break

        return valid

# Bishop subclass
wbsprite = pygame.image.load("white-bishop.png")
bbsprite = pygame.image.load("black-bishop.png")
class Bishop(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('bishop', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for d in directions:
            x1 = self.pos[0]
            y1 = self.pos[1]
            while True:
                x1 += d[0]
                y1 += d[1]

                if not on_board(x1, y1):
                    break
                
                if chessboard[x1][y1] is None:
                    valid.append((x1, y1))
                elif chessboard[x1][y1] is not None and chessboard[self.pos[0]][self.pos[1]].color != chessboard[x1][y1].color:
                    valid.append((x1, y1))
                    break
                else:
                    break

        return valid

# Knight subclass
wknsprite = pygame.image.load("white-knight.png")
bknsprite = pygame.image.load("black-knight.png")
class Knight(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('knight', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        possible = [(self.pos[0]-2, self.pos[1]-1), (self.pos[0]-2, self.pos[1]+1),
                    (self.pos[0]+2, self.pos[1]-1), (self.pos[0]+2, self.pos[1]+1),
                    (self.pos[0]-1, self.pos[1]-2), (self.pos[0]+1, self.pos[1]-2),
                    (self.pos[0]-1, self.pos[1]+2), (self.pos[0]+1, self.pos[1]+2)]
        
        for i in possible:
            if on_board(i[0], i[1]):
                if chessboard[x][y].color == 'white':
                    if (chessboard[i[0]][i[1]] is None or chessboard[i[0]][i[1]].color == 'black'):
                        valid.append(i)
                else:
                    if (chessboard[i[0]][i[1]] is None or chessboard[i[0]][i[1]].color == 'white'):
                        valid.append(i)

        return valid

# King subclass
wksprite = pygame.image.load("white-king.png")
bksprite = pygame.image.load("black-king.png")
class King(Piece):
    def __init__(self, color, pos, moved, sprite, checked):
            super().__init__('king', color, pos, moved, sprite, checked)

    def valid_moves(self):
        valid = []
        possible = [(self.pos[0] + 1, self.pos[1]), (self.pos[0] - 1, self.pos[1]),
                    (self.pos[0], self.pos[1] + 1), (self.pos[0], self.pos[1] - 1),
                    (self.pos[0] - 1, self.pos[1] - 1), (self.pos[0] + 1, self.pos[1] + 1),
                    (self.pos[0] - 1, self.pos[1] + 1), (self.pos[0] + 1, self.pos[1] - 1)]
        
        for i in possible:
            if on_board(i[0], i[1]):
                if chessboard[i[0]][i[1]] is None:
                    if not would_check(self.pos[0], self.pos[1], i[0], i[1], self.color):
                        valid.append(i)
                elif chessboard[i[0]][i[1]] is not None and chessboard[x][y].color != chessboard[i[0]][i[1]].color:
                    if not would_check(self.pos[0], self.pos[1], i[0], i[1], self.color):
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
                
                if chessboard[x1][y1] is None:
                    valid.append((x1, y1))
                elif chessboard[x1][y1] is not None and chessboard[x][y].color != chessboard[x1][y1].color:
                    valid.append((x1, y1))
                    break
                else:
                    break

        return valid
            

# Creating the chessboard
chessboard = [[None for i in range(8)] for i in range(8)]

# Setting up the pieces on the board
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
w_highlight = (212, 188, 238)
b_highlight = (160, 133, 219)
w_selected = (241, 244, 201)
b_selected = (180, 203, 89)
attack = (240, 68, 68)

# Initialize Pygame
pygame.init()

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
    if selected_piece is not None:
        moves = chessboard[x][y].valid_moves()

        for row in range(board_height):
            for col in range(board_width):
                if (row, col) in moves:
                    if chessboard[row][col] is not None and chessboard[row][col].color != selected_piece.color:
                        draw_square(row, col, attack, attack)
                    else:
                        draw_square(row, col, w_highlight, b_highlight)
                elif (row, col) == (x, y):
                    draw_square(row, col, w_selected, b_selected)

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

# Function for determining whether a move would result the king to be in check
def would_check(kx, ky, x, y, color):
    king_pos = (x, y)

    for row in range(board_height):
        for col in range(board_width):
            if chessboard[row][col] is not None:
                if chessboard[row][col].color != color:
                    if chessboard[row][col].role != 'king' and chessboard[row][col].role != 'pawn':
                        valid_moves = chessboard[row][col].valid_moves()
                        if king_pos in valid_moves:
                            return True
                    elif chessboard[row][col].role == 'pawn':
                        valid_moves = chessboard[row][col].pawn_capture()
                        if king_pos in valid_moves:
                            return True

    return False

# Main game loop
def game_loop():
    global x, y, selected_role, selected_piece
    
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # On user click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If a piece has already been selected beforehand
                if selected_role is not None:
                    moves = chessboard[x][y].valid_moves()
                    
                    mouse_coords = pygame.mouse.get_pos()
                    x, y = square_clicked(mouse_coords)
                    
                    # Moves the piece if move is legal
                    if (x, y) in moves:
                        selected_piece.move((x,y))
                        selected_role = None
                        selected_piece = None
                        
                    # Otherwise removes the selection
                    elif selected_piece == chessboard[x][y]:
                        selected_role = None
                        selected_piece = None
                    else:
                        selected_role = piece_clicked(x, y)
                        selected_piece = chessboard[x][y]
                        
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

    pygame.quit()
    quit()

# Start the game
game_loop()
