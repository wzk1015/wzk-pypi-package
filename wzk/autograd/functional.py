import math
#from wzk.autograd.thing import thing


def sigmoid(x):
    from wzk.autograd.thing import thing
    return thing(1 / (1 + math.exp(-x)), grad_fn=SigmoidBackward(x))


def relu(x):
    from wzk.autograd.thing import thing
    return thing(x if x > 0 else 0, grad_fn=ReLUBackward(x))


def leaky_relu(x, k=0.01):
    from wzk.autograd.thing import thing
    return thing(x if x > 0 else k * x, grad_fn=LeakyReLUBackward(x, k))


def tanh(x):
    from wzk.autograd.thing import thing
    return thing((math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x)),
                 grad_fn=TanhBackward(x))


def sin(x):
    from wzk.autograd.thing import thing
    return thing(math.sin(x), grad_fn=SinBackward(x))


def cos(x):
    from wzk.autograd.thing import thing
    return thing(math.cos(x), grad_fn=CosBackward(x))


def log(x):
    from wzk.autograd.thing import thing
    return thing(math.log(x), grad_fn=LogBackward(x))


class GradientFunction:
    def __init__(self, o1, o2):
        self.o1 = o1
        self.o2 = o2

    def backward(self, result_g):
        raise NotImplementedError

    def thing_bw(self):
        if hasattr(self.o1, "r_grad"):
            self.o1.grad.requires_grad_(False)
            self.o1.bw()
        if hasattr(self.o2, "r_grad"):
            self.o2.grad.requires_grad_(False)
            self.o2.bw()


class AddBackward(GradientFunction):
    def __init__(self, o1, o2):
        super().__init__(o1, o2)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += result_g
        if do_grad(self.o2):
            self.o2.grad += result_g
        self.thing_bw()

    def __repr__(self):
        #print("I am called", self.o1, self.o2)
        return "AddBackward"


class SubBackward(GradientFunction):
    def __init__(self, o1, o2):
        super().__init__(o1, o2)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += result_g
        if do_grad(self.o2):
            self.o2.grad -= result_g
        self.thing_bw()

    def __repr__(self):
        return "SubBackward"


class MulBackward(GradientFunction):
    def __init__(self, o1, o2):
        super().__init__(o1, o2)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += float(self.o2) * result_g
        if do_grad(self.o2):
            self.o2.grad += float(self.o1) * result_g
        self.thing_bw()

    def __repr__(self):
        return "MulBackward"


class DivBackward(GradientFunction):
    def __init__(self, o1, o2):
        super().__init__(o1, o2)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += 1 / float(self.o2) * result_g
        if do_grad(self.o2):
            self.o2.grad += float(self.o1) / float(self.o1) ** 2 * result_g
        self.thing_bw()

    def __repr__(self):
        return "DivBackward"


class PowBackward(GradientFunction):
    def __init__(self, o1, o2):
        super().__init__(o1, o2)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += result_g * float(self.o2) * \
                            float(self.o1) ** (float(self.o2) - 1)
        if do_grad(self.o2):
            self.o2.grad += float(self.o1) ** float(self.o2) \
                            * log(float(self.o1)) * result_g
        self.thing_bw()

    def __repr__(self):
        return "PowBackward"


class SinBackward(GradientFunction):
    def __init__(self, o):
        super().__init__(o, None)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += result_g * cos(self.o1)
        self.thing_bw()

    def __repr__(self):
        return "SinBackward"


class CosBackward(GradientFunction):
    def __init__(self, o):
        super().__init__(o, None)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += - result_g * sin(self.o1)
        self.thing_bw()

    def __repr__(self):
        return "CosBackward"


class LogBackward(GradientFunction):
    def __init__(self, o):
        super().__init__(o, None)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += 1 / self.o1 * result_g
        self.thing_bw()

    def __repr__(self):
        return "LogBackward"


class SigmoidBackward(GradientFunction):
    def __init__(self, o):
        super().__init__(o, None)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += sigmoid(self.o1) * (1 - sigmoid(self.o1))
        self.thing_bw()

    def __repr__(self):
        return "SigmoidBackward"


class TanhBackward(GradientFunction):
    def __init__(self, o):
        super().__init__(o, None)

    def backward(self, result_g):
        if do_grad(self.o1):
            self.o1.grad += 1 - tanh(self.o1) ** 2
        self.thing_bw()

    def __repr__(self):
        return "TanhBackward"


class LeakyReLUBackward(GradientFunction):
    def __init__(self, o, k):
        super().__init__(o, None)
        self.k = k

    def backward(self, result_g):
        if do_grad(self.o1):
            if self.o1 > 0:
                self.o1.grad += 1
            else:
                self.o1.grad += self.k
        self.thing_bw()

    def __repr__(self):
        return "LeakyReLUBackward"


class ReLUBackward(LeakyReLUBackward):
    def __init__(self, o):
        super().__init__(o, 0)

    def __repr__(self):
        return "ReLUBackward"


def do_grad(oi):
    return hasattr(oi, "r_grad") and oi.r_grad