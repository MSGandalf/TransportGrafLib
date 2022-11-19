import copy, json
from MyTimeLib import Time, f_frequency, f_time
from RoutesLib import Route, FootCrossing, RouteContainer


class Station:
    def __init__(self, name, pos=None, *routes):
        self.routes = []
        self.foot_crossings = []
        self.name = name.lower()
        for route in routes:
            if isinstance(route, Route):
                self.routes.append(route)
        if pos is None:
            self.pos = [-1, -1]
        else:
            self.pos = list(pos[:2])

    def get_routes(self):
        return list(self.routes)

    def get_foot_crossings(self):
        return list(self.foot_crossings)

    def add_route(self, route):
        if isinstance(route, Route):
            self.routes.append(route)

    def add_foot_crossing(self, foot_crossing):
        if isinstance(foot_crossing, FootCrossing):
            self.foot_crossings.append(foot_crossing)

    def __str__(self):
        return f'{self.__class__.__name__}({self.name}, {self.pos}: Routes ({" ".join(map(str, self.routes))}), Foot Crosses ({" ".join(map(str, self.foot_crossings))}))'

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        if isinstance(item, int) and 0 <= item <= 1:
            return self.pos[item]

    def set_pos(self, new_pos):
        self.pos = list(new_pos)

    def rename(self, new_name):
        self.name = new_name.lower()

    def save(self):
        return {"name": self.name,
                "pos": self.pos,
                "routes": list(map(Route.save, self.routes)),
                "foot_crossings": list(map(FootCrossing.save, self.foot_crossings))}

    def load(self, routes, foot_crossings):
        self.routes = []
        for i in routes:
            self.routes.append(Route(i['n_time'], i['next_station'].lower(), i['n_frequency'], i['transport'].lower()))
        for i in foot_crossings:
            self.foot_crossings.append(FootCrossing(i['time'], i['next_station'].lower()))


class Transport:
    def __init__(self, name, cost, speed=10, mode=None):
        self.name = name.lower()
        self.cost = cost
        self.mode = mode
        self.speed = speed

    def __call__(self):
        return self.cost

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {self.cost}₽, {self.mode})"  # ₽={chr(8381)}

    def __repr__(self):
        return self.__str__()

    def save(self):
        return {"name": self.name, "cost": self.cost, "speed": self.speed, "mode": self.mode}
