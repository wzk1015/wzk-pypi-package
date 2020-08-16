from difflib import Differ
import time


def diff_compare(in_lines1, in_lines2):
    l1 = in_lines1.split("\n")
    l2 = in_lines2.split("\n")
    d = Differ()
    result = list(d.compare(l1, l2))
    result = "\n".join(result)
    return result


class ErrorFucker:
    def __init__(self, msg="You idiot! You've raised error!",
                 exps=None, raises=False, bonus=True):
        if isinstance(exps, Exception):
            self.exps = [exps]
        else:
            self.exps = exps
        self.msg = msg
        self.raises = raises
        self.bonus = bonus

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.msg)
        print(str(exc_type)[8:-2] + ":  " + str(exc_val))
        if self.raises:
            if self.bonus:
                print("I threw it out!")
        else:
            if self.bonus:
                print("Luckily I've handled this.")
            return True


class Separate:
    def __init__(self, title="", pad="-", center=True, length=30,
                 count=False, enter_print=True):
        self.title = title
        self.pad = pad
        self.center = center
        self.length = length
        self.do_count = count
        self.count = 0
        self.enter = enter_print

    def __enter__(self):
        if self.enter:
            self.count += 1
            content = self.title + str(self.count) if self.do_count else ""
            if self.center:
                print(content.center(self.length, self.pad))
            else:
                print(content.ljust(self.length, self.pad))
        return self

    def __exit__(self, *args):
        if not self.enter:
            self.count += 1
        content = self.title + (str(self.count) if self.do_count else "")
        if self.center:
            print(content.center(self.length, self.pad))
        else:
            print(content.ljust(self.length, self.pad))


class Clock:
    def __init__(self, prefix="", print_out=True):
        self.prefix = prefix
        self.time = None
        self.start = None
        self.print_out = print_out

    def begin(self):
        self.start = time.time()
        if self.print_out:
            print("begin timing".center(30, "-"))

    def end(self):
        self.time = time.time() - self.start

    def _check(self):
        if self.time is None:
            raise RuntimeError("clock referenced before end of timing")

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, *args):
        self.end()
        if self.print_out:
            print("end timing".center(30, "-"))
            print('%s clock time: %.4f seconds' % (self.prefix, self.time))

    def __str__(self):
        self._check()
        return str(self.time)

    def __call__(self):
        self._check()
        return self.time


if __name__ == '__main__':
    with ErrorFucker(raises=False) as ef1:
        d1 = int("f")

    with Separate("seperate zone", count=True) as s:
        print("ohhh")

    with s:
        with Clock("test") as c:
            time.sleep(2)
        print(c)
        with c:
            time.sleep(2)

    with ErrorFucker(raises=True) as ef2:
        d2 = int("d")

