import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datavolley2.uis.cone_analysis import Ui_Form
from datavolley2.analysis.basic_filter_widget import Basic_Filter
from datavolley2.statistics.Actions.GameAction import Quality

from PyQt5 import QtCore, QtGui, QtWidgets


class ConeAnalysis:
    def __init__(self, from_position, to_position, quality, percentage):
        self.from_position = from_position
        self.to_position = to_position
        self.quality = quality
        self.percentage = percentage


# def paint_court_out(painter):
#     # surrouding field:
#     background_color = QColor(21, 157, 136, 255)
#     painter.fillRect(10, 10, 640, 340, background_color)


# def paintEvent_out(widget, event):
#     painter = QPainter(widget)
#     paint_court_out(painter)


def quality_to_float(quality):
    if quality == Quality.Perfect or quality == Quality.Kill:
        return 1
    elif quality == Quality.Good:
        return 0.8
    elif quality == Quality.Bad:
        return 0.5
    elif quality == Quality.Over:
        return 0.2
    else:
        return 0


class Main(QtWidgets.QWidget, Ui_Form, Basic_Filter):
    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)
        self.game_state = None
        self.outline_color = QColor(167, 176, 174, 255)
        self.net_color = QColor(0, 0, 0, 255)
        self.background_color = QColor(21, 157, 136, 255)
        self.court_color = QColor(211, 94, 16, 255)
        self.analysis = []

    def paint_court(self, painter):
        painter.fillRect(10, 310, 640, 340, self.background_color)
        # home field
        painter.setPen(self.outline_color)
        painter.drawRect(30, 330, 100, 100)
        painter.fillRect(31, 331, 99, 99, self.court_color)
        painter.drawRect(30, 430, 100, 100)
        painter.fillRect(31, 431, 99, 99, self.court_color)
        painter.drawRect(30, 530, 100, 100)
        painter.fillRect(31, 531, 99, 99, self.court_color)
        painter.drawRect(130, 330, 100, 100)
        painter.fillRect(131, 331, 99, 99, self.court_color)
        painter.drawRect(130, 430, 100, 100)
        painter.fillRect(131, 431, 99, 99, self.court_color)
        painter.drawRect(130, 530, 100, 100)
        painter.fillRect(131, 531, 99, 99, self.court_color)
        painter.drawRect(230, 330, 100, 100)
        painter.fillRect(231, 331, 99, 99, self.court_color)
        painter.drawRect(230, 430, 100, 100)
        painter.fillRect(231, 431, 99, 99, self.court_color)
        painter.drawRect(230, 530, 100, 100)
        painter.fillRect(231, 531, 99, 99, self.court_color)

        # # guest field
        # painter.setPen(self.outline_color)
        painter.drawRect(330, 330, 100, 100)
        painter.fillRect(331, 331, 99, 99, self.court_color)
        painter.drawRect(330, 430, 100, 100)
        painter.fillRect(331, 431, 99, 99, self.court_color)
        painter.drawRect(330, 530, 100, 100)
        painter.fillRect(331, 531, 99, 99, self.court_color)
        painter.drawRect(430, 330, 100, 100)
        painter.fillRect(431, 331, 99, 99, self.court_color)
        painter.drawRect(430, 430, 100, 100)
        painter.fillRect(431, 431, 99, 99, self.court_color)
        painter.drawRect(430, 530, 100, 100)
        painter.fillRect(431, 531, 99, 99, self.court_color)
        painter.drawRect(530, 330, 100, 100)
        painter.fillRect(531, 331, 99, 99, self.court_color)
        painter.drawRect(530, 430, 100, 100)
        painter.fillRect(531, 431, 99, 99, self.court_color)
        painter.drawRect(530, 530, 100, 100)
        painter.fillRect(531, 531, 99, 99, self.court_color)
        # paint the net
        painter.setPen(QPen(self.net_color, 3))
        painter.drawLine(330, 330, 330, 630)
        painter.drawLine(330, 330, 325, 325)
        painter.drawLine(330, 330, 335, 325)
        painter.drawLine(330, 630, 325, 635)
        painter.drawLine(330, 630, 335, 635)

    def paintEvent(self, event):
        painter = QPainter(self)

        self.paint_court(painter)

        # self.analysis.append(ConeAnalysis(4, 1, 0.8, 0.7))
        # self.analysis.append(ConeAnalysis(4, 5, 0.3, 0.1))
        # self.analysis.append(ConeAnalysis(2, 5, 0.5, 0.2))
        self.paintAnalysis(painter)

    def paintAnalysis(self, painter):
        for cone in self.analysis:
            startpoint_x = 330 if cone.from_position in [2, 3, 4] else 230
            if cone.from_position in [1, 2, 9]:
                startpoint_y = 580
            elif cone.from_position in [3, 6, 8]:
                startpoint_y = 480
            # elif cone.from_position in [4, 5, 7]:
            else:
                startpoint_y = 380

            if cone.to_position in [4, 5, 7]:
                endpoint_y = 580
            elif cone.to_position in [3, 6, 8]:
                endpoint_y = 480
            # elif cone.to_position in [1, 2, 9]:
            else:
                endpoint_y = 380
            size = 80 * cone.percentage
            endpoint_x = 380 if cone.to_position in [2, 3, 4] else 580

            p1 = [
                QPoint(startpoint_x, startpoint_y),
                QPoint(endpoint_x, int(endpoint_y - size / 2)),
                QPoint(endpoint_x, int(endpoint_y + size / 2)),
                QPoint(startpoint_x, startpoint_y),
            ]
            polyF = QPolygonF()
            for p in p1:
                polyF.append(p)
            qpath = QPainterPath()
            qpath.addPolygon(polyF)
            if cone.quality < 0.3:
                color = QColor(59, 116, 218, 255)
            elif cone.quality < 0.5:
                color = QColor(39, 223, 116, 255)
            elif cone.quality < 0.7:
                color = QColor(211, 197, 23, 255)
            else:
                color = QColor(231, 73, 12, 255)
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.drawPolyline(QPolygon(p1))
            painter.fillPath(qpath, color)

    def analyze(self):
        directions = {}
        total = 0
        for action in self.actions:
            if int(action.direction[0]) > 0 and int(action.direction[1]) > 0:
                key = str(action.direction[0]) + str(action.direction[1])
                if key in directions:
                    directions[key]["quantity"] += 1
                    directions[key]["quality"] += quality_to_float(action.quality)
                    total += 1
                else:
                    directions[key] = {
                        "from": action.direction[0],
                        "to": action.direction[1],
                        "quality": quality_to_float(action.quality),
                        "quantity": 1,
                    }
                    total += 1
        self.analysis.clear()
        for value in directions.values():
            self.analysis.append(
                ConeAnalysis(
                    int(value["from"]),
                    int(value["to"]),
                    value["quality"] / total,
                    value["quantity"] / total,
                )
            )
        self.update()


# class Widget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.analysis = []

#     def paint_court(self, painter):
#         painter.fillRect(10, 310, 640, 340, self.background_color)
#         # home field
#         painter.setPen(self.outline_color)
#         painter.drawRect(30, 330, 100, 100)
#         painter.fillRect(31, 331, 99, 99, self.court_color)
#         painter.drawRect(30, 430, 100, 100)
#         painter.fillRect(31, 431, 99, 99, self.court_color)
#         painter.drawRect(30, 530, 100, 100)
#         painter.fillRect(31, 531, 99, 99, self.court_color)
#         painter.drawRect(130, 330, 100, 100)
#         painter.fillRect(131, 331, 99, 99, self.court_color)
#         painter.drawRect(130, 430, 100, 100)
#         painter.fillRect(131, 431, 99, 99, self.court_color)
#         painter.drawRect(130, 530, 100, 100)
#         painter.fillRect(131, 531, 99, 99, self.court_color)
#         painter.drawRect(230, 330, 100, 100)
#         painter.fillRect(231, 331, 99, 99, self.court_color)
#         painter.drawRect(230, 430, 100, 100)
#         painter.fillRect(231, 431, 99, 99, self.court_color)
#         painter.drawRect(230, 530, 100, 100)
#         painter.fillRect(231, 531, 99, 99, self.court_color)

#         # # guest field
#         # painter.setPen(self.outline_color)
#         painter.drawRect(330, 330, 100, 100)
#         painter.fillRect(331, 331, 99, 99, self.court_color)
#         painter.drawRect(330, 430, 100, 100)
#         painter.fillRect(331, 431, 99, 99, self.court_color)
#         painter.drawRect(330, 530, 100, 100)
#         painter.fillRect(331, 531, 99, 99, self.court_color)
#         painter.drawRect(430, 330, 100, 100)
#         painter.fillRect(431, 331, 99, 99, self.court_color)
#         painter.drawRect(430, 430, 100, 100)
#         painter.fillRect(431, 431, 99, 99, self.court_color)
#         painter.drawRect(430, 530, 100, 100)
#         painter.fillRect(431, 531, 99, 99, self.court_color)
#         painter.drawRect(530, 330, 100, 100)
#         painter.fillRect(531, 331, 99, 99, self.court_color)
#         painter.drawRect(530, 430, 100, 100)
#         painter.fillRect(531, 431, 99, 99, self.court_color)
#         painter.drawRect(530, 530, 100, 100)
#         painter.fillRect(531, 531, 99, 99, self.court_color)
#         # paint the net
#         painter.setPen(QPen(self.net_color, 3))
#         painter.drawLine(330, 330, 330, 630)
#         painter.drawLine(330, 330, 325, 325)
#         painter.drawLine(330, 330, 335, 325)
#         painter.drawLine(330, 630, 325, 635)
#         painter.drawLine(330, 630, 335, 635)

#     def paintEvent(self, event):
#         painter = QPainter(self)

#         self.widget.paint_court(self, painter)

#         # self.widget.analysis.append(ConeAnalysis(4, 1, 0.8, 0.7))
#         # self.widget.analysis.append(ConeAnalysis(4, 5, 0.3, 0.1))
#         # self.widget.analysis.append(ConeAnalysis(2, 5, 0.5, 0.2))
#         # self.widget.paintAnalysis(self, painter)

#     def paintAnalysis(self, painter):
#         for cone in self.widget.analysis:
#             startpoint_y = 330 if cone.from_position in [2, 3, 4] else 430
#             if cone.from_position in [1, 2]:
#                 startpoint_x = 280
#             elif cone.from_position in [3, 6]:
#                 startpoint_x = 180
#             elif cone.from_position in [4, 5]:
#                 startpoint_x = 80

#             if cone.to_position in [4, 5]:
#                 endpoint_x = 280
#             elif cone.to_position in [3, 6]:
#                 endpoint_x = 180
#             elif cone.to_position in [1, 2]:
#                 endpoint_x = 80
#             size = 80 * cone.percentage
#             endpoint_y = 280 if cone.to_position in [2, 3, 4] else 80

#             p1 = [
#                 QPoint(startpoint_x, startpoint_y),
#                 QPoint(endpoint_x - size / 2, endpoint_y),
#                 QPoint(endpoint_x + size / 2, endpoint_y),
#                 QPoint(startpoint_x, startpoint_y),
#             ]
#             polyF = QPolygonF()
#             for p in p1:
#                 polyF.append(p)
#             qpath = QPainterPath()
#             qpath.addPolygon(polyF)
#             color = Qt.red if cone.quality > 0.5 else Qt.blue
#             painter.setBrush(QBrush(color, Qt.SolidPattern))
#             painter.drawPolyline(QPolygon(p1))
#             painter.fillPath(qpath, color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.resize(1200, 800)
    ex.show()
    sys.exit(app.exec_())
