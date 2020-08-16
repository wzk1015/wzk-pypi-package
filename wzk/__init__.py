from . import parser

from .games.flight_game import play as flight_game
from .games.game2048 import play as game2048
from .games.mine_sweeper import play as mine_sweep
from .games.texas_poker import play as texas_poker
from .games.pokemon import play as pokemon
from .games.mahjong import play as mahjong
from .vocab.vocab import lookup
from .vocab.vocab import translate
from .utils import *
from .ds import *
from .parser import *

from time import ctime


print("Welcome to wzk's library!")


def greeting():
    print("It's", ctime(), "Greeting from wzk!")