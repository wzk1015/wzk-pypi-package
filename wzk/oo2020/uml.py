from random import choice
from wzk.oo2020.dataMake import dataMake


def hw13_generator(mode=None, isStrong=None):
    if mode is None:
        mode = choice(["normal", "strong"])
    if isStrong is None:
        isStrong = choice([True, False])
    return dataMake(mode=mode, isStrong=isStrong)


if __name__ == '__main__':
    print(hw13_generator())