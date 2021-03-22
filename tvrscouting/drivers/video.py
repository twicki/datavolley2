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
from tvrscouting.analysis.basic_filter_widget import Basic_Filter


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


class Main(QtWidgets.QWidget, Ui_Dialog, Basic_Filter):
    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)
        ICON_PATH = os.path.join(os.path.dirname(__file__), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self._qt_setup()
        self._media_player_setup()
        self.set_up_game_state(game_state)
        self.current_action_index = 0
        self.nex_action_index = 1
        self.total_time = None
        self.leadup_time = 3
        self.isPaused = False
        self.displayed_actions = []
        self.next_item = None
        self.play_Actions = False
        self.auto_jump = True

    def reset_data(self):
        self.all_actions = []
        self.all_time_stamp_deltas = []
        self.all_time_stamps = []
        self.total_nuber_of_actions = 0

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
                    self.displayed_actions.append(
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
        ser = Serializer(self)
        game_state = ser.deserialize()
        self.set_up_game_state(game_state)

    def save_file(self):
        for new_action in self.all_actions:
            rally = new_action.from_rally
            action = new_action.action
            filter_string = (
                "%02d" % (rally[2][0])
                + "%02d" % (rally[2][0] + 1)
                + "%02d" % (rally[2][1])
                + "%02d" % (rally[2][1] + 1)
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
        ser = Serializer(self, self.game_state)
        ser.serialize()

    def apply_all_filters(self):
        if self.game_state is None:
            self.load_file()
            if self.game_state is None:
                return
        self.tableWidget.setRowCount(self.total_nuber_of_actions)
        filter_string = self.lineEdit.text()
        i = 0
        self.displayed_actions = []
        for action in self.all_actions:
            if isinstance(action.action, Gameaction):
                current_action = str(action.action)
                if (
                    self.check_all_rally_filters(action.from_rally)
                    and self.check_all_court_filters(action.from_rally[1])
                    and self.check_all_subaction_filters(action.from_rally)
                    and self.check_all_action_filters(current_action)
                ):
                    self.tableWidget.setItem(
                        0, i, QtWidgets.QTableWidgetItem(current_action)
                    )
                    self.displayed_actions.append(action)
                    i += 1
        self.tableWidget.setRowCount(i)
        self.tableWidget.scrollToBottom()
        self.lineEdit.clear()

    def set_mediaplayer_from_sliderposition(self, position):
        """Set the position"""
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 10000.0)

    def cell_was_clicked(self, row, column):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        current_action = self.displayed_actions[row]
        if modifiers == QtCore.Qt.ControlModifier:
            self.jump_to_current_action(current_action)
        elif modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            self.set_current_event_to_time(current_action)
        elif modifiers == QtCore.Qt.ShiftModifier:
            self.set_all_following_events_to_times(current_action)

        self.updateUI()

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.horizontalSlider.setValue(int(self.mediaplayer.get_position() * 10000))
        current_time = self.get_current_second_of_player()
        if self.auto_jump:
            self.next_item = None
            for index in range(len(self.displayed_actions) - 1):
                if (
                    current_time > self.displayed_actions[index].absolute_timestamp
                    and current_time
                    < self.displayed_actions[index + 1].absolute_timestamp
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

    def set_all_following_events_to_times(self, current_action):
        seconds = self.get_current_second_of_player()
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

    def set_current_event_to_time(self, current_action):
        current_action.absolute_timestamp = self.get_current_second_of_player()

    def jump_to_current_action(self, current_action):
        if self.total_time is None:
            self.OpenFile()
            return
        start_with_leadup = (
            current_action.absolute_timestamp - self.leadup_time
            if current_action.absolute_timestamp - self.leadup_time > 0
            else 0
        )
        percentage = start_with_leadup / self.total_time
        self.mediaplayer.set_position(percentage)

    def get_current_action_from_highlight(self):
        current_action = None
        if len(self.tableWidget.selectionModel().selectedRows()):
            row = self.get_current_row_of_selection()
            current_action = self.displayed_actions[row]
        return current_action

    def get_current_row_of_selection(self):
        if len(self.tableWidget.selectionModel().selectedRows()):
            return self.tableWidget.selectionModel().selectedRows()[0].row()
        else:
            return 0

    def select_next_cell(self):
        row = self.get_current_row_of_selection()
        self.tableWidget.clearSelection()
        if row < self.tableWidget.rowCount() - 1:
            self.tableWidget.item(row + 1, 0).setSelected(True)

    def select_previous_cell(self):
        row = self.get_current_row_of_selection()
        self.tableWidget.clearSelection()
        if row > 1:
            self.tableWidget.item(row - 1, 0).setSelected(True)

    def center_new_selection(self):
        row = self.get_current_row_of_selection()
        self.tableWidget.scrollToItem(
            self.tableWidget.item(row, 0),
            QtWidgets.QAbstractItemView.PositionAtCenter,
        )

    def keyPressEvent(self, e):
        current_action = self.get_current_action_from_highlight()
        print("event", e)
        if e.key() == QtCore.Qt.Key_F1:
            print(" jump to the event")
            if current_action:
                self.jump_to_current_action(current_action)
                self.center_new_selection()
        elif e.key() == QtCore.Qt.Key_F2:
            print(" setting current event")
            if current_action:
                self.set_current_event_to_time(current_action)
                self.select_next_cell()
                self.center_new_selection()
        elif e.key() == QtCore.Qt.Key_F4:
            print(" setting following events")
            if current_action:
                self.set_all_following_events_to_times(current_action)
        elif e.key() == QtCore.Qt.Key_Left:
            self.scroll_from_current_position(-5)
        elif e.key() == QtCore.Qt.Key_Right:
            self.scroll_from_current_position(5)
        elif e.key() == QtCore.Qt.Key_Down:
            self.select_next_cell()
            self.center_new_selection()
        elif e.key() == QtCore.Qt.Key_Up:
            self.select_previous_cell()
            self.center_new_selection()
        elif e.key() == QtCore.Qt.Key_Space:
            self.PlayPause()

    def set_position_from_time(self, time):
        if self.total_time:
            new_position = time / self.total_time
            self.mediaplayer.set_position(new_position)

    def get_current_second_of_player(self) -> float:
        if self.total_time:
            position = self.mediaplayer.get_position()
            return position * self.total_time
        return 0

    def scroll_from_current_position(self, time):
        new_time = self.get_current_second_of_player() + time
        self.set_position_from_time(new_time)

    def _media_player_setup(self):
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)

    def set_leadup_time(self):
        number = self.lineEdit.text()
        if number.isnumeric():
            self.leadup_time = float(number)
        else:
            print("unknown reset time")
        self.lineEdit.clear()

    def update_jumping_to_action(self):
        self.auto_jump = self.auto_jump_box.isChecked()

    def _qt_setup(self):
        self.pushButton.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.PlayEverything)
        self.pushButton_3.clicked.connect(self.PlayPauseActions)
        self.horizontalSlider.sliderMoved.connect(
            self.set_mediaplayer_from_sliderposition
        )
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.tableWidget.itemSelectionChanged.connect(self.update_player)
        self.load_button.clicked.disconnect()
        self.load_button.clicked.connect(self.load_file)
        self.saveFile_button.clicked.connect(self.save_file)
        self.reset_time_button.clicked.connect(self.set_leadup_time)
        self.auto_jump_box.clicked.connect(self.update_jumping_to_action)

        self.pushButton.keyPressEvent = self.keyPressEvent
        self.pushButton_2.keyPressEvent = self.keyPressEvent
        self.pushButton_3.keyPressEvent = self.keyPressEvent
        self.horizontalSlider.keyPressEvent = self.keyPressEvent
        self.tableWidget.keyPressEvent = self.keyPressEvent
        self.load_button.keyPressEvent = self.keyPressEvent
        self.saveFile_button.keyPressEvent = self.keyPressEvent
        self.action_filter_button.keyPressEvent = self.keyPressEvent
        self.court_filter_button.keyPressEvent = self.keyPressEvent
        self.rally_button.keyPressEvent = self.keyPressEvent
        self.reset_button.keyPressEvent = self.keyPressEvent
        self.load_button.keyPressEvent = self.keyPressEvent
        self.subaction_filter_button.keyPressEvent = self.keyPressEvent
        self.auto_jump_box.keyPressEvent = self.keyPressEvent


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())