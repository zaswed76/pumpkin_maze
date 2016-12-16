# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, QtCore

class WidgetPortal(QtWidgets.QWidget):
    def __init__(self, flags, *args, **kwargs):

        super().__init__(flags, *args, **kwargs)
        self.resize(500, 500)
        self.box = QtWidgets.QHBoxLayout(self)
        self.lab = QtWidgets.QLabel()
        self.box.addWidget(self.lab, alignment=QtCore.Qt.AlignCenter)

    def set_text(self, text):
        self.lab.setText(text)


def show_portal_widget(x, tiled_map, group_name):
    app = QtWidgets.QApplication(sys.argv)
    main = WidgetPortal(None, (QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint))
    main.show()
    main.set_text('{}'.format(x))
    tiled_map.set_portal(group_name)
    app.exec_()