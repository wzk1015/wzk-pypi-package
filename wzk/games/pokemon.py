import random

type2index = {
    "water"   : 0,
    "fire"    : 1,
    "grass"   : 2,
    "rock"    : 3,
    "electric": 4,
    "fly"     : 5,
    "normal"  : 6,
    "steel"   : 7
}
attack_table = {
    "water"   : ["fire", "rock"],
    "fire"    : ["grass", "steel"],
    "grass"   : ["water", "rock"],
    "rock"    : ["fire", "fly"],
    "electric": ["water", "fly"],
    "fly"     : ["grass"],
}
num_types = len(type2index.keys())


class Types:
    table = [[1 for i in range(num_types)] for j in range(num_types)]
    for attacker in attack_table.keys():
        for defender in attack_table[attacker]:
            table[type2index[attacker]][type2index[defender]] = 2
            table[type2index[defender]][type2index[attacker]] = 0.5

    @staticmethod
    def judge_power(type1, type2):
        assert isinstance(type1, str) and isinstance(type2, list)
        ans = 1
        for type in type2:
            times = Types.table[type2index[type1]][type2index[type]]
            if times == 2:
                print("great performance!")
            elif times == 0.5:
                print("bad performance..")
        return ans


class Pokemon:
    pid = 0
    pokemon_dict = {}

    def __init__(self, name, type, skills=None, level=5, **kwargs):
        self.name = name
        assert isinstance(level, int)
        self.level = level
        self.id = Pokemon.pid
        Pokemon.pokemon_dict[self.id] = self
        Pokemon.pid += 1

        self.HP = kwargs["HP"] if "HP" in kwargs.keys() else 10
        self.speed = kwargs["speed"] if "speed" in kwargs.keys() else 10
        self.attack = kwargs["attack"] if "attack" in kwargs.keys() else 10
        self.defense = kwargs["defense"] if "defense" in kwargs.keys() else 10

        self.skills = [None for i in range(4)]
        if skills:
            assert isinstance(skills, list)
            assert len(skills) <= 4
            for i in range(len(skills)):
                self.skills[i] = skills[i]

        assert isinstance(type, str) or isinstance(type, list)
        if isinstance(type, str):
            self.type = [type]
        else:
            self.type = type

        self.current_HP = self.HP

    def use_skill(self, index, enemy):
        assert isinstance(self.skills[index], Skill)
        self.skills[index].run(self, enemy)

    def add_skill(self, skill):
        assert isinstance(skill, Skill)
        self.skills.append(skill)

    def get_attacked(self, attacker, amount):
        self.current_HP -= amount/self.defense
        print("{} attacks {}! amount:{}".format(attacker, self, amount/self.defense))

    def help(self):
        for skill in self.skills:
            if isinstance(skill, Skill):
                print("1: {}  type:{}, power:{}, hit_rate:{}".format(
                    skill.name.ljust(10), skill.type, skill.power, skill.hit_rate))

    def show_infos(self, enemy):
        print("{}'s turn".format(self))
        print("Enemy's HP: {}".format(enemy.current_HP))
        print("Your HP: {}".format(self.current_HP))
        print("Your skills:")
        for i in range(4):
            if self.skills[i]:
                print("--{}:{}".format(i + 1, self.skills[i]))

    def make_move(self, enemy, repeat=False):
        if not repeat:
            self.show_infos(enemy)
        choice = input("number for using skill, 'skillsinfo' for info. Make a move:\n")
        if choice in ["1", "2", "3", "4"]:
            self.use_skill(int(choice) - 1, enemy)
            return
        elif choice == "skillsinfo":
            self.help()
        else:
            print("wrong command")
        self.make_move(enemy, repeat=True)

    def __str__(self):
        return self.name


class Skill:
    def __init__(self, name, type="normal", hit_rate=1, is_attack=True, power=0):
        self.name = name
        self.type = type
        self.attack = is_attack
        self.power = power
        self.hit_rate = hit_rate

    def run(self, user: Pokemon, enemy: Pokemon):
        assert isinstance(user, Pokemon) and isinstance(enemy, Pokemon)
        if self.attack:
            if random.random() <= self.hit_rate:
                enemy.get_attacked(user,
                                   self.power*Types.judge_power(self.type, enemy.type)*user.attack/100)

    def __str__(self):
        return self.name


def play():
    print("welcome to wzk's pokemon! this is a simple demo.\n"
          "you can easily make your MOD by modifying play() in pokemon.py")
    thunderbolt = Skill("thunderbolt", type="electric", power=80)
    pikuchu = Pokemon("pikachu", type="electric", skills=[thunderbolt],
                      level=20, attack=50, defense=50, speed=100, HP=50)
    jump = Skill("jump", power=0)
    fishking = Pokemon("fishking", type="water", skills=[jump], HP=20)

    while True:
        pikuchu.make_move(fishking)
        if fishking.current_HP < 0:
            print("pikachu win!")
            break
        print("-"*20)
        fishking.make_move(pikuchu)
        if pikuchu.current_HP < 0:
            print("that's impossible! how can you defeat pikuchu with fishking?")
            raise Exception
        print("-"*20)


if __name__ == '__main__':
    play()