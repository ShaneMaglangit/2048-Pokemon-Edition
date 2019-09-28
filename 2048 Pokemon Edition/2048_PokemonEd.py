import pygame
import random
import sys
import os

# Ensrues the path of the assets
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()

# Top Level Variable Declarations
# Resources
tiles = [
    pygame.image.load(resource_path('assets\\tile0.png')), pygame.image.load(resource_path('assets\\tile1.png')), pygame.image.load(resource_path('assets\\tile2.png')),
    pygame.image.load(resource_path('assets\\tile3.png')), pygame.image.load(resource_path('assets\\tile4.png')), pygame.image.load(resource_path('assets\\tile5.png')),
    pygame.image.load(resource_path('assets\\tile6.png')), pygame.image.load(resource_path('assets\\tile7.png')), pygame.image.load(resource_path('assets\\tile8.png')),
    pygame.image.load(resource_path('assets\\tile9.png')), pygame.image.load(resource_path('assets\\tile10.png'))
]

imgRetry = pygame.image.load(resource_path('assets\\retry.png'))
imgGuide = pygame.image.load(resource_path('assets\\guide.png'))
imgDirection = pygame.image.load(resource_path('assets\\direction.png'))

defaultFont = pygame.font.SysFont('Bauhaus 93', 120)

# Dimensions
windowHeight = 770
windowWidth = 675
defaultMargin = 15

board = [[None for i in range(4)] for j in range(4)]  # 4x4 Matrix
boardLength = len(board)

menuRect = pygame.Rect(0, 0, windowWidth, 100)
retryRect = pygame.Rect(defaultMargin, defaultMargin, 100, 100)
tilesRect = pygame.Rect(0, menuRect.height, windowWidth, windowHeight - menuRect.height)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
primary = (155, 121, 96)

# Other declarations
clock = pygame.time.Clock()
window = None

start = False
username = ''


# Classes
class Tiles(pygame.Surface):
    def __init__(self, image, xpos=0, ypos=0):
        self.image = image
        self.xpos = xpos
        self.ypos = ypos
        self.width = image.get_width()
        self.height = image.get_height()
        self.selected = False
        self.rect = pygame.Rect(xpos, ypos, image.get_width(), image.get_height())


# Functions
# Used to set up the game resources.
def setup():
    global window, board, username

    window = pygame.display.set_mode((windowWidth, windowHeight))

    # Setup the window
    pygame.display.set_caption('2048: Pokemon Edition')
    window.fill(white)
    pygame.display.flip()

    # Get the username
    if username == '':
        username = getUsername()

    # Set up the board
    xCoord = 0 + defaultMargin
    yCoord = menuRect.height + defaultMargin

    for row in range(boardLength):
        for col in range(boardLength):
            board[row][col] = Tiles(tiles[0], int(xCoord), int(yCoord))
            xCoord += board[row][col].width + defaultMargin
        xCoord = 0 + defaultMargin
        yCoord += board[row][col].height + defaultMargin

    displayMenu()
    displayTiles()
    generateTile()
    generateTile()
    displayDirection()


# Used to display the menu section
def displayMenu():
    pygame.draw.rect(window, white, menuRect)
    window.blit(imgRetry, (defaultMargin, defaultMargin))
    window.blit(imgGuide, (imgRetry.get_width() + defaultMargin * 2, defaultMargin))
    pygame.display.update(menuRect)


# Used to display the tiles
def displayTiles():
    pygame.draw.rect(window, white, tilesRect)

    for row in board:
        for col in row:
            window.blit(col.image, (col.xpos, col.ypos))

    pygame.display.update(tilesRect)


# Used to display the direction
def displayDirection():
    window.blit(imgDirection, (tilesRect.left + defaultMargin, tilesRect.top + defaultMargin))
    pygame.display.update(tilesRect)


# Used to generate new tiles
def generateTile():
    i = random.randint(1, 2)
    x = random.randint(0, 3)
    y = random.randint(0, 3)

    if board[x][y].image == tiles[0]:
        board[x][y].image = tiles[i]

        currentTile = board[x][y]
        tempHeight = currentTile.height - 120
        tempWidth = currentTile.height - 120

        # gradually scales up the generating tile
        while tempHeight != currentTile.height and tempWidth != currentTile.width:
            tempHeight += 1
            tempWidth += 1

            tempImage = pygame.transform.scale(currentTile.image, (tempWidth, tempHeight))
            tempx = currentTile.xpos + currentTile.rect.width / 2 - tempWidth / 2
            tempy = currentTile.ypos + currentTile.rect.height / 2 - tempHeight / 2

            window.blit(tempImage, (tempx, tempy))
            pygame.display.update(currentTile.rect)
    else:
        generateTile()


# Used to move the tiles
def move(row_start, row_end, col_start, col_end, row_dir, col_dir):
    moves = 0
    row = row_start
    
    while row != row_end:
        col = col_start
        
        while col != col_end:
            next_row = row + row_dir
            next_col = col + col_dir

            while 0 <= next_col <= 3 and 0 <= next_row <= 3:
                if board[next_row][next_col].image != tiles[0]:
                    if board[next_row][next_col].image == board[row][col].image:
                        board[row][col].image = tiles[tiles.index(board[row][col].image) + 1]
                        board[next_row][next_col].image = tiles[0]
                        moves += 1
                        break
                    elif board[row][col].image == tiles[0]:
                        board[row][col].image = board[next_row][next_col].image
                        board[next_row][next_col].image = tiles[0]
                        moves += 1
                    else:
                        break

                next_col += col_dir
                next_row += row_dir
                
            col += 1 if col_start < col_end else -1
        row += 1 if row_start < row_end else -1

    return moves

# Used to check if the user still has possible moves
def hasPossibleMoves():
    for row in range(boardLength):
        for col in range(boardLength):
            currentTile = board[row][col].image
            surroundingTiles = []

            if row > 0:
                surroundingTiles.append(board[row - 1][col].image)

            if row < len(board) - 1:
                surroundingTiles.append(board[row + 1][col].image)

            if col > 0:
                surroundingTiles.append(board[row][col - 1].image)

            if col < len(board) - 1:
                surroundingTiles.append(board[row][col + 1].image)

            if currentTile in surroundingTiles or tiles[0] in surroundingTiles:
                return True

    return False

# Used to check if the user won the game
def gameIsWon():
    for row in board:
        for tile in row:
            if tile.image == tiles[-1]:
                return True

    return False


# Used to show banner messages
def showBanner(username, isWinner):
    if isWinner:
        banner = pygame.image.load(resource_path('assets\\win.png'))
        txtUsername = defaultFont.render(username, True, primary)

        window.blit(banner, (15, 115))

        # display the text at the center
        window.blit(txtUsername, (tilesRect.width / 2 - txtUsername.get_width() / 2, 360))
    else:
        banner = pygame.image.load(resource_path('assets\\lose.png'))
        window.blit(banner, (15, 115))

    pygame.display.update(tilesRect)


# Used to get username of the user.
def getUsername():
    background = pygame.image.load(resource_path('assets\\username.png'))
    name = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            txtUsername = defaultFont.render(name, True, primary)

            if event.type == pygame.KEYDOWN:
                # Catch if user pressed the enter key
                if event.key == pygame.K_RETURN:
                    if name != '':
                        window.fill(white)
                        pygame.display.flip()

                    return name
                else:
                    # Delete existing letters on the current input
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    # Add the new character
                    else:
                        name += event.unicode

                    txtUsername = defaultFont.render(name, True, primary)
                    
            window.fill(white)
            window.blit(background, (0, 0))
            window.blit(txtUsername, (windowWidth / 2 - txtUsername.get_width() / 2, 340))
            pygame.display.flip()


# Used to run the overall program
def gameLoop():
    global start

    setup()

    while True:
        # get the position and actions of the mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Do not catch key events until user press spacebar
            if event.type == pygame.KEYUP:
                if start:
                    # Keep catching actions until game is over
                    if hasPossibleMoves() and not gameIsWon():
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                            if event.key == pygame.K_UP: 
                                moves = move(0, 3, 0, 4, 1, 0)
                            elif event.key == pygame.K_DOWN:
                                moves = move(3, -1, 0, 4, -1, 0)
                            elif event.key == pygame.K_LEFT:
                                moves = move(0, 4, 0, 3, 0, 1)
                            else:
                                moves = move(0, 4, 3, -1, 0, -1)
                            displayTiles()

                            # Only generate a new tile if a move has been made
                            if moves > 0:
                                generateTile()

                            # Show banners once game is over
                            if gameIsWon():
                                showBanner(username, True)
                            elif not hasPossibleMoves():
                                showBanner(username, False)

                    if event.key == pygame.K_SPACE:
                        start = False
                        gameLoop()
                else:
                    if event.key == pygame.K_SPACE:
                        displayTiles()
                        start = True

            # Check if the user hovers on the retry button
            if imgRetry.get_width() + defaultMargin > mouse[0] > defaultMargin and \
                    imgRetry.get_height() + defaultMargin > mouse[1] > defaultMargin:
                # Scale up the button
                tempRetry = pygame.transform.scale(imgRetry, (imgRetry.get_width() + 10, imgRetry.get_height() + 10))

                # Update the button
                pygame.draw.rect(window, white, retryRect)
                window.blit(tempRetry, (defaultMargin, defaultMargin))
                pygame.display.update(retryRect)

                # If the button is clicked, reset the game
                if click[0] == 1:
                    start = False
                    gameLoop()
            else:
                # Scale down the button
                pygame.draw.rect(window, white, retryRect)
                window.blit(imgRetry, (defaultMargin, defaultMargin))
                pygame.display.update(retryRect)

        pygame.display.flip()
        clock.tick(60)


# Execution
gameLoop()
