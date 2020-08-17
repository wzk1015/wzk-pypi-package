class L(list):
    def __init__(self, *args):
        list.__init__([])
        if len(args) == 1 and isinstance(args[0], list):
            self.extend(args[0])
        else:
            self.extend(list(args))


class S(str):
    def __init__(self, s=""):
        str.__init__(s)


class D(dict):
    def __init__(self, dct=None):
        if dct is None:
            dct = {}
        super().__init__(dct)
        self._inv = {dct[key]: key for key in dct.keys()}

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        try:
            self._inv[value] = key
        except TypeError:
            pass

    def __delitem__(self, key):
        v = self[key]
        self._inv.__delitem__(v)
        super().__delitem__(key)

    def inv(self):
         return DD(self._inv)


class DD(D):
    def __init__(self, dct=None):
        super().__init__({})
        if dct is not None:
            for k, v in dct.items():
                self[k] = v

    def __setitem__(self, key, value):
        try:
            if key is not str:
                raise AttributeError
            self.__getattribute__(key)
            raise TypeError("cannot set built-in name attribute " + key)
        except AttributeError:
            super().__setitem__(key, value)

    def __getattribute__(self, item):
        if item == "_keys":
            return super().keys()
        if item in self._keys:
            return super().__getitem__(item)
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key != "_inv":
            self.__setitem__(key, value)
        else:
            super().__setattr__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)



class T(tuple):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            tuple.__init__(args[0])
        else:
            tuple.__init__(tuple(args))


class Set(set):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], set):
            set.__init__(args[0])
        else:
            set.__init__(set(args))


class N:
    def __init__(self, i, lower_bound=None, upper_bound=None, loop=False,
                 integer=False):
        self.loop = loop
        if upper_bound is not None and lower_bound is not None:
            upper_bound, lower_bound = int(upper_bound), int(lower_bound)
            assert upper_bound > lower_bound
            self.range = upper_bound - lower_bound
        self.ub = upper_bound
        self.lb = lower_bound
        self.value = i
        self.integer = integer

    def _bound_check(self, value):
        if not self.loop and (self.ub is not None and value > self.ub) \
                or (self.lb is not None and value < self.lb):
            raise OverflowError("number " + str(self) + " overflow its range ["
                                + str(self.lb) + ", " + str(self.ub) + "]")
        if self.integer and not isinstance(value, int):
            raise TypeError("force-integer number cannot be " + str(value))
        if hasattr(self, 'range'):
            return (value - self.lb) % (self.ub - self.lb) + self.lb
        return N(value)

    def __add__(self, other):
        return self._bound_check(self.value + float(other))

    def __sub__(self, other):
        return self._bound_check(self.value - float(other))

    def __mul__(self, other):
        return self._bound_check(self.value*float(other))

    def __truediv__(self, other):
        return self._bound_check(self.value/float(other))

    def __repr__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __le__(self, other):
        return self.value <= float(other)

    def __lt__(self, other):
        return self.value < float(other)

    def __ge__(self, other):
        return self.value >= float(other)

    def __gt__(self, other):
        return self.value > float(other)

    def __eq__(self, other):
        return self.value == float(other)

    def __ne__(self, other):
        return self.value != float(other)

    def __pow__(self, power, modulo=None):
        return self.value ** float(power)

    def __mod__(self, other):
        return self.value%float(other)

    def set(self, v):
        self.value = self._bound_check(v)


if __name__ == '__main__':
    s = S("wzk is really good")
    s.remove("lo ")
    print(s)
    b = N(4, upper_bound=8, lower_bound=3, loop=True)
    print(b + 12)
    a = DD({"good": "kk"})
    a.bad = "nyima"
    print(a.good)
    print(a["bad"])
    print(a.inv()["nyima"])