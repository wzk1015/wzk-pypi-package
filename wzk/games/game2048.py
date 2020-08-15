from os import system
from random import randint, choice

board = None


def vacant(a, b):
    return board[a][b] == ""


def initial():
    global board
    board = [["" for i in range(4)] for j in range(4)]
    board[randint(0, 3)][randint(0, 3)] = 2
    while True:
        a, b = randint(0, 3), randint(0, 3)
        if vacant(a, b):
            board[a][b] = 2
            break


def showboard():
    system("cls")
    for i in range(4):
        print("|", end="")
        for j in range(4):
            print(str(board[i][j]).center(4), end="|")
        print("")


def show(old):
    system("cls")
    for i in range(4):
        print("|", end="")
        for j in range(4):
            print(str(old[i][j]).center(4), end="|")
        print("")


def move():
    a = input().lower()
    old = [["" for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            old[i][j] = board[i][j]
    if (a == "quit"):
        showboard()
        for i in range(4):
            board[i] = ["Q", "U", "I", "T"]
        return

    for i in range(4):
        temp = []  #store none-vacant value in row[i] with order
        if (a == "w"):
            for j in range(4):
                if not vacant(j, i):
                    temp.append(board[j][i])
        elif (a == "a"):
            for j in range(4):
                if not vacant(i, j):
                    temp.append(board[i][j])
        elif (a == "s"):
            for j in range(4):
                if not vacant(3 - j, i):
                    temp.append(board[3 - j][i])
        elif (a == "d"):
            for j in range(4):
                if not vacant(i, 3 - j):
                    temp.append(board[i][3 - j])

        if len(temp) == 4:
            if temp[0] == temp[1] and temp[2] == temp[3]:
                temp[0] = 2*temp[1]
                temp[1] = 2*temp[2]
                del temp[3]
                del temp[2]
            elif temp[0] == temp[1]:
                temp[0] = 2*temp[1]
                del temp[1]
            elif temp[1] == temp[2]:
                temp[1] = 2*temp[1]
                del temp[2]
            elif temp[2] == temp[3]:
                temp[2] = 2*temp[3]
                del temp[3]
        elif len(temp) == 3:
            if temp[0] == temp[1]:
                temp[0] = 2*temp[1]
                del temp[1]
            elif temp[1] == temp[2]:
                temp[1] = 2*temp[1]
                del temp[2]
        elif len(temp) == 2:
            if temp[0] == temp[1]:
                temp[0] = 2*temp[1]
                del temp[1]

        if (a == "w"):
            for j in range(len(temp)):
                board[j][i] = temp[j]
            for j in range(len(temp), 4):
                board[j][i] = ""
        elif (a == "a"):
            for j in range(len(temp)):
                board[i][j] = temp[j]
            for j in range(len(temp), 4):
                board[i][j] = ""
        elif (a == "s"):
            for j in range(len(temp)):
                board[3 - j][i] = temp[j]
            for j in range(len(temp), 4):
                board[3 - j][i] = ""
        elif (a == "d"):
            for j in range(len(temp)):
                board[i][3 - j] = temp[j]
            for j in range(len(temp), 4):
                board[i][3 - j] = ""

    if (old == board):  #没有任何变化，重新输入
        return False

    while True:
        a, b = randint(0, 3), randint(0, 3)
        if vacant(a, b):
            board[a][b] = choice([2, 4])
            break
    return True


def judge_lose():
    for i in range(4):
        for j in range(4):
            if vacant(i, j):
                return False
    temp = []
    for i in range(4):
        for j in range(4):
            if not vacant(i, j):
                temp.append(board[i][j])
        if len(temp) == 4:
            if temp[0] == temp[1] or temp[1] == temp[2] or temp[2] == temp[3]:
                return False
        elif len(temp) == 3:
            if temp[0] == temp[1] or temp[1] == temp[2]:
                return False
        elif len(temp) == 2:
            if temp[0] == temp[1]:
                return False
    temp = []
    for i in range(4):
        for j in range(4):
            if not vacant(j, i):
                temp.append(board[j][i])
        if len(temp) == 4:
            if temp[0] == temp[1] or temp[1] == temp[2] or temp[2] == temp[3]:
                return False
        elif len(temp) == 3:
            if temp[0] == temp[1] or temp[1] == temp[2]:
                return False
        elif len(temp) == 2:
            if temp[0] == temp[1]:
                return False

    return True


def play():
    print("Welcome to wzk's 2048!")
    print("Press enter to begin")
    input()

    initial()
    showboard()
    while judge_lose() == False:
        if (move()):
            showboard()

    print("You lose!hahaha")
    print("Byebye!")
    print("Press enter to quit")
    input()


if __name__ == "__main__":
    play()