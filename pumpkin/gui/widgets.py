# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtWidgets, QtCore
from pumpkin import paths

class Label(QtWidgets.QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)

class Widget(QtWidgets.QFrame):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.resize(500, 500)
        self.box = QtWidgets.QHBoxLayout(self)

    def set_widget(self, widget):
        self.box.addWidget(widget)

class PortalDialog(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check = QtWidgets.QCheckBox()
        self.form = QtWidgets.QFormLayout(self)
        self.form.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.form.setSpacing(47)
        self.form.addRow(Label('Portal'), self.check)





portal = PortalDialog



def show_portal_widget(x, tiled_map, group_name, widget):
    css_path = paths.css_path('gui_style.css')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(css_path, "r").read())
    main = Widget(None, (QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint))
    main.set_widget(widget())
    main.show()

    # tiled_map.set_portal(group_name)
    app.exec_()