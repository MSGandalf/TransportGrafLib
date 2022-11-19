MINUTES_IN_DAY = 1440


def f_frequency(t, time):
    if t[0] == 1:
        return t[1]
    if t[0] == 2:
        if 7 <= time.h <= 9 or 17 <= time.h <= 19:
            if len(t) > 1:
                return t[2]
            else:
                return 2 * t[1]
        return t[1]
    if t[0] == 3:
        if time() < t[2]:
            return t[2] - time()
        if time() > t[3]:
            return MINUTES_IN_DAY - time() + t[2] - time()
        return (time() - t[2]) % t[1]


def f_time(t, time):
    if t[0] == 1:
        return t[1]
    if t[0] == 2:
        if 7 <= time.h() <= 9 or 17 <= time.h() <= 19:
            if len(t) > 1:
                return t[2]
            else:
                return 2 * t[1]
        return t[1]


class Time:
    def __init__(self, a=None, h=None, m=None):
        if a is not None:
            self.n_h = a // 60 % 24
            self.n_m = a % 60
            self.n_time = self.n_h * 60 + self.n_m
        elif h is not None and m is not None:
            self.n_h = (h + m // 60) % 24
            self.n_m = m % 60
            self.n_time = self.n_h * 60 + self.n_m
        else:
            self.n_h = 0
            self.n_m = 0
            self.n_time = 0

    def __call__(self):
        return self.n_time

    def h(self):
        return self.n_h

    def m(self):
        return self.n_m

    def __add__(self, other):
        if isinstance(other, int):
            self.n_time += other
            self.n_h = self.n_time // 60 % 24
            self.n_m = self.n_time % 60
            self.n_time = self.n_h * 60 + self.n_m

    def __sub__(self, other):
        if isinstance(other, int):
            self.__add__(-other)
