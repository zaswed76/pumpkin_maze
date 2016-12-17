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
        self.setWindowTitle('Tiled gui lib')
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(1, 1, 1, 1)

    def set_widget(self, widget):
        self.box.addWidget(widget)

class PortalDialog(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = args[0]
        self.parent.setWindowTitle('Set Portal')

        self.check_portal = QtWidgets.QCheckBox()
        # откуда
        self.start_level = QtWidgets.QLineEdit()
        self.start_id = QtWidgets.QLineEdit()
        # куда
        self.finish_level = QtWidgets.QLineEdit()
        self.finish_id = QtWidgets.QLineEdit()

        self.form = QtWidgets.QFormLayout(self)

        self.form.setSpacing(12)
        self.form.addRow(Label('Portal'), self.check_portal)
        self.form.addRow(Label('Уровень входа'), self.start_level)
        self.form.addRow(Label('ID входа'), self.start_id)





portal = PortalDialog



def show_portal_widget(x, tiled_map, group_name, widget):
    css_path = paths.css_path('gui_style.css')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(css_path, "r").read())
    main = Widget(None, (QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint))
    main.set_widget(widget(main))
    main.show()

    # tiled_map.set_portal(group_name)
    app.exec_()