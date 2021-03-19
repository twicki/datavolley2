import os
import sys
from time import sleep

from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFrame, QFileDialog

from tvrscouting.uis.video import Ui_Dialog
import tvrscouting.utils.vlc as vlc
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.analysis.filters import *


class TimestampedAction:
    def __init__(
        self,
        action,
        rally,
        absolute_timestamp=None,
        relative_timestamp=None,
    ):
        super().__init__()
        self.action = action
        self.from_rally = rally
        self.absolute_timestamp = absolute_timestamp
        self.relative_timestamp = relative_timestamp


class Main(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self, game_state=None):
        super().__init__()
        self.setupUi(self)
        self._qt_setup()
        self._media_player_setup()
        self.set_up_game_state(game_state)
        self._filter_setup()
        self.current_action_index = 0
        self.nex_action_index = 1
        self.total_time = None
        self.leadup_time = 3
        self.isPaused = False
        self.displayed_actions = []
        self.next_item = None
        self.play_Actions = False

    def reset_data(self):
        self.all_actions = []
        self.all_time_stamp_deltas = []
        self.all_time_stamps = []
        self.total_nuber_of_actions = 0

    def reset_all_filters(self):
        self.action_filter = "@@@@@"
        self.rally_filter = "@@@@@@@@"
        self.court_filter = "@@@@@@@@@@@@@"
        self.sub_action_filter = "@@@@@"

    def set_up_game_state(self, game_state):
        self.game_state = game_state
        self.reset_data()
        self.reset_all_filters()
        if game_state:
            # get the total count of actions:
            self.total_nuber_of_actions = 0
            for rally in self.game_state.rallies:
                for action in rally[0]:
                    self.total_nuber_of_actions += 1

            self.tableWidget.setRowCount(self.total_nuber_of_actions)
            self.tableWidget.setColumnCount(1)
            i = 0
            initial_time_stamp = None
            for rally in self.game_state.rallies:
                for action in rally[0]:
                    self.tableWidget.setItem(
                        0, i, QtWidgets.QTableWidgetItem(str(action))
                    )
                    if initial_time_stamp is None:
                        initial_time_stamp = action.time_stamp
                    if action.time_stamp:
                        relative_time_stamp = action.time_stamp - initial_time_stamp
                    else:
                        relative_time_stamp = 0
                    self.all_actions.append(
                        TimestampedAction(
                            action,
                            rally,
                            relative_time_stamp,
                            relative_time_stamp,
                        )
                    )
                    i += 1
            self.tableWidget.scrollToBottom()

    def load_file(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open File", os.path.expanduser("~")
        )[0]
        if not filename:
            return
        ser = Serializer()
        game_state = ser.deserialize(filename)
        self.set_up_game_state(game_state)

    def save_file(self):
        for new_action in self.all_actions:
            rally = new_action.from_rally
            action = new_action.action
            filter_string = (
                str(rally[2][0])
                + str(rally[2][0] + 1)
                + str(rally[2][1])
                + str(rally[2][1] + 1)
                + str(rally[3][0])
                + str(rally[3][1])
                + "@"
                + "@"
            )
            old_rallies = ralley_filter_from_string(
                filter_string, self.game_state.rallies
            )
            for old_rally in old_rallies:
                for old_action in old_rally[0]:
                    if str(old_action) == str(action):
                        old_action.time_stamp = new_action.absolute_timestamp
                        break
        ser = Serializer(self.game_state)
        ser.serialize("output_timed.tvr")

    def reset_filters_and_apply(self):
        self.reset_all_filters()
        self.apply_all_filters()

    def store_rally_filter(self):
        self.rally_filter = self.lineEdit.text()
        self.filter_table.setItem(1, 1, QtWidgets.QTableWidgetItem(self.rally_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def store_court_filter(self):
        self.court_filter = self.lineEdit.text()
        self.filter_table.setItem(2, 1, QtWidgets.QTableWidgetItem(self.court_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def store_action_filter(self):
        self.action_filter = self.lineEdit.text()
        self.filter_table.setItem(0, 1, QtWidgets.QTableWidgetItem(self.action_filter))
        self.lineEdit.clear()
        self.apply_all_filters()

    def apply_all_filters(self):
        self.tableWidget.setRowCount(self.total_nuber_of_actions)
        filter_string = self.lineEdit.text()
        i = 0
        self.displayed_actions = []
        for action in self.all_actions:
            if isinstance(action.action, Gameaction):
                current_action = str(action.action)
                if (
                    compare_ralley_to_string(self.rally_filter, action.from_rally)
                    and compare_court_to_string(action.from_rally[1], self.court_filter)
                    and compare_action_to_string(current_action, self.action_filter)
                ):
                    self.tableWidget.setItem(
                        0, i, QtWidgets.QTableWidgetItem(current_action)
                    )
                    self.displayed_actions.append(action)
                    i += 1
        self.tableWidget.setRowCount(i)
        self.tableWidget.scrollToBottom()
        self.lineEdit.clear()

    def setPosition(self, position):
        """Set the position"""
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 10000.0)

    def cell_was_clicked(self, row, column):
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        current_action = None
        current_action = self.displayed_actions[row]

        if modifiers == QtCore.Qt.ControlModifier:
            start_with_leadup = (
                current_action.absolute_timestamp - self.leadup_time
                if current_action.absolute_timestamp - self.leadup_time > 0
                else 0
            )
            percentage = start_with_leadup / self.total_time
            self.mediaplayer.set_position(percentage)
        elif modifiers == QtCore.Qt.ShiftModifier:
            position = self.mediaplayer.get_position()
            seconds = position * self.total_time
            delta_to_original = seconds - current_action.relative_timestamp
            previousActions = True
            for action in self.all_actions:
                if action.action == current_action.action:
                    previousActions = False
                if previousActions:
                    if (
                        action.absolute_timestamp is not None
                        and action.absolute_timestamp > seconds
                    ):
                        action.absolute_timestamp = seconds
                else:
                    if action.relative_timestamp is not None:
                        action.absolute_timestamp = (
                            action.relative_timestamp + delta_to_original
                        )

        elif modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            position = self.mediaplayer.get_position()
            seconds = position * self.total_time
            current_action.absolute_timestamp = seconds
        self.updateUI()

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.horizontalSlider.setValue(int(self.mediaplayer.get_position() * 10000))
        current_time = self.mediaplayer.get_position() * self.total_time
        self.next_item = None
        for index in range(len(self.displayed_actions) - 1):
            if (
                current_time > self.displayed_actions[index].absolute_timestamp
                and current_time < self.displayed_actions[index + 1].absolute_timestamp
            ):
                self.tableWidget.clearSelection()
                self.tableWidget.item(index, 0).setSelected(True)
                self.next_item = self.displayed_actions[index + 1]
                # TODO: scroll to this spot
                break

        if self.mediaplayer.is_playing():
            self.pushButton_2.setText("Pause")
            self.pushButton_3.hide()
        else:
            self.pushButton_2.setText("Play")
            self.pushButton_3.show()
            self.pushButton_3.setText("Play Actions")
        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

    def open(self):
        self.OpenFile()

    def get_duration(self, filename):
        import ffmpeg

        info = ffmpeg.probe(filename)

        self.total_time = float(info["format"]["duration"])

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer"""
        if filename is None:
            filename = QFileDialog.getOpenFileName(
                self, "Open File", os.path.expanduser("~")
            )[0]
        if not filename:
            return
        # create the media
        if sys.version < "3":
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.widget.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.widget.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.widget.winId()))
        self.PlayPause()
        self.get_duration(filename)
        sleep(0.05)
        self.PlayPause()

    def PlayPause(self):
        """Toggle play/pause status"""
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.timer.start()
            self.isPaused = False

    def PlayEverything(self):
        self.play_Actions = False
        self.PlayPause()

    def update_player(self):
        # TODO: this does not work
        if self.play_Actions:
            sleep(self.leadup_time)
            start_with_leadup = self.next_item.absolute_timestamp - self.leadup_time
            percentage = start_with_leadup / self.total_time
            self.mediaplayer.set_position(percentage)
            self.updateUI()

    def PlayPauseActions(self):
        """Toggle play/pause status"""
        self.play_Actions = True
        self.PlayPause()

    def Stop(self):
        """Stop player"""
        self.mediaplayer.stop()
        self.pushButton_2.setText("Play")

    def keyPressEvent(self, e):
        print("event", e)
        if e.key() == QtCore.Qt.Key_Return:
            print(" return")
        elif e.key() == QtCore.Qt.Key_Enter:
            print(" enter")
        elif e.key() == QtCore.Qt.Key_F2:
            print(" F2")
            self.filter_table.clearSelection()
            self.filter_table.item(3, 0).setSelected(True)

    def _media_player_setup(self):
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)

    def _qt_setup(self):
        self.pushButton.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.PlayEverything)
        self.pushButton_3.clicked.connect(self.PlayPauseActions)
        self.horizontalSlider.sliderMoved.connect(self.setPosition)
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.tableWidget.itemSelectionChanged.connect(self.update_player)

        self.loadFile_button.clicked.connect(self.load_file)
        self.saveFile_button.clicked.connect(self.save_file)

        self.add_action_filter.clicked.connect(self.store_action_filter)
        self.add_court_filter.clicked.connect(self.store_court_filter)
        self.add_rally_filter.clicked.connect(self.store_rally_filter)
        self.reset_filters.clicked.connect(self.reset_filters_and_apply)
        self.apply_filters_button.clicked.connect(self.apply_all_filters)

    def _filter_setup(self):
        self.filter_table.setRowCount(4)
        self.filter_table.setColumnCount(2)
        for i, what, filter_string in zip(
            range(4),
            ["Action", "Rally", "Court", "SubAction"],
            [
                self.action_filter,
                self.rally_filter,
                self.court_filter,
                self.sub_action_filter,
            ],
        ):
            self.filter_table.setItem(i, 0, QtWidgets.QTableWidgetItem(what))
            self.filter_table.setItem(i, 1, QtWidgets.QTableWidgetItem(filter_string))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())