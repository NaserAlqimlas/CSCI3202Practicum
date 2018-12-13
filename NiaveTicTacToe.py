#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
import copy as cp
from os import system


PLAYER = -1
COMPUTER = +1
gameBoard = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def winCondition(state):
    if possilbeWins(state, COMPUTER):
        score = +1
    elif possilbeWins(state, PLAYER):
        score = -1
    else:
        score = 0

    return score


def possilbeWins(state, upNext):
    winningStates = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [upNext, upNext, upNext] in winningStates:
        return True
    else:
        return False


def terminate(state):
    return possilbeWins(state, PLAYER) or possilbeWins(state, COMPUTER)


def possibleMoves(state):
    moves = []

    for x, row in enumerate(state):
        for y, move in enumerate(row):
            if move == 0: moves.append([x, y])
    return moves


def validMoves(x, y):
    if [x, y] in possibleMoves(gameBoard):
        return True
    else:
        return False


def makeMove(x, y, upNext):
    if validMoves(x, y):
        gameBoard[x][y] = upNext
        return True
    else:
        return False

def niaveSolution(state):
    randomChoice = choice(possibleMoves(state))
    print(randomChoice)
    return randomChoice


def consoleClear():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def printBoard(state, computerMove, playerMove):
    for row in state:
        print('\n----------------')
        for space in row:
            if space == +1:
                print('|', computerMove, '|', end='')
            elif space == -1:
                print('|', playerMove, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')


def computerTurn(computerMove, playerMove):
    possibleSpaces = len(possibleMoves(gameBoard))
    if possibleSpaces == 0 or terminate(gameBoard):
        return

    consoleClear()
    print('Computer turn [{}]'.format(computerMove))
    printBoard(gameBoard, computerMove, playerMove)

    if possibleSpaces == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = niaveSolution(gameBoard)
        x, y = move[0], move[1]

    makeMove(x, y, COMPUTER)
    time.sleep(1)


def upNextTurn(computerMove, playerMove):
    possibleSpaces = len(possibleMoves(gameBoard))
    if possibleSpaces == 0 or terminate(gameBoard):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    consoleClear()
    print('PLAYER turn [{}]'.format(playerMove))
    printBoard(gameBoard, computerMove, playerMove)

    while (move < 1 or move > 9):
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            try_move = makeMove(coord[0], coord[1], PLAYER)

            if try_move == False:
                print('Bad move')
                move = -1
        except KeygameBoardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')


def main():
    consoleClear()
    playerMove = '' # X or O
    computerMove = '' # X or O
    first = ''  # if PLAYER is the first

    # PLAYER chooses X or O to play
    while playerMove != 'O' and playerMove != 'X':
        try:
            print('')
            playerMove = input('Choose X or O\nChosen: ').upper()
        except KeygameBoardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')

    # Setting Computer's choice
    if playerMove == 'X':
        computerMove = 'O'
    else:
        computerMove = 'X'

    # PLAYER may starts first
    consoleClear()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except KeygameBoardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')

    # Main loop of this game
    while len(possibleMoves(gameBoard)) > 0 and not terminate(gameBoard):
        if first == 'N':
            computerTurn(computerMove, playerMove)
            first = ''

        upNextTurn(computerMove, playerMove)
        computerTurn(computerMove, playerMove)

    # Game over message
    if possilbeWins(gameBoard, PLAYER):
        consoleClear()
        print('PLAYER turn [{}]'.format(playerMove))
        printBoard(gameBoard, computerMove, playerMove)
        print('YOU WIN!')
    elif possilbeWins(gameBoard, COMPUTER):
        consoleClear()
        print('Computer turn [{}]'.format(computerMove))
        printBoard(gameBoard, computerMove, playerMove)
        print('YOU LOSE!')
    else:
        consoleClear()
        printBoard(gameBoard, computerMove, playerMove)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
