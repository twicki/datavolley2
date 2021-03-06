import contextlib
import os
import sys
from time import sleep
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog

import tvrscouting.utils.vlc as vlc
from tvrscouting.analysis.basic_filter_widget import Basic_Filter
from tvrscouting.serializer.serializer import Serializer
from tvrscouting.statistics.Actions.GameAction import Gameaction
from tvrscouting.statistics.Gamestate.game import Game
from tvrscouting.statistics.Gamestate.game_state import GameState
from tvrscouting.uis.video import Ui_Dialog


class TimestampedAction:
    def __init__(
        self,
        action,
        rally,
        action_index=0,
        rally_index=0,
        absolute_timestamp=None,
        relative_timestamp=None,
    ):
        super().__init__()
        self.action = action
        self.from_rally = rally
        self.action_index = action_index
        self.rally_index = rally_index
        self.absolute_timestamp = absolute_timestamp
        self.relative_timestamp = relative_timestamp


class Main(QtWidgets.QWidget, Ui_Dialog, Basic_Filter):
    def __init__(self, game_state=None):
        super().__init__()
        Basic_Filter.__init__(self)
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/")
        icon = QtGui.QIcon.fromTheme(ICON_PATH + "tvrscouting.jpeg")
        self.setWindowIcon(icon)
        self._qt_setup()
        self._media_player_setup()
        self.set_volume(0)
        self.set_up_game_state(game_state)
        self.current_action_index = 0
        self.nex_action_index = 1
        self.total_time = None
        self.leadup_time = 3
        self.jump_threshold = 5
        self.isPaused = False
        self.displayed_actions = []
        self.next_item = None
        self.auto_jump: bool = False
        self.concurent_action: bool = False
        self.timer_start: Optional[float] = None
        self.hide_non_game_actions: bool = True

        self.jump_next_action_timer = QtCore.QTimer(self)
        self.jump_next_action_timer.setInterval(2 * self.leadup_time * 1000)
        self.jump_next_action_timer.timeout.connect(self.select_next_cell)

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
            self.update_action_view_from_game_state()

    def collect_total_number_of_actions(self):
        total_nuber_of_actions = 0
        for rally in self.game_state.rallies:
            for action in rally.actions:
                total_nuber_of_actions += 1
        return total_nuber_of_actions

    @contextlib.contextmanager
    def edit_table(self):
        self.action_view.itemChanged.connect(self.save_modified_version)
        self.action_view.itemChanged.disconnect()
        yield
        self.action_view.itemChanged.connect(self.save_modified_version)

    def update_action_view_from_game_state(self):
        self.total_nuber_of_actions = self.collect_total_number_of_actions()
        with self.edit_table():
            self.action_view.setRowCount(self.total_nuber_of_actions)
            self.action_view.setColumnCount(1)
            action_index = 0
            initial_time_stamp = None
            self.all_actions = []
            self.displayed_actions = []

            for rally_index, rally in enumerate(self.game_state.rallies):
                for action in rally.actions:
                    self.action_view.setItem(
                        0, action_index, QtWidgets.QTableWidgetItem(str(action))
                    )
                    self.action_view.setColumnWidth(action_index, 200)
                    if initial_time_stamp is None:
                        if action.time_stamp is not None:
                            initial_time_stamp = (
                                action.time_stamp if action.time_stamp > 5000 else 0
                            )
                    if action.time_stamp:
                        relative_time_stamp = action.time_stamp - initial_time_stamp
                    else:
                        relative_time_stamp = 0
                    self.all_actions.append(
                        TimestampedAction(
                            action,
                            rally,
                            action_index,
                            rally_index,
                            relative_time_stamp,
                            relative_time_stamp,
                        )
                    )
                    self.displayed_actions.append(
                        TimestampedAction(
                            action,
                            rally,
                            action_index,
                            rally_index,
                            relative_time_stamp,
                            relative_time_stamp,
                        )
                    )
                    action_index += 1
            self.action_view.scrollToBottom()

    def load_file(self):
        ser = Serializer(self)
        self.game = ser.deserialize()
        if self.game:
            game_state = self.game.game_state
            self.set_up_game_state(game_state)
            self.apply_all_filters()

    def save_file(self):
        new_game_state = GameState()
        rally_index = None
        rally_actions = []
        for new_action in self.all_actions:
            if rally_index != new_action.rally_index:
                rally_index = new_action.rally_index
                if len(rally_actions):
                    new_game_state.add_plain(rally_actions)
                    rally_actions = []
            new_action.action.time_stamp = new_action.absolute_timestamp
            rally_actions.append(new_action.action)
        if len(rally_actions):
            new_game_state.add_plain(rally_actions)
        self.game_state = new_game_state
        new_game = Game()
        new_game.game_state = self.game_state
        new_game.meta_info = self.game.meta_info
        ser = Serializer(self, new_game)
        ser.serialize()

    @contextlib.contextmanager
    def create_clean_game_state(self):
        new_game_state = GameState()
        yield new_game_state
        self.game_state = new_game_state
        self.update_action_view_from_game_state()
        self.apply_all_filters()

    def get_current_action_index_or_default(self):
        current_action = self.get_current_action_from_highlight()
        if current_action is None:
            if len(self.displayed_actions) == 0:
                return -1
            current_action = self.displayed_actions[0]
        return current_action.action_index

    def insert_action_after(self):
        row = self.get_current_row_of_selection()

        current_action_index = self.get_current_action_index_or_default()
        new_action_string = self.lineEdit.text()
        rally_index = None
        rally_actions = []
        with self.create_clean_game_state() as new_game_state:
            for new_action in self.all_actions:
                # create a new rally, store all the data if they don't match
                if rally_index != new_action.rally_index:
                    rally_index = new_action.rally_index
                    if len(rally_actions):
                        new_game_state.add_plain(rally_actions)
                        rally_actions = []
                new_action.action.time_stamp = new_action.absolute_timestamp
                rally_actions.append(new_action.action)
                if new_action.action_index == current_action_index:
                    for action in new_game_state.create_action_list_from_string(
                        new_action_string, new_action.absolute_timestamp
                    ):
                        rally_actions.append(action)
            if len(rally_actions):
                new_game_state.add_plain(rally_actions)

        self.action_view.clearSelection()
        self.action_view.item(row + 1, 0).setSelected(True)
        self.center_new_selection()

    def delete_current_action(self):
        current_action = self.get_current_action_from_highlight()
        if current_action is None:
            return
        row = self.get_current_row_of_selection()
        new_highlight_column = 0
        deleted_action_index = current_action.action_index

        rally_index = None
        rally_actions = []
        with self.create_clean_game_state() as new_game_state:
            for new_action in self.all_actions:
                if new_action.action_index != deleted_action_index:
                    # create a new rally, store all the data if they don't match
                    if rally_index != new_action.rally_index:
                        rally_index = new_action.rally_index
                        if len(rally_actions):
                            new_game_state.add_plain(rally_actions)
                            rally_actions = []
                    new_action.action.time_stamp = new_action.absolute_timestamp
                    rally_actions.append(new_action.action)
            if len(rally_actions):
                new_game_state.add_plain(rally_actions)
        self.action_view.clearSelection()
        if self.action_view.item(row, 0):
            self.action_view.item(row, 0).setSelected(True)
        elif self.action_view.item(row - 1, 0):
            self.action_view.item(row - 1, 0).setSelected(True)
        self.center_new_selection()

    def save_modified_version(self, item):
        changed_action_index = self.displayed_actions[item.row()].action_index
        highlited_row = item.row()
        action_str = item.text()

        rally_index = None
        rally_actions = []
        with self.create_clean_game_state() as new_game_state:
            for new_action in self.all_actions:
                # create a new rally, store all the data if they don't match
                if rally_index != new_action.rally_index:
                    rally_index = new_action.rally_index
                    if len(rally_actions):
                        new_game_state.add_plain(rally_actions)
                        rally_actions = []
                if new_action.action_index == changed_action_index:
                    for action in new_game_state.create_action_list_from_string(
                        action_str, new_action.absolute_timestamp
                    ):
                        rally_actions.append(action)
                else:
                    new_action.action.time_stamp = new_action.absolute_timestamp
                    rally_actions.append(new_action.action)
            if len(rally_actions):
                new_game_state.add_plain(rally_actions)

        self.action_view.clearSelection()
        self.action_view.item(highlited_row, 0).setSelected(True)
        self.center_new_selection()

    def apply_all_filters(self):
        if self.game_state is None:
            self.load_file()
            if self.game_state is None:
                return

        old_highlight_index = self.get_current_action_index_or_default()
        self.action_view.clearSelection()
        new_highlight_column = 0

        with self.edit_table():
            self.action_view.setRowCount(self.total_nuber_of_actions)
            i = 0
            self.displayed_actions = []
            for action in self.all_actions:
                if self.hide_non_game_actions:
                    if isinstance(action.action, Gameaction):
                        current_action = str(action.action)
                        if (
                            self.check_all_rally_filters(action.from_rally)
                            and self.check_all_court_filters(action.from_rally.court)
                            and self.check_all_subaction_filters(action.from_rally)
                            and self.check_all_action_filters(current_action)
                        ):
                            self.action_view.setItem(
                                0, i, QtWidgets.QTableWidgetItem(current_action)
                            )
                            self.action_view.setColumnWidth(i, 200)
                            self.displayed_actions.append(action)
                            i += 1
                            if action.action_index == old_highlight_index:
                                new_highlight_column = i
                else:
                    if isinstance(action, Gameaction):
                        current_action = str(action.action)
                        if (
                            self.check_all_rally_filters(action.from_rally)
                            and self.check_all_court_filters(action.from_rally.court)
                            and self.check_all_subaction_filters(action.from_rally)
                            and self.check_all_action_filters(current_action)
                        ):
                            self.action_view.setItem(
                                0, i, QtWidgets.QTableWidgetItem(current_action)
                            )
                            self.action_view.setColumnWidth(i, 200)
                            self.displayed_actions.append(action)
                            i += 1
                            if action.action_index == old_highlight_index:
                                new_highlight_column = i
                    else:
                        current_action = str(action.action)
                        if (
                            self.check_all_rally_filters(action.from_rally)
                            and self.check_all_court_filters(action.from_rally.court)
                            and self.check_all_subaction_filters(action.from_rally)
                        ):
                            self.action_view.setItem(
                                0, i, QtWidgets.QTableWidgetItem(current_action)
                            )
                            self.action_view.setColumnWidth(i, 200)
                            self.displayed_actions.append(action)
                            i += 1
                            if action.action_index == old_highlight_index:
                                new_highlight_column = i
            self.action_view.setRowCount(i)
        # since the table is one-indexed we need to remove 1
        new_highlight_column = (
            new_highlight_column - 1 if new_highlight_column > 0 else new_highlight_column
        )
        if self.action_view.item(new_highlight_column, 0):
            self.action_view.item(new_highlight_column, 0).setSelected(True)
            self.center_new_selection()
        self.lineEdit.clear()

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
        if self.timer_start:
            time_now = self.get_current_second_of_player()
            self.lcdNumber.show()
            self.lcdNumber.display(time_now - self.timer_start)
        if self.mediaplayer.is_playing():
            self.pushButton_2.setText("Pause")
        else:
            self.pushButton_2.setText("Play")
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
            filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser("~"))[0]
        if not filename:
            return
        # create the media
        if sys.version < "3":
            filename = unicode(filename)  # noqa
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
            self.jump_next_action_timer.stop()
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.timer.start()
            if self.concurent_action:
                self.jump_next_action_timer.start()
            self.isPaused = False

    def set_volume(self, position):
        self.mediaplayer.audio_set_volume(position)

    def set_mediaplayer_from_sliderposition(self, position):
        """Set the position"""
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 10000.0)

    def jump_to_current_cell(self):
        if self.auto_jump:
            current_action = self.get_current_action_from_highlight()
            if current_action:
                self.jump_to_current_action(current_action, self.jump_threshold)

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
                if action.absolute_timestamp is not None and action.absolute_timestamp > seconds:
                    action.absolute_timestamp = seconds
            else:
                if action.relative_timestamp is not None:
                    action.absolute_timestamp = action.relative_timestamp + delta_to_original

    def set_current_event_to_time(self, current_action):
        current_action.absolute_timestamp = self.get_current_second_of_player()

    def jump_to_current_action(self, current_action, jump_threshold=0):
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
        self.updateUI()

    def get_current_action_from_highlight(self):
        current_action = None
        if len(self.action_view.selectionModel().selectedRows()):
            row = self.get_current_row_of_selection()
            current_action = self.displayed_actions[row]
        return current_action

    def get_current_row_of_selection(self):
        if len(self.action_view.selectionModel().selectedRows()):
            return self.action_view.selectionModel().selectedRows()[0].row()
        else:
            return 0

    def select_next_cell(self):
        row = self.get_current_row_of_selection()
        if row < self.action_view.rowCount() - 1:
            self.action_view.clearSelection()
            self.action_view.item(row + 1, 0).setSelected(True)

    def select_previous_cell(self):
        row = self.get_current_row_of_selection()
        self.action_view.clearSelection()
        if row > 1:
            self.action_view.item(row - 1, 0).setSelected(True)

    def center_new_selection(self):
        row = self.get_current_row_of_selection()
        self.action_view.scrollToItem(
            self.action_view.item(row, 0),
            QtWidgets.QAbstractItemView.PositionAtCenter,
        )

    def keyPressEvent(self, e):
        current_action = self.get_current_action_from_highlight()
        if e.key() == QtCore.Qt.Key_F1:
            if current_action:
                self.jump_to_current_action(current_action)
                self.center_new_selection()
        elif e.key() == QtCore.Qt.Key_F2:
            if current_action:
                self.set_current_event_to_time(current_action)
                self.select_next_cell()
                self.center_new_selection()
        elif e.key() == QtCore.Qt.Key_F4:
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
        elif e.key() == QtCore.Qt.Key_Period:
            self.advance_frames(1)
        elif e.key() == QtCore.Qt.Key_Comma:
            self.advance_frames(-1)
        self.updateUI()

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

    def seconds_per_frame(self):
        """Seconds per frame"""
        return 1 / (self.mediaplayer.get_fps() or 25)

    def advance_frames(self, number):
        new_time = self.get_current_second_of_player() + (self.seconds_per_frame() * number)
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
            self.jump_next_action_timer.setInterval(2 * self.leadup_time * 1000)
        self.lineEdit.clear()

    def update_view_action_reel(self):
        self.concurent_action = self.action_reel_box.isChecked()
        if self.concurent_action:
            self.auto_jump = True
            self.jump_on_select_box.setChecked(True)

        if self.mediaplayer.is_playing() and self.concurent_action:
            self.jump_next_action_timer.start()
        else:
            self.jump_next_action_timer.stop()

    def update_jumping_to_action(self):
        self.auto_jump = self.jump_on_select_box.isChecked()
        if not self.auto_jump:
            self.concurent_action = False
            self.action_reel_box.setChecked(False)
        if self.mediaplayer.is_playing() and self.concurent_action:
            self.jump_next_action_timer.start()
        else:
            self.jump_next_action_timer.stop()

    def set_keypresses_to_custom_keypresses(self):
        self.pushButton.keyPressEvent = self.keyPressEvent
        self.pushButton_2.keyPressEvent = self.keyPressEvent
        self.load_button.keyPressEvent = self.keyPressEvent
        self.saveFile_button.keyPressEvent = self.keyPressEvent

        self.horizontalSlider.keyPressEvent = self.keyPressEvent
        self.action_view.keyPressEvent = self.keyPressEvent
        self.filter_table.keyPressEvent = self.keyPressEvent

        self.action_filter_button.keyPressEvent = self.keyPressEvent
        self.court_filter_button.keyPressEvent = self.keyPressEvent
        self.rally_button.keyPressEvent = self.keyPressEvent
        self.subaction_filter_button.keyPressEvent = self.keyPressEvent
        self.reset_time_button.keyPressEvent = self.keyPressEvent
        self.reset_button.keyPressEvent = self.keyPressEvent

        self.jump_on_select_box.keyPressEvent = self.keyPressEvent
        self.action_reel_box.keyPressEvent = self.keyPressEvent

        self.delete_action.keyPressEvent = self.keyPressEvent
        self.insert_action.keyPressEvent = self.keyPressEvent

        self.pushButton_3.keyPressEvent = self.keyPressEvent
        self.lcdNumber.keyPressEvent = self.keyPressEvent
        self.horizontalSlider_2.keyPressEvent = self.keyPressEvent
        self.hideactions.keyPressEvent = self.keyPressEvent

    def start_stop_timer(self):
        if self.timer_start is None:
            self.timer_start = self.get_current_second_of_player()
            self.pushButton_3.setText("Reset Timer")
            self.lcdNumber.show()
        else:
            self.timer_start = None
            self.pushButton_3.setText("Start Timer")
            self.lcdNumber.hide()
        pass

    def toggle_non_game_actions(self):
        self.hide_non_game_actions = self.hideactions.isChecked()
        self.apply_all_filters()

    def _qt_setup(self):
        self.pushButton.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.PlayPause)
        # we need to disconnect from the default load to connect to our custom load
        self.load_button.clicked.disconnect()
        self.load_button.clicked.connect(self.load_file)
        self.saveFile_button.clicked.connect(self.save_file)

        self.horizontalSlider.sliderMoved.connect(self.set_mediaplayer_from_sliderposition)
        self.action_view.cellClicked.connect(self.cell_was_clicked)
        self.action_view.itemSelectionChanged.connect(self.jump_to_current_cell)

        self.jump_on_select_box.clicked.connect(self.update_jumping_to_action)
        self.action_reel_box.clicked.connect(self.update_view_action_reel)

        self.reset_time_button.clicked.connect(self.set_leadup_time)
        self.insert_action.clicked.connect(self.insert_action_after)
        self.delete_action.clicked.connect(self.delete_current_action)

        self.pushButton_3.clicked.connect(self.start_stop_timer)
        self.lcdNumber.hide()

        self.horizontalSlider_2.sliderMoved.connect(self.set_volume)

        self.hideactions.clicked.connect(self.toggle_non_game_actions)

        self.set_keypresses_to_custom_keypresses()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())
