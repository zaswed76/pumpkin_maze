# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from pumpkin import paths


class ArrowButton(QtWidgets.QPushButton):
    def __init__(self, *__args, **kwargs):
        super().__init__(*__args)
        self.setCheckable(True)
        self.setFlat(True)
        size = QtCore.QSize(*kwargs['size_icon'])
        self.setFixedSize(size)
        self.setIconSize(size)


class Label(QtWidgets.QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)


class InputSide(QtWidgets.QFrame):
    ext_icon = '.png'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QtWidgets.QGridLayout(self)
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.size_icon = (32, 32)
        self.buttons_list = ['plus', 'top', None, 'left', 'door',
                             'right', None, 'bottom', 'minus']
        self.add_widgets()

    def add_widgets(self):
        n = 0
        for x in range(3):
            for y in range(3):
                button_name = self.buttons_list[n]
                if button_name is not None:
                    direct = str(self.size_icon[0])
                    pth = paths.icon_path(direct, button_name, self.ext_icon)
                    icon = QtGui.QIcon(pth)
                    self.grid.addWidget(ArrowButton(icon, "", size_icon=self.size_icon), x, y)
                n += 1


class Widget(QtWidgets.QFrame):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.resize(300, 200)
        self.setWindowTitle('Tiled gui lib')
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(1, 1, 1, 1)

    def set_widget(self, widget):
        self.box.addWidget(widget)


class PortalDialog(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.box = QtWidgets.QVBoxLayout(self)
        self.top_widget = QtWidgets.QFrame()
        self.side_widget = InputSide()
        self.box.addWidget(self.top_widget)
        self.box.addWidget(self.side_widget)
        self.parent = args[0]
        self.parent.setWindowTitle('Set Portal')

        self.check_portal = QtWidgets.QCheckBox()
        # откуда

        self.start_id = QtWidgets.QLineEdit()
        # куда
        self.finish_level = QtWidgets.QLineEdit()
        self.finish_id = QtWidgets.QLineEdit()

        self.form = QtWidgets.QFormLayout(self.top_widget)

        self.form.setSpacing(12)
        self.form.addRow(Label('Portal'), self.check_portal)
        # self.form.addRow(Label('ID входа'), self.start_id)

    def input_side(self):
        self.form.addRow(Label('вход слева'), self.start_id)
        self.form.addRow(Label('вход сверху'), self.start_id)
        self.form.addRow(Label('вход справа'), self.start_id)
        self.form.addRow(Label('вход сснизу'), self.start_id)


portal = PortalDialog


def show_portal_widget(x, tiled_map, group_name, widget):
    css_path = paths.css_path('gui_style.css')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(css_path, "r").read())
    main = Widget(None,
                  (QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint))
    main.set_widget(widget(main))
    main.show()

    # tiled_map.set_portal(group_name)
    app.exec_()
