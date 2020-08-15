import random
import os
import itertools
import time

money = point = stake = public_card = player_card = player_alive = player_all_in = None
lost_stake = sign = n = money_start = big_blind_stake_money = big_blind_stake = None


def santiao(cards):
    for combin in itertools.combinations(cards, 3):
        if combin[0][1] == combin[1][1] == combin[2][1]:
            return 50*combin[0][1]
    return 0


def sitiao(cards):
    for combin in itertools.combinations(cards, 4):
        if combin[0][1] == combin[1][1] == combin[2][1] == combin[3][1]:
            return 50*combin[0][1]
    return 0


def fullhouse(cards):
    rest = []
    for combin in itertools.combinations(cards, 3):
        if combin[0][1] == combin[1][1] == combin[2][1]:
            for i in cards:
                if not (i in combin):
                    rest.append(i)
            if rest[0][1] == rest[1][1]:
                return combin[0][1]*75 + rest[0][1]*5
    return 0


def shunzi(cards):
    if cards[1][1] - cards[0][1] == 1 and cards[2][1] - cards[1][1] == 1 and cards[3][1] - cards[2][1] == 1 and \
            cards[4][1] - cards[3][1] == 1:
        return 50*cards[4][1]
    return 0


def liangdui(cards):
    rest = []
    for combin in itertools.combinations(cards, 2):
        if combin[0][1] == combin[1][1]:
            for i in cards:
                if not (i in combin):
                    rest.append(i)
            if rest[0][1] == rest[1][1] or rest[0][1] == rest[2][1] or rest[1][1] == rest[2][1]:
                if combin[0][1] > rest[0][1]:
                    return combin[0][1]*75 + rest[0][1]*5
                else:
                    return combin[0][1]*5 + rest[0][1]*75
    return 0


def yidui(cards):
    for combin in itertools.combinations(cards, 2):
        if combin[0][1] == combin[1][1]:
            return 50*combin[0][1]
    return 0


def judge(cards):
    cards = sorted(list(cards), key=lambda x: x[1])
    point = [0, 0]
    color_same = 0
    if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0] == cards[4][0]:
        color_same = 1
    if color_same == 1 and cards[1][1] - cards[0][1] == 1 and cards[2][1] - cards[1][1] == 1 and cards[3][1] - cards[2][
        1] == 1 and cards[4][1] - cards[3][1] == 1:
        point[0] = 10000 + 50*cards[4][1]
        point[1] = "同花顺！666666"
    elif sitiao(cards) != 0:
        point[0] = 9000 + sitiao(cards)
        point[1] = "四条！66666"
    elif fullhouse(cards) != 0:
        point[0] = 8000 + fullhouse(cards)
        point[1] = "Full House!6666"
    elif color_same == 1:
        point[0] = 7000
        point[1] = "同花！666"
    elif shunzi(cards) != 0:
        point[0] = 6000 + shunzi(cards)
        point[1] = "顺子！66"
    elif santiao(cards) != 0:
        point[0] = 5000 + santiao(cards)
        point[1] = "三条！6"
    elif liangdui(cards) != 0:
        point[0] = 4000 + liangdui(cards)
        point[1] = "两对!"
    elif yidui(cards) != 0:
        point[0] = 3000 + yidui(cards)
        point[1] = "一对"
    else:
        point[0] = 0 + cards[4][1]*200 + cards[3][1]*15 + cards[2][1]*1 + cards[1][1]*0.05 + cards[0][1]*0.003
        point[1] = "高牌"

    return point


def input_new_card():
    color = int(input("颜色"))
    if color == 1:
        color = "Heart"
    if color == 2:
        color = "Club"
    if color == 3:
        color = "Diamond"
    if color == 4:
        color = "Spade"
    number = int(input("点数"))
    card = (color, number)
    return card


def test():
    while True:
        cards = []
        for i in range(5):
            cards.append(input_new_card())
        point = judge(cards)
        result = point[1]
        print("玩家" + str(i + 1) + "的牌是" + result)
        print(cards)
        print(point[0])

def judge_win():
    for i in range(n):
        if money[i] < 0:
            player_alive.remove(i)
    if len(player_alive) == 1:
        return player_alive
    return -1


def calculate_money(winner):
    total_stake = lost_stake
    winner_stake = 0
    for i in stake:
        total_stake += i
    for i in winner:
        winner_stake += stake[i]
    for i in player_all_in:
        money[i] += 2*stake[i]
    for player_win in winner:
        if not i in player_all_in:
            money[player_win] += (total_stake/(len(winner) - len(player_all_in)))


def show_money():
    for i in range(n):
        print("玩家" + str(i + 1) + "现在有" + str(int(money[i])) + "元钱")


def make_first_stake(big_blind):  #small_blind):
    global player_all_in
    global player_alive
    stake[big_blind] = 40
    print("玩家" + str(big_blind + 1) + "下大盲注" + str(big_blind_stake_money) + "元")

    #stake[small_blind]=20
    #print("玩家"+str(small_blind+1)+"下小盲注"+str(small_blind_stake_money)+"元")
    make_stake()


def make_stake():
    global player_all_in
    global player_alive
    global lost_stake

    loop_sign = 0
    big_stake = -1
    big_stake_person = -1
    for j in range(n):
        if stake[j] > big_stake:
            big_stake = stake[j]
            big_stake_person = j

    j = big_stake_person + 1
    while True:
        if not j in player_alive:
            j = renew(j)
            continue
        if j == big_stake_person:  #完成一轮下注，无人再加
            loop_sign = 1
        while True:
            while True:
                try:
                    current_stake = int(input("玩家" + str(j + 1) + "请下注，当前最大注为" + str(big_stake) + "元，不下注请输入0  "))
                    break
                except ValueError:
                    print("请输入整数！")
            if current_stake == 0 and loop_sign == 0:
                break
            if current_stake == money[j]:
                player_all_in.append(j)
                print("all in!")
                break
            elif current_stake == 0 and big_stake_person != j:
                break
            elif current_stake < big_stake or current_stake > money[j] or current_stake < stake[j]:
                print("下注必须>=此前的投注且不能<=余额，或all in，或为0，请重新输入\n")
            else:
                break
        if current_stake == 0:  #弃牌
            player_alive.remove(j)
            money[j] -= stake[j]
            lost_stake += stake[j]
            stake[j] = 0
            j = renew(j)
            if loop_sign == 1:
                break
            continue
        print("玩家" + str(j + 1) + "下注" + str(current_stake) + "元")

        stake[j] = current_stake
        if current_stake > big_stake:
            big_stake = current_stake
            big_stake_person = j
            loop_sign = 0
        j = renew(j)

        if loop_sign == 1:
            break


def renew(a):
    a += 1
    if a == n:
        a = 0
    return a


def get_new_card():
    while True:
        color = random.choice(["Heart", "Club", "Diamond", "Spade"])
        number = random.randint(1, 13)
        card = (color, number)
        if (card in public_card):
            continue
        else:
            find_sign = 0
            for i in range(n):
                if card in player_card[i]:
                    find_sign = 1
                    break
            if find_sign == 1:
                continue
            break
    return card


def get_hand_card():
    for i in range(n):
        player_card[i].append(get_new_card())
        player_card[i].append(get_new_card())
        print("第" + str(i + 1) + "个玩家，输入任意字符以查看底牌")
        input()
        print(player_card[i][0])
        print(player_card[i][1])
        print("输入任意字符以继续，并切换到下一玩家")
        input()
        os.system("cls")


def get_three_public_card():
    print("初始的公共牌为")
    for i in range(3):
        public_card.append(get_new_card())
        print(public_card[i])


def get_public_card(k):
    a = get_new_card()
    print("新加入的第" + str(k) + "张公共牌为" + str(a) + "\n现在的全部公共牌为")
    public_card.append(a)
    for i in range(k):
        print(public_card[i])


def compare_card():
    print("见证奇迹的时刻！")
    player_win = []
    for i in player_alive:
        whole_card = list(set(player_card[i] + public_card))
        single_max_point = 0
        #遍历whole_card的五元子集
        for combin in itertools.combinations(whole_card, 5):
            current_point = judge(combin)  #判断分数
            if current_point[0] > single_max_point:
                single_max_point = current_point[0]
                result = current_point[1]
                cards = combin
        point.append((i, single_max_point))
        time.sleep(2)
        print("玩家" + str(i + 1) + "的牌是" + result)
        print(cards)
    max_point = 0
    for j in point:
        if j[1] > max_point:
            max_point = j[1]
    for j in point:
        if max_point == j[1]:
            player_win.append(j[0])
    return player_win


def start():
    global money, point, stake, public_card, player_card, \
        player_alive, player_all_in, lost_stake, sign, n, \
        money_start, big_blind_stake_money, big_blind_stake
    money = []
    point = []
    stake = []
    public_card = []
    player_card = []
    player_alive = []
    player_all_in = []
    lost_stake = 0
    sign = 1  #胜负界定
    n = 0  #玩家个数
    money_start = 500
    big_blind_stake_money = 40
    big_blind_stake = 0
    print("Welcome to wzk's Texas Poker!")
    print("规则为无限制德州扑克，不过其中all in功能尚未测试可能有bug")
    print("遇到其他bug请告诉我，敬请体验~")
    while True:
        try:
            n = int(input("输入玩家人数  "))
            assert n > 1
            break
        except (ValueError, AssertionError):
            print("请输入大于1的整数！")
    for i in range(n):
        money.append(money_start)
        player_alive.append(i)
        player_card.append([])


def gameover(winner):
    for i in range(n):
        money[i] -= stake[i]
    global sign, big_blind_stake, lost_stake, big_stake  #,small_blind_stake
    time.sleep(1)
    print("本轮获胜的玩家:")
    for i in winner:
        print("玩家" + str(i + 1))
    print("恭喜！\n")
    calculate_money(winner)
    show_money()
    big_blind_stake = renew(big_blind_stake)
    lost_stake = 0
    big_stake = 0
    #small_blind_stake=renew(small_blind_stake)
    while True:
        over = input("本轮结束，输入a再来一轮，输入q退出  ")
        if over == "a":
            sign = 1
            break
        if over == "q":
            print("游戏结束，别忘了给wzk发红包哦")
            time.sleep(3)
            sign = 0
            break
        else:
            print("输入错误，请重新输入！")


def game():
    global sign, player_alive
    while sign == 1:  #每一轮游戏
        player_alive = []
        for i in range(n):
            player_alive.append(i)
            stake.append(0)

        show_money()
        get_hand_card()  #发底牌
        make_first_stake(big_blind_stake)  #,small_blind_stake)#下注
        if judge_win() != -1:
            gameover(judge_win())
            continue
        time.sleep(1)
        get_three_public_card()  #发三张公共牌
        make_stake()  #下注，判定胜负
        if judge_win() != -1:
            gameover(judge_win())
            continue
        time.sleep(1)
        get_public_card(4)  #发第四张公共牌
        make_stake()  #下注，判定胜负
        if judge_win() != -1:
            gameover(judge_win())
            continue
        time.sleep(1)
        get_public_card(5)  #发第五张公共牌
        make_stake()  #下注，判定胜负
        if judge_win() != -1:
            gameover(judge_win())
            continue
        winner = compare_card()
        gameover(winner)

def play():
    start()
    game()


if __name__ == '__main__':
    play()