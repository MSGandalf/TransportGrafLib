from transport_lib import *
import pygame


def radius(x, y, xx=0, yy=0): return ((x - xx) ** 2 + (y - yy) ** 2) ** 0.5


FPS = 60
W = 1000  # ширина экрана
H = 1000  # высота экрана
pygame.init()
# pygame.mixer.set_num_channels(16)
sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
fn = pygame.font.Font(None, 15)
fn100 = pygame.font.Font(None, 100)
fn80 = pygame.font.Font(None, 80)
fn40 = pygame.font.Font(None, 40)
fn50 = pygame.font.Font(None, 50)

c = City("Moscow")

cx, cy = 0, 0

colors = (
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 100, 0),
    (255, 0, 100),
    (100, 255, 0),
    (100, 100, 0),
    (100, 100, 100),
    (0, 100, 255)
)


def draw_():
    global c
    sc.fill((0, 0, 0))
    for i in c.stations:
        pygame.draw.circle(sc, (30, 30, 30), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy), 17)
        for ii in c.stations[i].get_routes():
            pygame.draw.line(sc, (0, 40, 0), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy),
                             (c.stations[ii.next_station].pos[0] - cx, c.stations[ii.next_station].pos[1] - cy), 6)
    for i in c.stations:
        pygame.draw.circle(sc, (100, 100, 100), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy), 16)
        for ii in c.stations[i].get_routes():
            pygame.draw.line(sc, (0, 100, 0), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy),
                             (c.stations[ii.next_station].pos[0] - cx, c.stations[ii.next_station].pos[1] - cy), 4)
    for i in c.stations:
        pygame.draw.circle(sc, (255, 255, 255), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy), 15)
        text = fn50.render(i, True, (255, 255, 255))
        sc.blit(text, (c.stations[i].pos[0] - cx - 50, c.stations[i].pos[1] - cy + 20))
        for ii in c.stations[i].get_routes():
            pygame.draw.line(sc, (0, 255, 0), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy),
                             (c.stations[ii.next_station].pos[0] - cx, c.stations[ii.next_station].pos[1] - cy), 2)


def draw():
    global c
    sc.fill((0, 0, 0))
    t = {}
    for n, i in enumerate(c.transports):
        pygame.draw.line(sc, colors[n], (10, 50 + n * 40), (100, 50 + n * 40), 2)
        text = fn50.render(i, True, colors[n])
        sc.blit(text, (10, 50 + n * 40 - text.get_height()))
        t[i] = n
    for i in c.stations:
        pygame.draw.circle(sc, (30, 30, 30), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy), 17)
        for ii in c.stations[i].get_routes():
            if ii.transport in t:
                pygame.draw.line(sc, list(map(lambda x: x // 7, colors[t[ii.transport]])),
                                 (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy),
                                 (c.stations[ii.next_station].pos[0] - cx, c.stations[ii.next_station].pos[1] - cy), 10)
    for i in c.stations:
        pygame.draw.circle(sc, (100, 100, 100), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy), 16)
        for ii in c.stations[i].get_routes():
            if ii.transport in t:
                pygame.draw.line(sc, list(map(lambda x: x // 3, colors[t[ii.transport]])),
                                 (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy),
                                 (c.stations[ii.next_station].pos[0] - cx, c.stations[ii.next_station].pos[1] - cy), 7)
    for i in c.stations:
        pygame.draw.circle(sc, (255, 255, 255), (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy), 15)
        text = fn50.render(i, True, (255, 255, 255))
        sc.blit(text, (c.stations[i].pos[0] - cx - 50, c.stations[i].pos[1] - cy + 20))
        for ii in c.stations[i].get_routes():
            if ii.transport in t:
                pygame.draw.line(sc, colors[t[ii.transport]], (c.stations[i].pos[0] - cx, c.stations[i].pos[1] - cy),
                                 (c.stations[ii.next_station].pos[0] - cx, c.stations[ii.next_station].pos[1] - cy), 4)
    if route is not None:
        text = fn50.render(
            f"road - {int(Time(a=route.time).h())}:{round(Time(a=route.time).m()):02}, at end - {int(Time(a=route.timenow).h())}:{round(Time(a=route.timenow).m()):02}",
            True, (255, 255, 255))
        sc.blit(text, (W - 600, 10))
        text = fn50.render(f"will cost {route.cost}.", True, (255, 255, 255))
        sc.blit(text, (W - 600, 70))
        for i in route.route:
            for n in range(len(i[1]) - 1):
                pygame.draw.line(sc, list(map(lambda x: x // 7, colors[t[i[0]]])),
                                 (c.stations[i[1][n]].pos[0] - cx, c.stations[i[1][n]].pos[1] - cy),
                                 (c.stations[i[1][n + 1]].pos[0] - cx, c.stations[i[1][n + 1]].pos[1] - cy), 22)
            for n in range(len(i[1]) - 1):
                pygame.draw.line(sc, list(map(lambda x: x // 3, colors[t[i[0]]])),
                                 (c.stations[i[1][n]].pos[0] - cx, c.stations[i[1][n]].pos[1] - cy),
                                 (c.stations[i[1][n + 1]].pos[0] - cx, c.stations[i[1][n + 1]].pos[1] - cy), 19)
            for n in range(len(i[1]) - 1):
                pygame.draw.line(sc, colors[t[i[0]]],
                                 (c.stations[i[1][n]].pos[0] - cx, c.stations[i[1][n]].pos[1] - cy),
                                 (c.stations[i[1][n + 1]].pos[0] - cx, c.stations[i[1][n + 1]].pos[1] - cy), 15)
    if sel1 != -1:
        pygame.draw.circle(sc, (100, 30, 0), (c.stations[sel1].pos[0] - cx, c.stations[sel1].pos[1] - cy), 22)
        pygame.draw.circle(sc, (200, 60, 0), (c.stations[sel1].pos[0] - cx, c.stations[sel1].pos[1] - cy), 20)
        pygame.draw.circle(sc, (255, 100, 0), (c.stations[sel1].pos[0] - cx, c.stations[sel1].pos[1] - cy), 18)
    if sel2 != -1:
        pygame.draw.circle(sc, (0, 100, 30), (c.stations[sel2].pos[0] - cx, c.stations[sel2].pos[1] - cy), 22)
        pygame.draw.circle(sc, (0, 200, 60), (c.stations[sel2].pos[0] - cx, c.stations[sel2].pos[1] - cy), 20)
        pygame.draw.circle(sc, (0, 255, 100), (c.stations[sel2].pos[0] - cx, c.stations[sel2].pos[1] - cy), 18)
    if sell != -1:
        text = fn50.render(f"selected {list(c.transports.keys())[sell]}", True, (255, 255, 255))
        sc.blit(text, (10, H - 50))


def f(x):
    if x is not None:
        return int(x)


route = None
sel1, sel2, sell = -1, -1, -1
if input("START?   ('y'/'n')    ") == 'y':
    if input("CONSOLE?    ('y'/'n')    ") == 'y':
        last = ''
        while True:
            draw()
            pygame.display.update()
            pygame.event.get()
            a = input(">>>")
            try:
                b = a.split()
                if a.startswith(" "):
                    a = last + a[2:]
                else:
                    b = b[1:]
                if a.startswith("xy ") or a.startswith("0 "):
                    last = 'xy '
                    cx = int(b[0])
                    cy = int(b[1])
                    print('OK')
                if a.startswith("add_station ") or a.startswith("1 "):
                    last = 'add_station '
                    c.add_station(Station(b[0]))
                    print('OK')
                elif a.startswith("add_route ") or a.startswith("2 "):
                    last = 'add_route '
                    c.stations[b[0]].add_route(Route([1, float(b[2])], b[1], [1, float(b[3])], b[4]))
                    print('OK')
                elif a.startswith("add_route_and_reverse ") or a.startswith("3 "):
                    last = 'add_route_and_reverse '
                    c.stations[b[0]].add_route(Route([1, float(b[2])], b[1], [1, float(b[3])], b[4]))
                    c.stations[b[1]].add_route(Route([1, float(b[2])], b[0], [1, float(b[3])], b[4]))
                    print('OK')
                elif a.startswith("add_transport ") or a.startswith("4 "):
                    last = 'add_transport '
                    c.add_transport(Transport(b[0], int(b[1])))
                    print('OK')
                if a.startswith("setxy ") or a.startswith("5 "):
                    last = 'setxy '
                    c.stations[b[0]].set_pos((int(b[1]), int(b[2])))
                    print('OK')
                elif a.startswith("load "):
                    last = 'load '
                    c.load(b[0])
                    print('OK')
                elif a.startswith("save "):
                    last = 'save '
                    c.save(b[0])
                    print('OK')
                elif a.startswith("list"):
                    last = 'list'
                    print(c)
                elif a.startswith("route "):
                    last = 'route '
                    b += [None] * 10
                    print(*c.make_route(b[0], b[1], Time(h=int(b[2]), m=int(b[3]))), sep='\n')
                elif a.startswith("get_routes "):
                    last = 'get_routes '
                    a = []
                    for i in c.stations:
                        for ii in c.stations[i].routes:
                            if ii.transport == b[0].lower():
                                a.append((ii.next_station, i, ii.time(Time(h=int(b[1]), m=int(b[2])))))
                    for i in sorted(a):
                        print(i[0], f'---{i[2]}m. at {b[1]}:{b[2]}-->', i[1])


                elif a.startswith("help") or a == "h":
                    last = 'help'
                    print("""
                1/add_station [name:str]
                2/add_route [name of station:str] [next station:str] [time of road:float] [frequency:float] [transport:str]
                3/add_route_and_reverse [name of station:str] [next station:str] [time of road:float] [frequency:float] [transport:str]
                4/add_transport [name:str] [cost:int]
                route [station1:str] [station2:str] [time_now_h:int] [time_now_m:int]       
                                               [[MAY BE] weight_of_time = 1] [[MAY BE] weight_of_money = 0] [[MAY BE] weight_of_time_in_foot_crossings = 1]
                load [name:str]
                save [name:str]
                    """)
                elif a.startswith("exit"):
                    exit()
            except Exception as e:
                print("ERROR:", e)
    else:
        a = True
        while a:
            a = False
            name = input("file to load:::::::")
            try:
                c.load(name)
            except Exception as e:
                print("ERROR:", e)
                a = True
        sel1 = -1
        sel2 = -1
        do = 1
        sell = -1
        route = None
        while True:
            draw()
            pygame.display.update()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    c.save(name)
                    exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        c.save(name)
                    if i.key == pygame.K_1:
                        do = 1
                    if i.key == pygame.K_2:
                        do = 2
                    if i.key == pygame.K_3:
                        do = 3
                    if i.key == pygame.K_4:
                        do = 4
                elif i.type == pygame.MOUSEBUTTONDOWN:
                    if i.button == 4:
                        sell -= 1
                        if sell < 0:
                            sell = len(c.transports.keys()) - 1
                    if i.button == 5:
                        sell += 1
                        if sell > len(c.transports.keys()) - 1:
                            sell = 0
                            if len(c.transports.keys()) - 1 == -1:
                                sell = -1
                    if i.button == 2:
                        mouse = pygame.mouse.get_pos()
                        mouse = (mouse[0] + cx, mouse[1] + cy)
                        if do == 1:
                            m = float('inf')
                            for a in c.stations:
                                if radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1]) < m:
                                    m = radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1])
                                    s = a
                            if route is None:
                                route = RouteContainer(c.transports, 0, s, 0, 1, 1, False)
                            else:
                                for a in c.stations[route.last].get_routes():
                                    if a.next_station == s:
                                        route.add(a)
                    if i.button == 1:
                        mouse = pygame.mouse.get_pos()
                        mouse = (mouse[0] + cx, mouse[1] + cy)
                        if do == 1:
                            if sel1 == -1:
                                m = float('inf')
                                for a in c.stations:
                                    if radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1]) < m:
                                        m = radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1])
                                        sel1 = a
                            elif sel2 == -1:
                                m = float('inf')
                                for a in c.stations:
                                    if radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1]) < m:
                                        m = radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1])
                                        sel2 = a
                                if sel1 != sel2:
                                    try:
                                        route = c.make_route(sel1, sel2, Time(a=0))[0]
                                    except BaseException as e:
                                        print("ERROR:", e)
                                        route = None
                                        sel1, sel2 = -1, -1

                                else:
                                    route = None
                                    sel1, sel2 = -1, -1
                            else:
                                route = None
                                sel1, sel2 = -1, -1
                        elif do == 2:
                            c.add_station(Station(input(">>>"), mouse))
                        elif do == 4:
                            m = float('inf')
                            for a in c.stations:
                                if radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1]) < m:
                                    m = radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1])
                                    sel1 = a
                elif i.type == pygame.MOUSEBUTTONUP:
                    if i.button == 1:
                        mouse = pygame.mouse.get_pos()
                        mouse = (mouse[0] + cx, mouse[1] + cy)
                        if do == 4:
                            m = float('inf')
                            for a in c.stations:
                                if radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1]) < m:
                                    m = radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1])
                                    sel2 = a
                            c.stations[sel1].add_route(
                                Route([1, int(input(">>>time>>>"))], sel2, [1, int(input(">>>freq>>>")), sell]))
                elif i.type == pygame.MOUSEMOTION:
                    mouse = pygame.mouse.get_pos()
                    mouse = (mouse[0] + cx, mouse[1] + cy)
                    if i.buttons[0] and do == 3:
                        m = float('inf')
                        for a in c.stations:
                            if radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1]) < m:
                                m = radius(mouse[0], mouse[1], c.stations[a].pos[0], c.stations[a].pos[1])
                                s = a
                        if m != float('inf'):
                            c.stations[s].set_pos((c.stations[s].pos[0] + i.rel[0], c.stations[s].pos[1] + i.rel[1]))
                    if i.buttons[2]:
                        cx -= i.rel[0]
                        cy -= i.rel[1]

c.add_station(Station("a", [0, 0]))
c.add_station(Station("b", [300, 100]))
c.add_station(Station("c", [300, 100]))
c.add_station(Station("d", [300, 100]))

c.stations["a"].add_route(Route([1, 1.6], "c", [1, 5], "Bus1"))
c.stations["c"].add_route(Route([1, 1.6], "b", [1, 5], "Bus1"))
c.stations["b"].add_route(Route([1, 1.6], "d", [1, 5], "Bus1"))
c.stations["a"].add_route(Route([1, 5], "d", [1, 5], "Bus2"))

c.add_transport(Transport("Bus1", 50))
c.add_transport(Transport("Bus2", 50))
c.add_transport(Transport("Bus3", 50))
# print(c)

# c.transports["Bus1"].cost = 54
# c.transports["Bus2"].cost = 54

print(c)

print(c.make_route("a", "d", Time(100)))
print(c.make_route_last("a", "d", Time(100)))

c.save(1)
