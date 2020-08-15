import random


heap = None
players = None

def four(tp, num=0):
    return [Card(tp, num), Card(tp, num), Card(tp, num), Card(tp, num)]


class Card:
    def __init__(self, tp, num=0):
        self.tp = tp
        self.num = num

    def __str__(self):
        num_dict = {
            0: "",
            1: "一",
            2: "二",
            3: "三",
            4: "四",
            5: "五",
            6: "六",
            7: "七",
            8: "八",
            9: "九",
        }
        return num_dict[self.num] + self.tp

    def __eq__(self, other):
        return self.tp == other.tp and self.num == other.num


class CardsHeap:
    def __init__(self):
        self.total_number = 136
        self.cards = []
        self.cards.extend(four("東"))
        self.cards.extend(four("南"))
        self.cards.extend(four("西"))
        self.cards.extend(four("北"))
        self.cards.extend(four("中"))
        self.cards.extend(four("發"))
        self.cards.extend(four("白"))
        for i in range(1, 10):
            self.cards.extend(four("萬", i))
            self.cards.extend(four("筒", i))
            self.cards.extend(four("条", i))
        random.shuffle(self.cards)

    def draw(self, num=1):
        ans = []
        for i in range(num):
            ans.append(self.cards.pop())
        return ans

    def discard(self, card):
        self.cards.append(card)
        random.shuffle(self.cards)


class Player:
    def __init__(self, heap, index):
        self.cards = []
        self.cards.extend(heap.draw(13))
        self.index = index
        self.heap = heap

        self.show_card()
        self.rearrange()

    def show_card(self):
        print("玩家", self.index, "的卡牌：")
        for i in range(len(self.cards)):
            print(str(i + 1) + str(self.cards[i]), end=" ")

    def rearrange(self):
        while True:
            order = input("选择需要交换的牌的序号，q退出\n")
            try:
                if order == "q":
                    return
                a, b = int(order.split()[0]) - 1, int(order.split()[1]) - 1
                card_b = self.cards[b]
                card_a = self.cards[a]
                self.cards[a] = card_b
                self.cards[b] = card_a
                self.show_card()
            except (IndexError, TypeError):
                print("错误输入！")

    def take_turn(self, ps):
        self.cards.extend(self.heap.draw())
        self.judge_win()
        self.show_card()
        self.rearrange()

        while True:
            order = input("选择弃牌")
            try:
                a = int(order.split()[0])
                card = self.cards.pop(a)
                print(self, "弃牌", card)
                heap.discard(card)

                if not ps[ps.index(self) + 1].chi(card):
                    for p in ps:
                        if p != self:
                            p.peng(card)
                            p.gang(card)

                self.judge_win()
                return

            except (IndexError, TypeError, ValueError):
                print("错误输入！")

    def chi(self, card):
        while True:
            order = input(str(self) + "吃？q退出")
            try:
                if order == "q":
                    return False
                a, b = self.cards[int(order.split()[0]) - 1], self.cards[int(order.split()[1]) - 1]
                lst = sorted([a.num, b.num, card.num])
                if a.tp == b.tp == card.tp and lst[0] == lst[1] - 1 == lst[2] - 2:
                    print(self, "吃：", a, " ", b)
                    heap.discard(a)
                    heap.discard(b)
                    self.judge_win()
                    return True

            except (IndexError, TypeError):
                print("错误输入！")

    def peng(self, card):
        while True:
            order = input(str(self) + "碰？q退出")
            try:
                if order == "q":
                    return False
                a, b = self.cards[int(order.split()[0]) - 1], self.cards[int(order.split()[1]) - 1]
                if a.tp == b.tp == card.tp and a.num == b.num == card.num:
                    print(self, "碰：", a, " ", b)
                    heap.discard(a)
                    heap.discard(b)
                    self.judge_win()
                    return True

            except (IndexError, TypeError):
                print("错误输入！")

    def gang(self, card):
        while True:
            order = input(str(self) + "杠？q退出")
            try:
                if order == "q":
                    return False
                a, b, c = self.cards[int(order.split()[0]) - 1], self.cards[int(order.split()[1]) - 1], \
                          self.cards[int(order.split()[2])]
                if a.tp == b.tp == c.tp == card.tp and a.num == b.num == c.num == card.num:
                    print(self, "杠：", a, " ", b, " ", c)
                    heap.discard(a)
                    heap.discard(b)
                    heap.discard(c)
                    self.judge_win()
                    return True

            except (IndexError, TypeError):
                print("错误输入！")

    def __str__(self):
        return "玩家" + str(self.index)

    def judge_win(self):
        self.rearrange()
        if len(self.cards)%3 != 2:
            return False
        if self.cards[-1] != self.cards[-2]:
            return False
        m = len(self.cards)//3
        for i in range(m):
            sub = sorted(self.cards[i:i + 2], key=lambda k: k.num)
            if not (sub[0].tp == sub[1].tp == sub[2].tp
                    and sub[0].num == sub[1].num - 1 == sub[2].num - 2) \
                    and not (sub[0] == sub[1] == sub[2]):
                return False
        print(self, "胜利！")
        self.show_card()
        exit()


def play():
    print("welcome to wzk's mahjong!\nI never really test this program, so whatever..")
    global heap, players
    heap = CardsHeap()
    player1 = Player(heap, 1)
    player2 = Player(heap, 2)
    player3 = Player(heap, 3)
    player4 = Player(heap, 4)
    players = [player1, player2, player3, player4]
    while True:
        for player in players:
            player.take_turn(players)


if __name__ == '__main__':
    play()