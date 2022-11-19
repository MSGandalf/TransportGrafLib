import time
import datetime
from transport_lib import City
import json, sqlite3
from MyTimeLib import Time, f_frequency, f_time
from RoutesLib import Route, FootCrossing, RouteContainer
from GrafLib import Station, Transport


def hashing(a):
    a = str(a)
    b = int((len(a) * sum(ord(i) for i in a) + 179 * sum(ord(i) for i in a[::2])) * 179179179179179179179 // (
            sum(ord(i) ** 2 for i in a[::3]) + 1) * 179 + len(a))
    # BAD HASH int((((len(a)*len(set(a))*12589)%5173580 + 179)*sum(ord(i) for i in a))//(len(a) + 25 * 179 / len(a)))
    return b


class ObjectCity:
    def __init__(self):
        self.city = City("Unnamed")
        self.access = False
        self.password = 0
        self.base = None
        self.sql = None

    def decorate_route(self, route):
        if route is None:
            return "Bad route data"
        s = ""
        for i in route[0].route:
            s += f"on {i[0]}: "
            s += " -> ".join(i[1])
            s += "\n"
        s += "\n" * 100
        s += str(route)
        return s

    def execute(self, txt: str) -> str:
        if self.sql is not None:
            self.sql.execute("""INSERT INTO full_log(date, request) VALUES(?, ?)""",
                             (repr(datetime.datetime.now()), str(txt)))
            self.base.commit()
        try:
            if txt.startswith("help"):
                return """
legend: (X) - parameter, [X] - optional parameter
valid commands:
    USER COMMANDS -----------------------------
    help -> this page.
    list -> generously information about city.
    route (from) (to) [time = 0:0] [weight time = 1] [weight money = 0.001]
        -> makes route from (from) to (to).
    load (filename) -> load info from file.
    
    
    EDITOR COMMANDS:
    to edit file you need get access.
    !!! edit [password] -> getting access, if there is no password,
            don't enter password at all.
    and after getting access, you can do:
    
    save (filename) -> save info to file.
    start_log (filename) -> start logging in filename. All logs making by SQLite3,
            DB1 - routes:
                date, request, sfrom, sto, res.
            DB2 - full_log:
                date, request.
    deploy -> placing all stations at map like it can be in real.
    add_station / as (name)
    add_route / ar (station1) (station2) (transport) (type of time) (time) (type of wait) (wait) ->
        add route from station1 to station2 and back, at transport,
        !!! wait need and time needed write in [] and doesn't include spaces!: like 3 [35,3:00,15:00] or 1 [15]
        with time and it's type:
            types of time:                      time needed
        1 - standard (constant)         (constant time)
        2 - time with pike hours        (basic time) [time at peak = basic time * 2]
        
        wait time:
            types of wait:                      wait needed
        1 - standard (constant)         (constant time)
        2 - time with pike hours        (basic time) [time at peak = basic time * 2]
        3 - route with schedule         (one transport once at time) [from time = 0:00] [to time = 23:59]
                                # train, starting at 6 and routes to 21, every hour will be
                                     (wait type) = 3, (and wait need) = [60 6:00 19:00]
        
    add_single_route / asr (station1) (station2) (transport) (type of time) (time) (type of wait) (wait) ->
        like add_route, but route will be only one side (from station1 to station2)
    set_password (password now, if no password, don't enter anything) [password2, if empty - no password.] ->
                                                                                                set password2 as main.
    set_pos (name_station) (xpos) (ypos) -> set station position.
            """
            elif txt.startswith("list"):
                return str(self.city)
            elif txt.startswith("route "):
                a = txt.split()[1:]
                print(a)
                r = None
                if len(a) == 2:
                    r = self.city.make_route(a[0], a[1], Time(0))
                elif len(a) == 3:
                    r = self.city.make_route(a[0], a[1], Time(h=int(a[2].split(":")[0]),
                                                              m=int(a[2].split(":")[1])))
                elif len(a) == 4:
                    r = self.city.make_route(a[0], a[1], Time(h=int(a[2].split(":")[0]),
                                                              m=int(a[2].split(":")[1])),
                                             float(a[3]))
                elif len(a) >= 5:
                    r = self.city.make_route(a[0], a[1], Time(h=int(a[2].split(":")[0]),
                                                              m=int(a[2].split(":")[1])),
                                             float(a[3]), float(a[4]))
                print(a)
                if self.sql is not None:
                    self.sql.execute("""INSERT INTO routes(date, request, sfrom, sto, result) VALUES(?, ?, ?, ?, ?)""",
                                     (repr(datetime.datetime.now()), str(txt), str(r[0].route[0][1][0]),
                                      str(r[0].route[-1][1][-1]), str(r)))
                    self.base.commit()
                print(a)
                return self.decorate_route(r), r
            elif txt.startswith("load "):
                a = txt.split()[1:]
                self.access = False
                self.password = self.city.load(a[0])

                return f"loaded {self.city.name}: \n\n{self.city}"
            elif txt.startswith("edit"):
                a = txt.split()[1:]
                if len(a) == 0:
                    a = ['']
                if self.access:
                    return "access already exist"
                if hashing(a[0]) == self.password:
                    self.access = True
                    return "access established"
                return "wrong password"
            elif txt.startswith("save ") and self.access:
                a = txt.split()[1:]
                self.city.save(a[0], self.password)
                return "saved."
            elif txt.startswith("start_log") and self.access:
                a = txt.split()[1:]
                if self.base:
                    self.sql.close()
                    self.base.commit()
                    self.base.close()
                self.base = sqlite3.connect(f"Data/{a[0]}")
                self.sql = self.base.cursor()
                self.sql.execute("""DROP TABLE IF EXISTS routes;""")
                self.sql.execute("""DROP TABLE IF EXISTS full_log;""")
                self.sql.execute("""CREATE TABLE routes (
                    date varchar(70),
                    request varchar(250),
                    sfrom varchar(70),
                    sto varchar(70),
                    result varchar(500));""")
                self.sql.execute("""CREATE TABLE full_log (
                    date varchar(70),
                    request varchar(250));""")
                return "Ok."
            elif txt.startswith("deploy") and self.access:
                self.city.auto_deploy()
                return "deployed."
            elif (txt.startswith("add_station ") or txt.startswith("as ")) and self.access:
                a = txt.split()[1:]
                self.city.add_station(a[0])
                return f"added station {a[0]}."
            elif (txt.startswith("add_route ") or txt.startswith("ar ")) and self.access:
                a = txt.split()[1:]
                if a[2] not in self.city.transports.keys():
                    return f"Previously make transport {a[2]}"
                et = []
                for i in a[4].replace('[', '').replace(']', '').split(','):
                    if ':' in i:
                        et.append(Time(h=int(i.split(':')[0]), m=int(i.split(':')[1])))
                    else:
                        et.append(int(i))
                if a[3] == '1':
                    if len(et) == 0:
                        return "Somthing bad here"
                    et = et[:1]
                if a[3] == '2':
                    if len(et) == 1:
                        et += [et[0] + et[0]]
                    if len(et) == 0:
                        return "Somthing bad here"
                    et = et[:2]
                ew = []
                for i in a[4].replace('[', '').replace(']', '').split(','):
                    if ':' in i:
                        ew.append(int(i.split(':')[0] * 60 + int(i.split(':')[1])))
                    else:
                        ew.append(int(i))
                if a[3] == '1':
                    if len(et) == 0:
                        return "Somthing bad here"
                    ew = ew[:1]
                if a[3] == '2':
                    if len(et) == 1:
                        et += [et[0] + et[0]]
                    if len(et) == 0:
                        return "Somthing bad here"
                    ew = ew[:2]
                if a[3] == '3':
                    if len(et) == 2:
                        et += [23 * 60 + 59]
                    if len(et) == 1:
                        et += [0, 23 * 60 + 59]
                    if len(et) == 0:
                        return "Somthing bad here"
                    ew = ew[:3]
                self.city.stations[a[0]].add_route(Route([int(a[3])] + et, a[1], [int(a[5])] + ew, a[2]))
                self.city.stations[a[1]].add_route(Route([int(a[3])] + et, a[0], [int(a[5])] + ew, a[2]))
                return f"added route {a[0]} with {a[1]}."
            elif (txt.startswith("add_single_route ") or txt.startswith("asr ")) and self.access:
                a = txt.split()[1:]
                if a[2] not in self.city.transports.keys():
                    return f"Previously make transport {a[2]}"
                et = []
                for i in a[4].replace('[', '').replace(']', '').split(','):
                    if ':' in i:
                        et.append(Time(h=int(i.split(':')[0]), m=int(i.split(':')[1])))
                    else:
                        et.append(int(i))
                if a[3] == '1':
                    if len(et) == 0:
                        return "Somthing bad here"
                    et = et[:1]
                if a[3] == '2':
                    if len(et) == 1:
                        et += [et[0] + et[0]]
                    if len(et) == 0:
                        return "Somthing bad here"
                    et = et[:2]
                ew = []
                for i in a[4].replace('[', '').replace(']', '').split(','):
                    if ':' in i:
                        ew.append(int(i.split(':')[0] * 60 + int(i.split(':')[1])))
                    else:
                        ew.append(int(i))
                if a[3] == '1':
                    if len(et) == 0:
                        return "Somthing bad here"
                    ew = ew[:1]
                if a[3] == '2':
                    if len(et) == 1:
                        et += [et[0] + et[0]]
                    if len(et) == 0:
                        return "Somthing bad here"
                    ew = ew[:2]
                if a[3] == '3':
                    if len(et) == 2:
                        et += [23 * 60 + 59]
                    if len(et) == 1:
                        et += [0, 23 * 60 + 59]
                    if len(et) == 0:
                        return "Somthing bad here"
                    ew = ew[:3]
                self.city.stations[a[0]].add_route(Route([int(a[3])] + et, a[1], [int(a[5])] + ew, a[2]))
                return f"added single route from {a[0]} to {a[1]}."
            elif txt.startswith("set_password") and self.access:
                a = txt.split()[1:]
                if len(a) == 0:
                    a = ['', '']
                if len(a) == 1:
                    a = ['', a[0]]
                if hashing(a[0]) == self.password:
                    self.password = hashing(a[1])
                    return "password replaced."
                return "wrong password"
            elif txt.startswith("set_pos ") and self.access:
                a = txt.split()[1:]
                self.city.stations[a[0]].set_pos((int(a[1]), int(a[2])))
                return "pos is set."
            return None
        except BaseException as e:
            return str(type(e)) + str(e)
