import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ObjectCityLib import ObjectCity, hashing

# c = ObjectCity()
# c.execute("load 3.txt")
# c.city.transports['bus1'].speed = 30
# c.city.transports['train'].speed = 60
# c.city.transports['subway'].speed = 60
# c.city.transports['bus2'].speed = 30
# c.city.transports['plane'].speed = 320
# print(c.city.transports)
# print(c.execute("edit"))
# print(c.execute("save 3.txt"))


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

TRANSPORT_COLORS = (
    (100, 100, 100),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 100, 0),
    (0, 100, 255),
    (100, 255, 0),
    (100, 0, 150),
    (0, 150, 0),
    (100, 150, 255)
)


def more_slidely(color1, color2):
    return tuple(map((lambda n: (n[0] + n[1]) // 2), zip(color1, color2)))


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.center = None
        self.press = False
        self.theme = 'light'
        self.W, self.H = 1000, 800
        self.sc, self.cx, self.cy = 1, 0, 0
        self.route = None
        self.last_pos = (self.cx, self.cy)
        self.obj = ObjectCity()
        self.initUI()
        self.resize_elements()

    def initUI(self):
        self.setGeometry(100, 100, self.W, self.H)
        self.setWindowTitle('Транспорт')
        self.setMouseTracking(True)

        self.console_input = QLineEdit(self)
        self.console_input.move(10, 10)

        self.result = QTextEdit(self)
        self.result.move(10, 60)

        self.setStyleSheet("background-color:rgb(255,255,220)")
        self.result.setStyleSheet("color: black;")
        self.console_input.setStyleSheet("color: black;")
        self.qp = QPainter()

    def scale(self, x, y):
        return int(x * self.sc - self.cx), int(y * self.sc - self.cy)

    def paintEvent(self, event):
        self.qp.begin(self)
        text_color = ((255, 255, 255) if self.theme != 'light' else (0, 0, 0))
        main_color = ((255, 255, 220) if self.theme == 'light' else (0, 0, 0))
        coords = [[100, 200], [200, 300], [300, 100]]
        for s in self.obj.city.stations:
            for i in self.obj.city.stations[s].get_routes():
                self.qp.setPen(
                    QPen(QBrush(QColor(*TRANSPORT_COLORS[list(self.obj.city.transports.keys()).index(i.transport)])),
                         5))
                self.qp.drawLine(*self.scale(*self.obj.city.stations[s].pos),
                                 *self.scale(*self.obj.city.stations[i.next_station].pos))
        if self.route is not None:
            for i in self.route.route:
                for ii in range(1, len(i[1])):
                    self.qp.setPen(QPen(QBrush(QColor(
                        *more_slidely(TRANSPORT_COLORS[list(self.obj.city.transports.keys()).index(i[0])],
                                      main_color))),
                        15))
                    self.qp.drawLine(*self.scale(*self.obj.city.stations[i[1][ii - 1]].pos),
                                     *self.scale(*self.obj.city.stations[i[1][ii]].pos))
                    self.qp.setPen(QPen(
                        QBrush(QColor(*TRANSPORT_COLORS[list(self.obj.city.transports.keys()).index(i[0])])), 5))
                    self.qp.drawLine(*self.scale(*self.obj.city.stations[i[1][ii - 1]].pos),
                                     *self.scale(*self.obj.city.stations[i[1][ii]].pos))
            self.qp.setPen(QColor(*text_color))
            self.qp.setFont(QFont('Decorative', 40))
            self.qp.drawText(QPoint(self.W // 3 + 20, 110), f'time:{self.route.time} cost:{self.route.cost}₽')
        for s in self.obj.city.stations:
            self.qp.setPen(QColor(*text_color))
            self.qp.setFont(QFont('Decorative', 30))
            self.qp.drawText(QPoint(*self.scale(*self.obj.city.stations[s].pos)), s)
        self.qp.setPen(QColor(*text_color))
        self.qp.setFont(QFont('Decorative', 30))
        y = 0
        for i in self.obj.city.transports:
            self.qp.setPen(QColor(*TRANSPORT_COLORS[list(self.obj.city.transports.keys()).index(i)]))
            self.qp.drawText(QPoint(self.W // 3 + 20, 200 + y), f'{i}, cost:{self.obj.city.transports[i].cost}₽')
            y += 50
        # self.qp.drawLine(*coords[2], *coords[0])
        # self.qp.drawEllipse(*[250, 250], 20, 20)
        # self.qp.drawRect(*[170, 170], *[20, 20])
        self.qp.end()

    def resizeEvent(self, event):
        self.W = self.size().width()
        self.H = self.size().height()
        self.resize_elements()

    def resize_elements(self):
        self.console_input.setGeometry(10, 10, self.W - 20, 40)
        self.result.setGeometry(10, 60, self.W // 3, self.H - 70)

    def execute(self, text):
        res = self.obj.execute(text)
        if isinstance(res, tuple):
            self.route = res[1][0]
            res = res[0]
        if res is None and False:
            try:
                res = str(eval(text))
            except BaseException as e:
                res = str(e)
        if res is None:
            res = self.result.toPlainText()
        if self.obj.access:
            self.setStyleSheet("background-color:black")
            self.result.setStyleSheet("color: white;")
            self.console_input.setStyleSheet("color: white;")
            self.theme = 'dark'
        else:
            self.setStyleSheet("background-color:rgb(255,255,220)")
            self.result.setStyleSheet("color: black;")
            self.console_input.setStyleSheet("color: black;")
            self.theme = 'light'
        self.result.setText(res)
        if text.startswith('load '):
            self.cx, self.cy, self.sc = 0, 0, 1

    def mousePressEvent(self, event):
        self.last_pos = (event.x(), event.y())
        self.press = True

    def mouseMoveEvent(self, event):
        if self.press:
            self.cx -= event.x() - self.last_pos[0]
            self.cy -= event.y() - self.last_pos[1]
            self.last_pos = (event.x(), event.y())
            self.update()

    def wheelEvent(self, event):
        self.center = (self.W // 2 + self.cx) / self.sc, (self.H // 2 + self.cy) / self.sc
        self.sc *= (10 + event.angleDelta().y() / 120) / 10
        dx = self.scale(*self.center)[0] - self.W // 2
        dy = self.scale(*self.center)[1] - self.H // 2
        self.cx += dx
        self.cy += dy
        self.update()

    def mouseReleaseEvent(self, event):
        self.press = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.execute(self.console_input.text())
            self.console_input.setText("")
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
