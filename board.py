import pygame

# Set up the dimensions of the window
window_width = 400
window_height = 400

# Set up the dimensions of the board
board_width = 8
board_height = 8
square_size = 50

# Set up the colors
white = (255, 0, 0)
black = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Create the game window
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Chessboard")

# Create the chessboard
def draw_board():
    for row in range(board_height):
        for col in range(board_width):
            x_pos = col * square_size
            y_pos = row * square_size
            if (row + col) % 2 == 0:
                pygame.draw.rect(game_display, white, [x_pos, y_pos, square_size, square_size])
            else:
                pygame.draw.rect(game_display, black, [x_pos, y_pos, square_size, square_size])

# Main game loop
def game_loop():
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        # Draw the board
        draw_board()

        piece_image = pygame.image.load("pawn.png")
        resized_image = pygame.transform.scale(piece_image, (50, 50))
        game_display.blit(resized_image, (0, 0))

        # Update the screen
        pygame.display.update()



    pygame.quit()
    quit()

# Start the game
game_loop()


