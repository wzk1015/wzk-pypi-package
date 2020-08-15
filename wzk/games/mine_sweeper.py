from random import randint
from os import system
from time import time

SIZE = NUM_MINE = board = vis = mines = cleared = sweep = None

def countNum(i, j):
    count = 0
    positions = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1),
                 (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
    for pos in positions:
        if pos[0] < 0 or pos[0] >= SIZE or pos[1] < 0 or pos[1] >= SIZE:
            continue
        if (pos[0], pos[1]) in mines:
            count += 1
    return count


def init():
    global mines
    global board
    global vis
    global sweep

    for i in range(SIZE):
        board.append([])
        vis.append([])
        cleared.append([])
        sweep.append([])
        for j in range(SIZE):
            board[i].append("0")
            vis[i].append(False)
            cleared[i].append(False)
            sweep[i].append(False)

    while len(mines) < NUM_MINE:
        a = randint(0, SIZE - 1)
        b = randint(0, SIZE - 1)
        if (a, b) not in mines:
            board[a][b] = "X"
            mines.add((a, b))
            continue

    for i in range(SIZE):
        for j in range(SIZE):
            if (i, j) not in mines:
                board[i][j] = str(countNum(i, j))


def showRealBoard():
    print("   ", end="")
    st = ""
    for k in range(1, SIZE + 1):
        st += str(k).ljust(3)
    print(st + "\n   ", end="")
    for k in range(len(st) - 1):
        print("-", end="")
    print()

    for i in range(SIZE):
        print(str(i + 1).ljust(2) + "|", end="")
        for j in range(SIZE):
            print(str(board[i][j]).ljust(2), end=" ")
        print()
    print()


def showUserBoard():
    print("   ", end="")
    st = ""
    for k in range(1, SIZE + 1):
        st += str(k).ljust(3)
    print(st + "\n   ", end="")
    for k in range(len(st) - 1):
        print("-", end="")
    print()

    for i in range(SIZE):
        print(str(i + 1).ljust(2) + "|", end="")
        for j in range(SIZE):
            if sweep[i][j]:
                print("S".ljust(2), end=" ")
            elif vis[i][j]:
                print(str(board[i][j]).ljust(2), end=" ")
            else:
                print('-'.ljust(2), end=" ")
        print()
    print()


def clear(i, j):
    global vis
    global cleared
    positions = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1),
                 (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
    if cleared[i][j]:
        return
    cleared[i][j] = True
    for pos in positions:
        a = pos[0]
        b = pos[1]
        if a < 0 or a >= SIZE or b < 0 or b >= SIZE:
            continue
        vis[a][b] = True
        if board[a][b] == "0":
            clear(a, b)


def move():
    global vis
    global flag
    global cleared
    global sweep

    try:
        action = input("Make a move: ").split(" ")
        a = int(action[0]) - 1
        b = int(action[1]) - 1
        if len(action) > 2:
            c = int(action[2])
        else:
            c = 1
        m = board[a][b]
    except (IndexError, ValueError):
        return "error"

    if c == 0:
        sweep[a][b] = not sweep[a][b]
    else:
        if sweep[a][b]:
            return "error"
        if m == "X":
            return "lose"
        elif m == "0":
            for i in range(SIZE):
                for j in range(SIZE):
                    cleared[i][j] = False
            vis[a][b] = True
            clear(a, b)
            pass
        else:
            vis[a][b] = True

    sweep_mines = set()
    for i in range(SIZE):
        for j in range(SIZE):
            if sweep[i][j]:
                sweep_mines.add((i, j))
    if sweep_mines == mines:
        return "win"


def play():
    global SIZE, NUM_MINE, board, vis, mines, cleared, sweep
    print("WZK'S MineSweeper")
    print("input format:\nrow colomn    (for open)\nrow colomn 0  (for sweep)\n")
    SIZE = int(input("size of the board: "))
    NUM_MINE = int(input("number of mines:   "))

    while NUM_MINE > SIZE ** 2 or SIZE <= 0 or NUM_MINE <= 0:
        print("Too many mines!")
        SIZE = int(input("size of the board: "))
        NUM_MINE = int(input("number of mines:   "))
    best_time = 99999999

    while True:
        board = []
        vis = []
        mines = set()
        cleared = []
        sweep = []

        init()
        showUserBoard()
        start = time()
        while True:
            ret = move()
            _ = system("cls")
            if ret == "win":
                showRealBoard()
                end = time()
                timecost = end - start
                print("YOU WIN!!!!!!!!!!")
                print("TIME: " + str(timecost))
                if timecost < best_time:
                    print("NEW HIGH SCORE!")
                    best_time = timecost
                elif best_time != 99999999:
                    print("HIGH SCORE: " + str(best_time))
                break
            elif ret == "lose":
                showRealBoard()
                print("BOOM!!!!! YOU DIED!!!!!")
                break
            elif ret == "error":
                showUserBoard()
                print("Wrong input, try again!")
            else:
                showUserBoard()

        a = input("q to quit, other to try again\n")
        if a == "q":
            break
        _ = system("cls")


if __name__ == '__main__':
    play()