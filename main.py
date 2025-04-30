import os
import time
import copy
import random

# Initialize game-wide variables
game_record = []
playing = True

game_board = ['-'] * 9
currentTurn = 1 if random.random() < .5 else -1
playerPiece = ''
botPiece = ''

# Procedure that initializes board and individual game variables - returns nothing
def initGame() -> None:
    global game_board
    global currentTurn
    game_board = ['-'] * 9
    currentTurn = 1 if random.random() < .5 else -1 # randomly choose who starts first

# Procedure that makes a move on the board - returns the new board and turn after the move is applied
def makeMove(board: list[int], move: int, turn: int) -> tuple[list[list], int]:
    board[move] = playerPiece if turn == 1 else botPiece
    turn *= -1 # switch turns
    return board, turn

# Procedure that displays the current players turn - returns nothing
def displayTurn(currentTurn: int) -> None:
    print(f'Player turn: {"User" if currentTurn == 1 else "Bot"}')
    
# Procedure that diplays a board state to the user - returns nothing
def displayBoard(board: list[int]) -> None:
    for i in range(3):
        print('  '.join(board[i * 3:i * 3 + 3]))
    print() # Add new line for spacing

# Procedure that displays the current game outcome - returns nothing
def displayGameOutcome(outcome: int) -> None:
    global game_board
    displayBoard(game_board)
    if outcome == 0: # tie
        print('You Tied!')
    elif outcome == 1: # win
        print('You Win!')
    elif outcome == -1: # loss
        print('You Lose!')
    else:
        print('Error: Something Went Wrong')

# Procedure that checks if a move is valid - returns true if the move is valid and false if it is not
def isValidMove(board: list[int], move: int) -> bool:
    return 0 <= move <= 8 and board[move] == '-'

# Procedure that find all possible moves given a board state - returns a list of all possible moves
def getPossibleMoves(board: list[int]) -> list[int]:
    moves = []
    for i in range(len(board)):
        if isValidMove(board, i): # Move is valid, append it to the moves list
            moves.append(i)
    return moves

# Procedure that gets the bots next move - returns the move index of it's next move
def botMove(board: list[int], currentTurn: int) -> int:
    move, _ = minimax(board, currentTurn) # Use the minmax algorithm to find the optimal move
    return move

# Recursive minimax algorithim for calculating the best move for a given board state and turn
# - returns the best move for a given board and its score
def minimax(board: list[int], currentTurn: int) -> tuple[int, int]:
    if isGameOver(board):
        return -1, getGameOutcome(board)
    # Initialize score and move variables
    score = - currentTurn * 100 # make score start out as an extreme number so that any score will initially be better
    bestMove = None
    # Iterate though all possible moves to find the best move
    for move in getPossibleMoves(board):
        new_board, new_turn = makeMove(copy.deepcopy(board), move, currentTurn)
        _, move_score = minimax(new_board, new_turn)

        # If this move results in a better score, save it
        if (currentTurn == -1 and move_score < score) or (currentTurn == 1 and move_score > score):
            # Save current best move as well as the score for later comparison
            score = move_score
            bestMove = move
    # Return the best move along with the score
    return bestMove, score * .9 # multiplying score by .9 to prioritze earlier wins

# Procedure that checks if the game is over - returns true if the game is over and false if it isn't
def isGameOver(board: list[int]) -> bool:
    return not (getGameOutcome(board) is False) # Using 'is' because 0 is considered as False when == is used
    # so ties would be not be treated as a game over

# Procedure that detimines the result of the game (1 if player won or -1 if the bot won)
# returns False if it is not over
def getGameOutcome(board: list[int]) -> any:
    # Check row win
    for row in [board[0:3], board[3:6], board[6:9]]:
        if row[0] != '-' and row[0] == row[1] == row[2]:
            return 1 if row[0] == playerPiece else -1
    # Check column win
    for column in [[board[0], board[3], board[6]], [board[1], board[4], board[7]], [board[2], board[5], board[8]]]:
        if column[0] != '-' and column[0] == column[1] == column[2]:
            return 1 if column[0] == playerPiece else -1
    # Check diagonal win
    for diagonal in [[board[0], board[4], board[8]], [board[2], board[4], board[6]]]:
        if diagonal[0] != '-' and diagonal[0] == diagonal[1] == diagonal[2]:
            return 1 if diagonal[0] == playerPiece else -1
    # Check for tie
    if not any(piece == '-' for piece in board):
        return 0
    return False

# Procedure that plays one Tic Tac Toe game - returns the outcome of the game
def playGame() -> int:
    global currentTurn
    global game_board
    # individual game Loop
    while not isGameOver(game_board):
        os.system('clear')
        displayTurn(currentTurn)
        displayBoard(game_board)
        if (currentTurn == 1):
            # Ask for the players move
            print(f'Available moves: {", ".join([str(move + 1) for move in getPossibleMoves(game_board)])}. ')
            player_input = input('Enter in a valid move (1-9): ') # displaying moves from 1-9 for better readability
            if player_input.isdigit():
                move = int(player_input) - 1
            else:
                move = -1
        else:
            # Bot makes a move
            time.sleep(1.5)
            move = botMove(game_board, currentTurn)
        if isValidMove(game_board, move):
            game_board, currentTurn = makeMove(game_board, move, currentTurn)
        else:
            # move is invalid, do not apply it
            # The user will be prompted to enter a move again when the loop repeats
            pass
    os.system('clear')
    outcome = getGameOutcome(game_board)

    # append game outcome to the game record list
    game_record.append(outcome)
    return outcome

# Procedure that displays the users record that is stored in the game record list - returns nothing
def displayGameRecord() -> None:
    global game_record
    wins = game_record.count(1)
    ties = game_record.count(0)
    loses = game_record.count(-1)
    print(f'Game Record:\nWins: {wins}\nTies: {ties}\nLoses: {loses}')

# Procedure that asks if the user want to continue playing - returns True if yes otherwise False
def checkIfUserStillWantsToPlay() -> bool:
    decision = ''
    while decision != 'y' and decision != 'n':
        decision = input('Do you want to play another game (y/n)? ').lower()
    return True if decision == 'y' else False

# Procedure that displays the starting instructions - returns nothing
def showStartingInstructions() -> None:
    global botPiece
    global playerPiece
    print('Welcome to Tic-Tac-Toe')
    time.sleep(3)
    playerPiece = ''
    while playerPiece != 'X' and playerPiece != 'O':
        os.system('clear')
        playerPiece = input('Do you want to be X\'s or O\'s? ').upper()
    botPiece = 'O' if playerPiece == 'X' else 'X'
    os.system('clear')
    print('When entering in moves, the numbers are as follows:')
    displayBoard([str(i+1) for i in range(9)])


os.system('clear')
showStartingInstructions()
time.sleep(4)

# Game loop
while playing:
    os.system('clear')
    initGame()
    outcome = playGame()
    displayGameOutcome(outcome)
    time.sleep(4)
    os.system('clear')
    displayGameRecord()
    playing = checkIfUserStillWantsToPlay()

os.system('clear')
print('Thanks for playing!')
