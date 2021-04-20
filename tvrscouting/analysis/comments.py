from PyQt5 import QtWidgets
from tvrscouting.uis.comments import Ui_Form as Comment_UI


class CommentView(QtWidgets.QWidget, Comment_UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)