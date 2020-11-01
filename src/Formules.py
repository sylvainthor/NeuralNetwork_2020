#!/usr/bin/env python
import math


class Formules:

    def __init__(self):
        pass

    def sigmoide(self, x):
        return 1 / (1 + math.exp(-x))

    def softmax(self, x):
        return math.exp(x) / (1 + math.exp(x))

    def tanh(self, x):
        return math.tanh(x)


# test :
def main():
    f = Formules()
    print(f.sigmoide(5.0))


if __name__ == '__main__':
    main()