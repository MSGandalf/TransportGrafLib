import copy, json, math
from random import randint
from MyTimeLib import Time, f_frequency, f_time
from RoutesLib import Route, FootCrossing, RouteContainer
from GrafLib import Station, Transport

SPEED_ON_FOOTS = 3


def radius(x, y, a=0, b=0): return math.sqrt((a - x) ** 2 + (b - y) ** 2)


def insec(p1, r1, p2, r2):
    x = p1[0]
    y = p1[1]
    R = r1
    a = p2[0]
    b = p2[1]
    S = r2
    d = math.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
    if d > (R + S) or d < (abs(R - S)):
        # print("Two circles have no intersection")
        return None,
    elif d == 0:
        # print("Two circles have same center!")
        return None,
    else:
        A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(R ** 2 - A ** 2)
        x2 = x + A * (a - x) / d
        y2 = y + A * (b - y) / d
        x3 = round(x2 - h * (b - y) / d, 2)
        y3 = round(y2 + h * (a - x) / d, 2)
        x4 = round(x2 + h * (b - y) / d, 2)
        y4 = round(y2 - h * (a - x) / d, 2)
        c1 = [x3, y3]
        c2 = [x4, y4]
        return c1, c2


class City:
    def __init__(self, name):
        self.stations = {}
        self.transports = {}
        self.name = name.lower()

    def add_station(self, station):
        if isinstance(station, Station):
            self.stations[station.name.lower()] = station

    def add_transport(self, transport):
        if isinstance(transport, Transport):
            self.transports[transport.name.lower()] = transport

    def auto_deploy_last(self):
        a = list(self.stations.keys())
        b = {}
        c = {}
        for i in self.stations:
            b[i] = self.make_routes_range(i)
        self.stations[a[0]].set_pos((0, 0))
        c[a[0]] = (0, 0)
        self.stations[a[1]].set_pos((b[a[1]][a[0]], 0))
        c[a[1]] = (b[a[1]][a[0]], 0)
        for s in a[2:]:
            p1, p2, p3, p4 = 0, 0, 0, 0
            p1 = randint(0, len(c) - 1)
            n = 1000
            while p2 == p1 and n > 0:
                n -= 1
                p2 = randint(0, len(c) - 1)
            n = 1000
            while p3 in (p1, p2) and n > 0:
                n -= 1
                p3 = randint(0, len(c) - 1)
            n = 1000
            while p4 in (p1, p2, p3) and n > 0:
                n -= 1
                p4 = randint(0, len(c) - 1)
            points = []
            points += list(insec(c[a[p1]], b[a[p1]][s], c[a[p2]], b[a[p2]][s]))
            points += list(insec(c[a[p1]], b[a[p1]][s], c[a[p3]], b[a[p3]][s]))
            points += list(insec(c[a[p1]], b[a[p1]][s], c[a[p4]], b[a[p3]][s]))
            points += list(insec(c[a[p2]], b[a[p2]][s], c[a[p3]], b[a[p3]][s]))
            points += list(insec(c[a[p2]], b[a[p2]][s], c[a[p4]], b[a[p4]][s]))
            points += list(insec(c[a[p3]], b[a[p3]][s], c[a[p4]], b[a[p4]][s]))
            for i in range(points.count(None)):
                points.remove(None)
            m = float('inf')
            for i in points:
                l = 0
                for j in c:
                    l += (radius(*i, *c[j]) - b[j][s]) ** 2
                if l < m:
                    m = l
                    k = i
            if m != float('inf'):
                self.stations[s].set_pos(k)
                c[s] = k
            else:
                self.stations[s].set_pos(
                    ((c[a[p1]][0] + c[a[p2]][0] + c[a[p3]][0]) / 3, (c[a[p1]][1] + c[a[p2]][1] + c[a[p3]][1]) / 3))
                c[s] = ((c[a[p1]][0] + c[a[p2]][0] + c[a[p3]][0]) / 3, (c[a[p1]][1] + c[a[p2]][1] + c[a[p3]][1]) / 3)

    def auto_deploy(self):
        a = list(self.stations.keys())
        b = {}
        c = {}
        for i in self.stations:
            b[i] = self.make_routes_range(i)
        self.stations[a[0]].set_pos((0, 0))
        c[a[0]] = (0, 0)
        self.stations[a[1]].set_pos((b[a[1]][a[0]], 0))
        c[a[1]] = (b[a[1]][a[0]], 0)
        for s in a[2:]:
            points = []
            for i in range(len(c)):
                for ii in range(len(c)):
                    points += list(insec(c[a[i]], b[a[i]][s], c[a[ii]], b[a[ii]][s]))
            for i in range(points.count(None)):
                points.remove(None)
            m = float('inf')
            for i in points:
                l = 0
                for j in c:
                    l += (radius(*i, *c[j]) - b[j][s]) ** 2
                if l < m:
                    m = l
                    k = i
            if m != float('inf'):
                self.stations[s].set_pos(k)
                c[s] = k
            else:
                self.stations[s].set_pos(0, b[s][a[0]])
                c[s] = (0, b[s][a[0]])

    def make_routes_range(self, station1):
        time_now = 0
        go = {}
        graf = {}
        for i in self.stations:
            graf[i] = float('inf')
        graf[station1] = 0
        check = station1
        while check:
            for r in self.stations[check].get_routes():
                if r.next_station not in graf:
                    continue
                c = r.time(time_now + graf[check]) * self.transports[r.transport].speed + graf[check]
                if graf[r.next_station] > c:
                    graf[r.next_station] = c

            for r in self.stations[check].get_foot_crossings():
                if r.next_station not in graf:
                    continue
                c = r.time * SPEED_ON_FOOTS + graf[check][0]

                if graf[r.next_station][0] > c:
                    graf[r.next_station][0] = c

            go[check] = graf[check]
            del graf[check]

            min = float('inf')
            check = ''
            for i in graf:
                if graf[i] < min:
                    min = graf[i]
                    check = i

        return go

    def make_route_last_last(self, station1, station2, time_now, weight_of_money=0, weight_of_time=1,
                             weight_of_time_in_foot_crossings=1):
        if isinstance(time_now, Time):
            time_now = time_now()
        go = {}
        graf = {}
        for i in self.stations:
            graf[i] = [float('inf'), [[None, 0, 0, ""]], 0, 0]
        graf[station1][0] = 0
        #    ^          ^        ^
        #   name       num, route to point = [(Transport,time),(...),(...)]
        check = station1
        graf[check][1][0][3] += station1
        while check:
            for r in self.stations[check].get_routes():
                if r.next_station not in graf:
                    continue
                c = r.time(time_now + graf[check][0]) * weight_of_time + graf[check][0]
                a = 0
                b = 0
                if r.transport != graf[check][1][-1][0]:
                    c += r.frequency(time_now + graf[check][0]) * weight_of_time + \
                         self.transports[r.transport].cost * weight_of_money
                    b = r.frequency(time_now + graf[check][0])
                    a = self.transports[r.transport].cost

                if graf[r.next_station][0] > c:
                    graf[r.next_station][0] = c
                    if a:
                        graf[r.next_station][1] = copy.deepcopy(graf[check][1]) + [
                            [r.transport, r.time(time_now + graf[check][0]) + b, 1,
                             graf[check][1][-1][3].split()[-1] + ' -> ' + r.next_station]]
                    else:
                        graf[r.next_station][1] = copy.deepcopy(graf[check][1])
                        graf[r.next_station][1][-1][1] += r.time(time_now + graf[check][0])
                        graf[r.next_station][1][-1][2] += 1
                        graf[r.next_station][1][-1][3] += ' -> ' + r.next_station
                    graf[r.next_station][2] = graf[check][2] + a
                    graf[r.next_station][3] = graf[check][3] + r.time(time_now + graf[check][0]) + b

            for r in self.stations[check].get_foot_crossings():
                if r.next_station not in graf:
                    continue
                c = r.time * weight_of_time_in_foot_crossings + graf[check][0]

                if graf[r.next_station][0] > c:
                    graf[r.next_station][0] = c
                    graf[r.next_station][1] = copy.deepcopy(graf[check][1]) + [
                        [None, r.time, 1, graf[check][1][-1][3].split()[-1] + ' -> ' + r.next_station]]
                    graf[r.next_station][2] = graf[check][2]
                    graf[r.next_station][3] = graf[check][3] + r.time

            go[check] = graf[check]
            del graf[check]

            min = float('inf')
            check = ''
            for i in graf:
                if graf[i][0] < min:
                    min = graf[i][0]
                    check = i

        go[station2][1] = copy.deepcopy(go[station2][1][1:])
        return go[station2]

    def make_route_last(self, station1, station2, time_now, weight_of_time=1, weight_of_money=0,
                        weight_of_time_in_foot_crossings=1):
        if isinstance(time_now, Time):
            time_now = time_now()
        go = {}
        graf = {}
        for i in self.stations:
            graf[i] = []
        #     name      [0]value, [1]transport, [2]time_road, [3]stations, [4]txt_stations, [5]time_all, [6]cost
        graf[station1] = [[0, None, 0, 0, [], 0, 0]]
        #    ^          ^        ^
        #     name      [0]value, [1]transport, [2]time_road, [3]stations, [4]txt_stations, [5]time_all, [6]cost
        check = station1
        while check:
            for r in self.stations[check].get_routes():
                if r.next_station not in graf:
                    continue
                m = float('inf')
                a = -1
                b = -1
                c = -1
                t = -1
                for i in range(len(graf[check])):
                    if graf[check][i][0] + (weight_of_time * r.frequency(time_now + graf[check][i][0])) * (
                            graf[check][i][1] != r.transport) + \
                            (weight_of_money * self.transports[r.transport].cost) * (
                            graf[check][i][1] != r.transport or graf[check][i][1] is None) < m:
                        m = graf[check][i][0] + (weight_of_time * r.frequency(time_now + graf[check][i][0])) * (
                                graf[check][i][1] != r.transport) + \
                            (weight_of_money * self.transports[r.transport].cost) * (
                                    graf[check][i][1] != r.transport or graf[check][i][1] is None)
                        a = i
                        t = graf[check][i][5]
                        b = r.frequency(time_now + graf[check][i][0]) * (graf[check][i][1] != r.transport)
                        c = self.transports[r.transport].cost * (
                                graf[check][i][1] != r.transport or graf[check][i][1] is None)
                k = r.time(time_now + t + b) * weight_of_time + m
                for g in graf[r.next_station]:
                    if g[1] == r.transport:
                        if g[0] > k:
                            g[0] = k
                            g[2] = graf[check][a][2] + b + r.time(time_now + t + b)
                            g[3] = graf[check][a][3] + 1
                            g[4] = graf[check][a][4] + [r.next_station]
                            g[5] = graf[check][a][5] + b + r.time(time_now + t + b)
                            g[6] = graf[check][a][6] + c
                        break
                else:
                    if r.transport == graf[check][a][1]:
                        graf[r.next_station].append([k,
                                                     r.transport,
                                                     graf[check][a][2] + b + r.time(time_now + t + b),
                                                     graf[check][a][3] + 1,
                                                     graf[check][a][4] + [r.next_station],
                                                     graf[check][a][5] + b + r.time(time_now + t + b),
                                                     graf[check][a][6] + c
                                                     ])
                    else:
                        #   name  [0]value, [1]transport, [2]time_road, [3]stations, [4]txt_stations, [5]time_all, [6]cost
                        graf[r.next_station].append([k,
                                                     r.transport,
                                                     graf[check][a][2] + b + r.time(time_now + t + b),
                                                     1,
                                                     graf[check][a][4] + [[graf[check][a][3], r.transport], check,
                                                                          r.next_station],
                                                     graf[check][a][5] + b + r.time(time_now + t + b),
                                                     graf[check][a][6] + c
                                                     ])

            for r in self.stations[check].get_foot_crossings():
                if r.next_station not in graf:
                    continue
                m = float('inf')
                a = -1
                b = -1
                c = -1
                t = -1
                for i in range(len(graf[check])):
                    if graf[check][i][0] < m:
                        m = graf[check][i][0]
                        a = i
                        t = graf[check][i][5]
                        b = 0
                        c = 0

                k = r.time(time_now + t) * weight_of_time_in_foot_crossings + m
                for g in graf[r.next_station]:
                    if g[1] == r.transport:
                        if g[0] > k:
                            g[0] = k
                            g[2] = graf[check][a][2] + b + r.time(time_now + t + b)
                            g[3] = graf[check][a][3] + 1
                            g[4] = graf[check][a][4] + [r.next_station]
                            g[5] = graf[check][a][5] + b + r.time(time_now + t + b)
                            g[6] = graf[check][a][6] + c
                        break
                else:
                    if r.transport == graf[check][a][1]:
                        graf[r.next_station].append([k,
                                                     None,
                                                     graf[check][a][2] + b + r.time(time_now + t + b),
                                                     graf[check][a][3] + 1,
                                                     graf[check][a][4] + [r.next_station],
                                                     graf[check][a][5] + b + r.time(time_now + t + b),
                                                     graf[check][a][6] + c
                                                     ])
                    else:
                        #   name  [0]value, [1]transport, [2]time_road, [3]stations, [4]txt_stations, [5]time_all, [6]cost
                        graf[r.next_station].append([k,
                                                     None,
                                                     graf[check][a][2] + b + r.time(time_now + t + b),
                                                     1,
                                                     graf[check][a][4] + [[graf[check][a][3], None], check,
                                                                          r.next_station],
                                                     graf[check][a][5] + b + r.time(time_now + t + b),
                                                     graf[check][a][6] + c
                                                     ])

            go[check] = graf[check]
            del graf[check]

            m = float('inf')
            check = ''
            for i in graf:
                if graf[i] and min(graf[i])[0] < m:
                    m = min(graf[i])[0]
                    check = i

        a = min(go[station2])
        last = -1
        n = 0
        for c, i in enumerate(a[4]):
            if isinstance(i, list):
                if last != -1:
                    a[4][last][0] = n
                n = -1
                last = c
            else:
                n += 1
        if last != -1:
            a[4][last][0] = n
        return min(go[station2]), min(go[station2])[4]

    def make_route(self, station1, station2, time_now, weight_of_time=1, weight_of_money=0,
                   weight_of_time_in_foot_crossings=1):
        if isinstance(time_now, Time):
            time_now = time_now()
        graf = {}
        for i in self.stations:
            graf[i] = RouteContainer(self.transports, time_now, station1, weight_of_money, weight_of_time,
                                     weight_of_time_in_foot_crossings, bad=True)
        graf[station1] = RouteContainer(self.transports, time_now, station1, weight_of_money, weight_of_time,
                                        weight_of_time_in_foot_crossings, bad=False)
        check_all = []
        for i in self.stations[station1].routes:
            check_all.append(i.transport)
        while check_all:
            check = check_all[0]
            # Using here Dijkstra's algorithm, for finding routes at one of transport
            gg = {}
            g = {}
            for i in graf:
                g[i] = graf[i].copy()
            c = ''
            m = float('inf')
            for i in g:
                tt = float('inf')
                for ii in self.stations[i].get_routes():
                    if ii.transport == check:
                        if ii.frequency(time_now) < tt:
                            tt = ii.frequency(time_now)
                if g[i]() + tt <= m:
                    m = g[i]()
                    c = i
            while c:
                for i in self.stations[c].get_routes():
                    if i.next_station in g:
                        if i.transport == check:
                            k = 0
                            if g[c].route and g[c].route[-1][0] is None:
                                k += i.frequency(time_now)
                            k += i.time(time_now + k)
                            if g[c] + k < g[i.next_station]():
                                g[i.next_station] = g[c].copy()
                                g[i.next_station].add(i)
                for i in self.stations[c].get_foot_crossings():
                    if i.next_station in g:
                        k = i.time
                        if g[c] + k < g[i.next_station]:
                            g[i.next_station] = g[c].copy()
                            g[i.next_station].add(i)

                gg[c] = g[c]
                del g[c]
                c = ''
                m = float('inf')
                for i in g:
                    tt = float('inf')
                    for ii in self.stations[i].get_routes():
                        if ii.transport == check:
                            if ii.frequency(time_now) < tt:
                                tt = ii.frequency(time_now)
                    if g[i]() + tt <= m:
                        m = g[i]()
                        c = i

            check_all.pop(0)
            for i in graf:
                if graf[i] > gg[i]:
                    graf[i] = gg[i].copy()
                    for a in self.stations[i].get_routes():
                        if not a.transport in check_all:
                            check_all.append(a.transport)

        return graf[station2], graf

    def get_all_routes(self, station, time_now, weight_of_time=1, weight_of_money=0,
                       weight_of_time_in_foot_crossings=1):
        return self.make_route(station, station, time_now, weight_of_money, weight_of_time,
                               weight_of_time_in_foot_crossings)

    def __repr__(self):
        a = "\n\t|"
        return f'''{self.name}: {len(self.stations)} stations, {len(self.transports)} transports.
    |-----------------------------------------------------------------------------------
    |stations:\n\t|{a.join(map(str, self.stations.values()))}
    |-----------------------------------------------------------------------------------
    |transports:\n\t|{a.join(map(str, self.transports.values()))}'''

    def __str__(self):
        return self.__repr__()

    def save(self, name, password=0):
        a = {"name": self.name,
             "stations": list(map(Station.save, self.stations.values())),
             "transports": list(map(Transport.save, self.transports.values())),
             "password": password}

        with open(f"Data/{name}", "w", encoding='utf-8') as w:
            w.write(str(a).replace("'", '"').replace('None', '"None"'))

        return a

    def load(self, name):
        a = json.load(open(f"Data/{name}", encoding='utf-8'))
        self.name = a['name'].lower()
        self.transports = {}
        for i in a['transports']:
            if i['mode'] == "None":
                i['mode'] = None
            if 'speed' not in i.keys():
                i['speed'] = 10
            self.transports[i['name'].lower()] = Transport(i['name'].lower(), i['cost'], i['speed'], i['mode'])
        self.stations = {}
        for i in a['stations']:
            self.stations[i['name'].lower()] = Station(i['name'], i['pos'])
            self.stations[i['name'].lower()].load(i['routes'], i['foot_crossings'])
        return int(a['password'])
