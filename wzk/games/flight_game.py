"""
board:

77  78  080910111213149481  82
        07    65    15
79  80  06    66    16  83  84
93      05    67    17
01020304      68      18192021
52            69            22
51            70            23
50535455565758  64636261605924
49            76            25
48            75            26
47464544      74      30292827
        43    73    31      95
85  86  42    72    32  89  90
        41    71    33
87  889640393837363534  91  92
"""

from random import randint

bg_color_dict = {"red": "41", "green": "42", "yellow": "43", "blue": "44", "black": "40", "white": "47"}
fg_color_dict = {"red": "31", "green": "32", "yellow": "33", "blue": "34", "black": "30", "white": "37"}

board = None


def roll(a):
    return randint(1, 6)


def fly(pos, num):
    if pos + num > 52:
        return pos + num - 52
    return pos + num


class Plane:
    def __init__(self, color, num, owner):
        self.owner = owner
        self.color = color
        self.arrived = False
        self.num = num
        if color == "red":
            self.symbol = "R" + str(self.num)
            self.park = 84 + self.num
        if color == "yellow":
            self.symbol = "Y" + str(self.num)
            self.park = 76 + self.num
        if color == "green":
            self.symbol = "G" + str(self.num)
            self.park = 88 + self.num
        if color == "blue":
            self.symbol = "B" + str(self.num)
            self.park = 80 + self.num
        self.pos = self.park

    def arrive(self):
        self.arrived = True
        self.pos = self.park
        self.symbol = self.symbol[0] + "!"
        self.owner.update_status()
        print("Wow! Your plane arrived!")

    def move(self, dice):
        def fly_across():
            if self.pos == 5 and self.color == "red":
                if len(board.points[67].planes) > 0:
                    board.points[67].kick(self)
                self.pos = 17
                print("FLY ACROSS!")
            elif self.pos == 18 and self.color == "yellow":
                if len(board.points[61].planes) > 0:
                    board.points[61].kick(self)
                self.pos = 30
                print("FLY ACROSS!")
            elif self.pos == 31 and self.color == "blue":
                if len(board.points[73].planes) > 0:
                    board.points[73].kick(self)
                self.pos = 43
                print("FLY ACROSS!")
            elif self.pos == 44 and self.color == "green":
                if len(board.points[55].planes) > 0:
                    board.points[55].kick(self)
                self.pos = 4
                print("FLY ACROSS!")

        board.points[self.pos].fly_out(self)
        if self.pos in self.owner.airport:
            # Take off
            self.pos = self.owner.ready
        elif self.pos == self.owner.ready:
            self.pos = self.owner.start + dice
            if dice in [2, 6]:
                self.pos += 4
        elif 1 <= self.pos <= 52:
            if not (self.pos + dice > self.owner.end >= self.pos):
                self.pos = fly(self.pos, dice)

                fly_across()

                # add 4
                if board.points[self.pos].color == self.color:
                    if not (self.pos + 4 > self.owner.end >= self.pos):
                        self.pos = fly(self.pos, 4)

                fly_across()

            else:
                # Come to end
                dis = self.owner.end - self.pos
                self.pos = self.owner.sprint + dice - dis - 1

        elif 52 <= self.pos <= 76:
            new_pos = self.pos + dice
            if new_pos > self.owner.sprint + 6:
                dis = self.owner.sprint + 6 - self.pos
                self.pos = self.owner.sprint + 6 - (dice - dis)
            elif new_pos == self.owner.sprint + 6:
                self.arrive()
            else:
                self.pos = new_pos
        board.points[self.pos].fly_in(self)

    def kick_out(self):
        self.pos = self.park
        board.points[self.pos].fly_in(self)
        print("{0} WAS KICKED OUT!!!".format(self.color.capitalize()))


class Player:
    def __init__(self, color):
        self.color = color
        self.planes = [Plane(color, 1, self), Plane(color, 2, self), Plane(color, 3, self), Plane(color, 4, self)]
        self.status = 0
        if self.color == "red":
            self.airport = [85, 86, 87, 88]
            self.start = 39
            self.end = 37
            self.sprint = 71
            self.ready = 96
        elif self.color == "yellow":
            self.airport = [77, 78, 79, 80]
            self.start = 0
            self.end = 50
            self.sprint = 53
            self.ready = 93
        elif self.color == "green":
            self.airport = [89, 90, 91, 92]
            self.start = 26
            self.end = 24
            self.sprint = 59
            self.ready = 95
        elif self.color == "blue":
            self.airport = [81, 82, 83, 84]
            self.start = 13
            self.end = 11
            self.sprint = 65
            self.ready = 94

    def init_board(self):
        for plane in self.planes:
            board.points[plane.pos].fly_in(plane)

    def update_status(self):
        self.status += 1

    def count_not_fly_planes(self):
        count = 0
        for plane in self.planes:
            if plane.pos in self.airport:
                count += 1
        return count

    def take_turn(self):
        print("Player ", end="")
        print("\033[1;{0};{0}m{1}\033[0m".format(fg_color_dict[self.color], self.color), end="")
        a = input("'s turn. Press enter to roll the dice\n")
        dice = roll(a)
        print("You got {0}!".format(str(dice)))
        if self.count_not_fly_planes() == 4 and dice not in [5, 6, 100]:
            print("You can't take off ^_^")
            board.show()
            return

        while True:
            try:
                plane = self.planes[int(input("Which plane do you want to move?\n")) - 1]
                if plane.pos in self.airport and dice not in [5, 6, 100]:
                    raise ValueError
                if plane.arrived:
                    raise ValueError
                break
            except (ValueError, IndexError):
                print("Illegal input! Try again")

        if dice == 100:
            # debug
            board.points[plane.pos].fly_out(plane)
            plane.arrive()
        else:
            plane.move(dice)

        board.show()
        if self.status == 4:
            return
        if dice == 6 or dice == 100:
            # roll again
            print("EXTRA CHANCE!")
            self.take_turn()


class Point:
    def __init__(self, number):
        self.content = "  "
        self.number = number
        self.planes = []
        if number <= 52:
            self.color = ["red", "yellow", "blue", "green"][(number - 1)%4]
        elif 53 <= number <= 58 or 77 <= number <= 80:
            self.color = "yellow"
        elif 59 <= number <= 64 or 89 <= number <= 92:
            self.color = "green"
        elif 65 <= number <= 70 or 81 <= number <= 84:
            self.color = "blue"
        elif 71 <= number <= 76 or 85 <= number <= 88:
            self.color = "red"
        elif 93 <= number <= 96:
            self.color = "white"

        self.set_content()
        self.bg_color = bg_color_dict[self.color]
        if self.color in ["yellow", "green", "white"]:
            self.fg_color = fg_color_dict["black"]
        else:
            self.fg_color = fg_color_dict["white"]

    def set_content(self):
        if len(self.planes) == 1:
            self.content = self.planes[0].symbol
        elif len(self.planes) > 1:
            self.content = self.planes[0].symbol[0]*2
        else:
            self.content = "  "

    def fly_in(self, plane):
        if self.planes:
            self.kick(plane)
        self.planes.append(plane)
        self.set_content()

    def kick(self, new_plane):
        for old_plane in self.planes:
            if old_plane.color != new_plane.color:
                self.fly_out(old_plane)
                old_plane.kick_out()
        self.set_content()

    def fly_out(self, plane):
        self.planes.remove(plane)
        self.set_content()

    def __str__(self):
        if self.color is not "white":
            return "\033[5;{2};{0}m{1}\033[0m".format(self.bg_color, self.content, self.fg_color)
        else:
            return "\033[5;{1};0m{0}\033[0m".format(self.content, self.fg_color)


class Board:
    def __init__(self):
        self.points = []
        for i in range(97):
            self.points.append(Point(i))

    def show(self):
        p = self.points
        red = "\033[1;31;31m==\033[0m"
        blue = "\033[1;34;34m==\033[0m"
        green = "\033[1;32;32m||\033[0m"
        yellow = "\033[1;33;33m||\033[0m"
        red_arrow = "\033[1;31;31m=>\033[0m"
        blue_arrow = "\033[1;34;34m<=\033[0m"
        green_arrow = "\033[1;32;32m/\\\033[0m"
        yellow_arrow = "\033[1;33;33m\\/\033[0m"

        print("{0}  {1}  {2}{3}{4}{5}{6}{7}{8}{11}{9}  {10}".format(p[77], p[78], p[8], p[9], p[10], p[11],
                                                                    p[12], p[13], p[14], p[81], p[82], p[94]))
        print("        {0}    {1}    {2}       ".format(p[7], p[65], p[15]))
        print("{0}  {1}  {2}    {3}    {4}  {5}  {6}".format(p[79], p[80], p[6], p[66], p[16], p[83], p[84]))
        print("{5}      {0}{3}{3}{1}{3}{4}{2}       ".format(p[5], p[67], p[17], red, red_arrow, p[93]))
        print("{0}{1}{2}{3}      {4}      {5}{6}{7}{8}".format(p[1], p[2], p[3], p[4], p[68], p[18], p[19], p[20],
                                                               p[21]))
        print("{0}    {3}      {1}      {4}    {2}".format(p[52], p[69], p[22], green_arrow, yellow))
        print("{0}    {3}      {1}      {4}    {2}".format(p[51], p[70], p[23], green, yellow))
        print("{0}{1}{2}{3}{4}{5}{6}  {7}{8}{9}{10}{11}{12}{13}".format(p[50], p[53], p[54], p[55], p[56],
                                                                        p[57], p[58], p[64], p[63], p[62],
                                                                        p[61], p[60], p[59], p[24]))
        print("{0}    {3}      {1}      {4}    {2}".format(p[49], p[76], p[25], green, yellow))
        print("{0}    {3}      {1}      {4}    {2}".format(p[48], p[75], p[26], green, yellow_arrow))
        print("{0}{1}{2}{3}      {4}      {5}{6}{7}{8}".format(p[47], p[46], p[45], p[44], p[74], p[30], p[29],
                                                               p[28], p[27]))
        print("        {0}{4}{3}{1}{3}{3}{2}      {5}".format(p[43], p[73], p[31], blue, blue_arrow, p[95]))
        print("{0}  {1}  {2}    {3}    {4}  {5}  {6}".format(p[85], p[86], p[42], p[72], p[32],
                                                             p[89], p[90]))
        print("        {0}    {1}    {2}".format(p[41], p[71], p[33]))
        print("{0}  {1}{11}{2}{3}{4}{5}{6}{7}{8}  {9}  {10}".format(p[87], p[88], p[40], p[39], p[38], p[37],
                                                                    p[36], p[35], p[34], p[91], p[92], p[96]))


def play():
    print("Please use PYCHARM or JUPYTER to open this! or colors will be illegal!")
    players = [Player("yellow"), Player("blue"), Player("green"), Player("red")]
    global board
    board = Board()
    for player in players:
        player.init_board()
    winners = []
    board.show()
    Exit = False
    while not Exit:
        for player in players:
            if player not in winners:
                player.take_turn()
            if player.status == 4 and player not in winners:
                winners.append(player)
                print("{1} win ! Rank {0}!\n".format(str(len(winners)), player.color.capitalize()))
            if len(winners) == 3:
                print("Game Over!")
                print("1st: " + winners[0].color)
                print("2nd: " + winners[1].color)
                print("3rd: " + winners[2].color)
                Exit = True
                break

    input("Press enter to exit")


if __name__ == '__main__':
    play()