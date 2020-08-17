from wzk.autograd.functional import *


class Thing:
    def __init__(self, v, grad_fn=None, requires_grad=True):
        self.v = float(v)
        if requires_grad:
            self.grad = Thing(0, requires_grad=False)
            self.grad_fn = grad_fn
        self.r_grad = requires_grad

    def backward(self):
        assert self.r_grad and self.grad_fn
        self.grad_fn.backward(1)

    def bw(self):
        if self.r_grad and self.grad_fn:
            self.grad_fn.backward(self.grad)

    def update(self, lr):
        self.v -= self.grad * lr

    def zero_grad(self):
        self.grad = 0

    def requires_grad(self):
        return self.r_grad

    def requires_grad_(self, boolean):
        self.r_grad = boolean
        if not boolean:
            self.grad_fn = None

    def __add__(self, other):
        return thing(self.v + float(other), grad_fn=AddBackward(self, other))

    def __sub__(self, other):
        return thing(self.v - float(other), grad_fn=SubBackward(self, other))

    def __mul__(self, other):
        return thing(self.v * float(other), grad_fn=MulBackward(self, other))

    def __truediv__(self, other):
        return thing(self.v / float(other), grad_fn=DivBackward(self, other))

    def __pow__(self, power, modulo=None):
        return thing(self.v ** float(power), grad_fn=PowBackward(self, power))

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self + -1 * other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return thing(float(other) / self.v, grad_fn=DivBackward(other, self))

    def __rpow__(self, other):
        return thing(float(other) ** self.v, grad_fn=PowBackward(other, self))

    def __repr__(self):
        num = "%.2f" % self.v if int(self.v) != self.v else str(int(self.v))
        if not self.grad_fn:
            return "Thing(%s)" % num
        return "Thing(%s, grad_fn=%s)" % (num, self.grad_fn)

    def __int__(self):
        return int(self.v)

    def __float__(self):
        return float(self.v)

    def __le__(self, other):
        return self.v <= float(other)

    def __lt__(self, other):
        return self.v < float(other)

    def __ge__(self, other):
        return self.v >= float(other)

    def __gt__(self, other):
        return self.v > float(other)

    def __eq__(self, other):
        return self.v == float(other)

    def __ne__(self, other):
        return self.v != float(other)

    def __neg__(self):
        return -1 * self


def thing(value, grad_fn=None, requires_grad=True):
    return Thing(value, grad_fn, requires_grad)


if __name__ == '__main__':
    a = thing(2)
    b = thing(3)
    c = a + leaky_relu(b)
    d = thing(5) # a + a*b
    e = tanh(d) # (a + a*b) * (a*b) = a^2(b + b^2)
    f = relu(c) + sin(e)
    g = log(f)

    #print(a.v, b.v, c.v, d.v, e.v, f.v)
    g.backward()
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)