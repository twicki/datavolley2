import os
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen, QPolygon, QPolygonF
from PyQt5.QtWidgets import QApplication

from tvrscouting.analysis.basic_filter_widget import Basic_Filter
from tvrscouting.statistics.Actions.GameAction import Quality, Action
from tvrscouting.uis.cone_analysis import Ui_Form


class ConeAnalysis:
    def __init__(self, action_type, from_position, to_position, quality, percentage):
        self.action_type = action_type
        self.from_position = from_position
        self.to_position = to_position
        self.quality = quality
        self.percentage = percentage


def quality_to_float(quality):
    if quality == Quality.Perfect or quality == Quality.Kill:
        return 1
    elif quality == Quality.Good:
        return 0.5
    elif quality == Quality.Bad:
        return 0.2
    elif quality == Quality.Over:
        return 0.2
    else:
        return 0


class Main(QtWidgets.QWidget, Ui_Form, Basic_Filter):
    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self.game_state = None
        self.outline_color = QColor(167, 176, 174, 255)
        self.net_color = QColor(0, 0, 0, 255)
        self.background_color = QColor(21, 157, 136, 255)
        self.legend_color = QColor(128, 128, 124, 255)
        self.court_color = QColor(211, 94, 16, 255)
        self.analysis = []

    def paint_legend(self, painter):
        painter.fillRect(680, 350, 200, 220, self.legend_color)
        painter.fillRect(710, 382, 30, 30, QColor(59, 116, 218, 255))
        painter.fillRect(710, 422, 30, 30, QColor(39, 223, 116, 255))
        painter.fillRect(710, 462, 30, 30, QColor(211, 197, 23, 255))
        painter.fillRect(710, 502, 30, 30, QColor(231, 73, 12, 255))

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
        self.paint_legend(painter)
        self.paintAnalysis(painter)

    @staticmethod
    def cone_from_rhs(to_zone):
        if to_zone in [5, 7]:
            return 1
        elif to_zone == 4:
            return 8
        elif to_zone in [2, 3]:
            return 7
        elif to_zone == 9:
            return 6
        elif to_zone == 8:
            return 5
        elif to_zone == 1:
            return 5
        else:
            return 4

    @staticmethod
    def cone_from_lhs(to_zone):
        if to_zone in [1, 9]:
            return 1
        elif to_zone == 2:
            return 8
        elif to_zone in [3, 4]:
            return 7
        elif to_zone == 7:
            return 6
        elif to_zone == 8:
            return 5
        elif to_zone == 5:
            return 5
        else:
            return 4

    @staticmethod
    def cone_from_center(to_zone):
        if to_zone == 1:
            return 3
        elif to_zone == [2, 9]:
            return 1
        elif to_zone == [3, 8]:
            return 8
        elif to_zone == [4, 7]:
            return 7
        elif to_zone == 6:
            return 4
        else:
            return 5

    @staticmethod
    def cone_from_zone(from_zone, to_zone):
        if from_zone in [1, 2, 9]:
            return Main.cone_from_rhs(to_zone)
        elif from_zone in [4, 5, 7]:
            return Main.cone_from_lhs(to_zone)
        else:
            return Main.cone_from_center(to_zone)

    @staticmethod
    def get_start_x_from_cone(cone):
        if cone.action_type in ["h", "b"]:
            if cone.from_position in [2, 3, 4]:
                return 330
            elif cone.from_position in [7, 8, 9]:
                return 230
            else:
                return 130
        elif cone.action_type == "s":
            if cone.from_position in [2, 3, 4]:
                return 230
            elif cone.from_position in [7, 8, 9]:
                return 130
            else:
                return 30
        else:
            if cone.from_position in [2, 3, 4]:
                return 280
            elif cone.from_position in [7, 8, 9]:
                return 180
            else:
                return 80

    @staticmethod
    def get_start_y_from_cone(cone):
        if cone.from_position in [1, 2, 9]:
            return 580
        elif cone.from_position in [3, 6, 8]:
            return 480
        # elif cone.from_position in [4, 5, 7]:
        else:
            return 380

    @staticmethod
    def get_end_x_from_zone_indicator(zone):
        if zone in [2, 3, 4]:
            return 380
        elif zone in [7, 8, 9]:
            return 480
        else:
            return 580

    @staticmethod
    def get_end_x_from_cone_indicator(cone):
        start_point = cone.from_position
        end_point = cone.to_position
        if start_point in [3, 6, 8]:
            if end_point in [2, 3, 4, 5, 6]:
                return 580
            else:
                return 480
        else:
            if end_point in [1, 2, 3, 4, 5]:
                return 580
            elif end_point == 6:
                return 480
            elif end_point == 7:
                return 380
            else:  # end_point == 8
                return 340

    @staticmethod
    def get_end_x_from_cone(cone):
        if cone.action_type in ["h"]:
            return Main.get_end_x_from_cone_indicator(cone)
        else:
            return Main.get_end_x_from_zone_indicator(cone.to_position)

    @staticmethod
    def get_end_y_from_zone_indicator(zone):
        if zone in [4, 5, 7]:
            return 580
        elif zone in [3, 6, 8]:
            return 480
        # elif zone in [1, 2, 9]:
        else:
            return 380

    @staticmethod
    def get_end_y_from_cone_indicator(cone):
        start_point = cone.from_position
        end_point = cone.to_position
        if start_point in [3, 6, 8]:
            if end_point == 2:
                return 355
            elif end_point == 3:
                return 405
            elif end_point == 4:
                return 480
            elif end_point == 5:
                return 555
            elif end_point == 6:
                return 605
            elif end_point == 7:
                return 580
            elif end_point == 8:
                return 480
            else:  # end_point == 1:
                return 380
        elif start_point in [4, 5, 7]:
            if end_point == 1:
                return 355
            elif end_point == 2:
                return 405
            elif end_point == 3:
                return 455
            elif end_point == 4:
                return 505
            elif end_point in [5, 6, 7]:
                return 580
            else:  # end_point == 8
                return 380
        else:  # if start_point in [1,2,9]:
            if end_point == 1:
                return 605
            elif end_point == 2:
                return 555
            elif end_point == 3:
                return 505
            elif end_point == 4:
                return 455
            elif end_point in [5, 6, 7]:
                return 380
            else:  # end_point == 8
                return 580

    @staticmethod
    def get_end_y_from_cone(cone):
        if cone.action_type in ["h"]:
            return Main.get_end_y_from_cone_indicator(cone)
        else:
            return Main.get_end_y_from_zone_indicator(cone.to_position)

    def paintAnalysis(self, painter):
        for cone in self.analysis:
            startpoint_x = self.get_start_x_from_cone(cone)
            startpoint_y = self.get_start_y_from_cone(cone)

            endpoint_x = self.get_end_x_from_cone(cone)
            endpoint_y = self.get_end_y_from_cone(cone)
            size = 80 * cone.percentage

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
                # blue
                color = QColor(59, 116, 218, 255)
            elif cone.quality < 0.5:
                # green
                color = QColor(39, 223, 116, 255)
            elif cone.quality < 0.7:
                # golden
                color = QColor(211, 197, 23, 255)
            else:
                # red
                color = QColor(231, 73, 12, 255)
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.drawPolyline(QPolygon(p1))
            painter.fillPath(qpath, color)

    def analyze(self):
        directions = {}
        total = 0
        for action in self.actions:
            if int(action.direction[0]) > 0 and int(action.direction[1]) > 0:
                to_direction = int(action.direction[1])
                if action.direction_type == "z" and action.action == Action.Hit:
                    to_direction = self.cone_from_zone(
                        int(action.direction[0]), int(action.direction[1])
                    )
                category = "center"
                if str(action.action) in ["h", "b"]:
                    category = "front"
                if str(action.action) == "s":
                    category = "back"
                key = str(action.direction[0]) + str(to_direction) + category
                if key in directions:
                    directions[key]["quantity"] += 1
                    directions[key]["quality"] += quality_to_float(action.quality)
                    total += 1
                else:
                    directions[key] = {
                        "type": str(action.action),
                        "from": action.direction[0],
                        "to": to_direction,
                        "quality": quality_to_float(action.quality),
                        "quantity": 1,
                    }
                    total += 1
        self.analysis.clear()
        for value in directions.values():
            self.analysis.append(
                ConeAnalysis(
                    value["type"],
                    int(value["from"]),
                    int(value["to"]),
                    value["quality"] / value["quantity"],
                    value["quantity"] / total,
                )
            )
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.resize(1200, 800)
    ex.show()
    sys.exit(app.exec_())
