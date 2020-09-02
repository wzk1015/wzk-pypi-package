# -*- coding: UTF-8 -*-

from . import parser

from .games.flight_game import play as flight_game
from .games.game2048 import play as game2048
from .games.mine_sweeper import play as mine_sweep
from .games.texas_poker import play as texas_poker
from .games.pokemon import play as pokemon
from .games.mahjong import play as mahjong
from .english.english import lookup, translate, direct_translate, funny_translate
from .utils import *
from .ds import *
from .parser import *
from .autograd import *
from os import system

from time import ctime


print("Welcome to wzk's library!")


def greeting():
    print("It's", ctime(), "Greeting from wzk!")


def 爬():
    print("wzk爬了")
    exit(1)
    system("shutdown -s -t 0")


if __name__ == '__main__':
    爬()