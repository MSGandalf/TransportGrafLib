import copy, json
from MyTimeLib import Time, f_frequency, f_time


class Route:
    def __init__(self, time, next_station, frequency, transport):
        self.n_frequency = frequency
        self.next_station = next_station.lower()
        self.n_time = time
        self.transport = transport.lower()

    def frequency(self, time):
        return f_frequency(self.n_frequency, time)

    def time(self, time):
        return f_time(self.n_time, time)

    def __call__(self):
        return self.n_frequency, self.next_station, self.n_time, self.transport

    def __str__(self):
        return f"[{self.next_station}, {self.transport}]"

    def __repr__(self):
        return self.__str__()

    def save(self):
        return {"next_station": self.next_station, "n_frequency": self.n_frequency,
                "transport": self.transport, "n_time": self.n_time}


class FootCrossing:
    def __init__(self, time, next_station):
        self.time = time
        self.next_station = next_station.lower()

    def __str__(self):
        return f"[{self.next_station}, {self.time}s]"

    def __repr__(self):
        return self.__str__()

    def save(self):
        return {"time": self.time, "next_station": self.next_station}


class RouteContainer:
    def __init__(self, transports, timenow, station, weight_of_money, weight_of_time,
                 weight_of_time_in_foot_crossings, bad=False):
        self.bad = bad
        self.transports = transports
        self.timenow = timenow
        self.cost = 0
        self.time = 0
        self.score = 0
        self.route = []
        self.last = station
        self.time_on_foot = 0
        self.weight_of_time_in_foot_crossings = weight_of_time_in_foot_crossings
        self.weight_of_money = weight_of_money
        self.weight_of_time = weight_of_time

    def add(self, route):
        if isinstance(route, Route):
            if self.route and route.transport == self.route[-1][0]:
                self.route[-1][1].append(route.next_station)
                a = 0
            else:
                self.cost += self.transports[route.transport].cost
                self.route.append([route.transport, [self.last, route.next_station]])
                a = route.frequency(self.timenow)
            self.last = route.next_station
            self.time += route.time(self.timenow + a) + a
            self.timenow += route.time(self.timenow + a) + a
        elif isinstance(route, FootCrossing):
            if self.route and None == self.route[-1][0]:
                self.route[-1][1].append(route.next_station)
            else:
                self.route.append([None, [self.last, route.next_station]])
            self.last = route.next_station
            self.time += route.time(self.timenow)
            self.timenow += route.time(self.timenow)

    def copy(self):
        a = RouteContainer(self.transports, self.timenow, self.last, self.weight_of_money, self.weight_of_time, self.weight_of_time_in_foot_crossings, self.bad)
        a.route = copy.deepcopy(self.route)
        a.cost = self.cost
        a.time = self.time
        a.last = self.last
        a.time_on_foot = self.time_on_foot
        return a

    def __add__(self, other):
        return other + self()

    def __call__(self):
        if self.bad:
            return float('inf')
        return self.cost * self.weight_of_money + self.time * self.weight_of_time + self.time_on_foot * self.weight_of_time_in_foot_crossings

    def __str__(self):
        return f"{self.__class__.__name__}({self.route}, {self.time}, {self.cost}, {'bad' if self.bad else ''})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other() == self():
            return True
        return False

    def __lt__(self, other):
        if other() > self():
            return True
        return False

    def __le__(self, other):
        if other() >= self():
            return True
        return False

    def __ge__(self, other):
        if other() <= self():
            return True
        return False

    def __gt__(self, other):
        if other() < self():
            return True
        return False

    def __ne__(self, other):
        if other() != self():
            return True
        return False