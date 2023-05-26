import pygame

# Set up the Piece class
class Piece:
    def __init__(self, role, color, pos, moved, sprite):
            self.role = role
            self.color = color
            self.pos = pos
            self.moved = False
            self.sprite = sprite


# Pawn subclass
wpsprite = pygame.image.load("white-pawn.png")
bpsprite = pygame.image.load("black-pawn.png")
class Pawn(Piece):
    def __init__(self, color, pos, moved, sprite):
            super().__init__('pawn', color, pos, moved, sprite)

# Rook subclass
wrsprite = pygame.image.load("white-rook.png")
brsprite = pygame.image.load("black-rook.png")
class Rook(Piece):
    def __init__(self, color, pos, moved, sprite):
            super().__init__('rook', color, pos, moved, sprite)

# Bishop subclass
wbsprite = pygame.image.load("white-bishop.png")
bbsprite = pygame.image.load("black-bishop.png")
class Bishop(Piece):
    def __init__(self, color, pos, moved, sprite):
            super().__init__('pawn', color, pos, moved, sprite)

# Knight subclass
wknsprite = pygame.image.load("white-knight.png")
bknsprite = pygame.image.load("black-knight.png")
class Knight(Piece):
    def __init__(self, color, pos, moved, sprite):
            super().__init__('knight', color, pos, moved, sprite)

# King subclass
wksprite = pygame.image.load("white-king.png")
bksprite = pygame.image.load("black-king.png")
class King(Piece):
    def __init__(self, color, pos, moved, sprite):
            super().__init__('king', color, pos, moved, sprite)

# Queen subclass
wqsprite = pygame.image.load("white-queen.png")
bqsprite = pygame.image.load("black-queen.png")
class Queen(Piece):
    def __init__(self, color, pos, moved, sprite):
            super().__init__('queen', color, pos, moved, sprite)
            

# Creating the chessboard
chessboard = [[None for i in range(8)] for i in range(8)]

# Setting up the pieces on the board
for i in range(8):
    chessboard[1][i] = Pawn('black', (1, i), False, bpsprite)
    chessboard[6][i] = Pawn('white', (6, i), False, wpsprite)

chessboard[0][0] = Rook('black', (0, 0), False, brsprite)
chessboard[0][7] = Rook('black', (0, 7), False, brsprite)
chessboard[7][0] = Rook('white', (0, 0), False, wrsprite)
chessboard[7][7] = Rook('white', (0, 7), False, wrsprite)

chessboard[0][1] = Knight('black', (0, 1), False, bknsprite)
chessboard[0][6] = Knight('black', (0, 6), False, bknsprite)
chessboard[7][1] = Knight('white', (7, 1), False, wknsprite)
chessboard[7][6] = Knight('white', (7, 6), False, wknsprite)

chessboard[0][2] = Bishop('black', (0, 2), False, bbsprite)
chessboard[0][5] = Bishop('black', (0, 5), False, bbsprite)
chessboard[7][2] = Bishop('white', (7, 2), False, wbsprite)
chessboard[7][5] = Bishop('white', (7, 5), False, wbsprite)

chessboard[0][3] = Queen('black', (0, 3), False, bqsprite)
chessboard[0][4] = King('black', (0, 4), False, bksprite)
chessboard[7][3] = Queen('white', (7, 3), False, wqsprite)
chessboard[7][4] = King('white', (7, 4), False, wksprite)

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

# Initialize Pygame
pygame.init()

# Create the game window
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Chessboard")

# Visualising the chessboard
def draw_board():
    for row in range(board_height):
        for col in range(board_width):
            x_pos = col * square_size
            y_pos = row * square_size
            if (row + col) % 2 == 0:
                pygame.draw.rect(game_display, white, [x_pos, y_pos, square_size, square_size])
            else:
                pygame.draw.rect(game_display, black, [x_pos, y_pos, square_size, square_size])

    for row in range(board_height):
        for col in range(board_width):
            if chessboard[row][col] is not None:
                x_pos = col * square_size
                y_pos = row * square_size
                game_display.blit(chessboard[row][col].sprite, (x_pos, y_pos))


# Main game loop
def game_loop():
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        # Draw the board
        draw_board()

        # Update the screen
        pygame.display.update()

    pygame.quit()
    quit()

# Start the game
game_loop()
