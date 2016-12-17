# -*- coding: utf-8 -*-

import sys
import os
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui
from pumpkin import paths


class ArrowButton(QtWidgets.QPushButton):
    def __init__(self, *__args, **kwargs):
        super().__init__(*__args)
        self.setCheckable(True)
        self.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)


class Label(QtWidgets.QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)


class InputSide(QtWidgets.QFrame):
    ext_icon = '.png'
    size_reduction = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(Label('Input sides'))
        self.grid = QtWidgets.QGridLayout()
        self.box.addLayout(self.grid)

        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.size_icon = (32, 32)
        self.buttons_list = ['plus', 'top', None, 'left', 'door',
                             'right', None, 'bottom', 'minus']
        self.buttons = {}
        self.add_widgets()
        size = self.size_icon[0] * 3 + (4 * 13)
        self.setFixedSize(size, size)

    def add_widgets(self):
        n = 0
        for x in range(3):
            for y in range(3):
                button_name = self.buttons_list[n]
                if button_name is not None:
                    self.buttons[button_name] = ArrowButton()
                    self.buttons[button_name].clicked.connect(
                        partial(self.button_press, button_name))
                    self.buttons[button_name].setObjectName(
                        button_name)
                    size = QtCore.QSize(*self.size_icon)
                    self.buttons[button_name].setFixedSize(size)
                    self.buttons[button_name].setIconSize(size)
                    self.grid.addWidget(self.buttons[button_name], x,
                                        y)
                n += 1
        mini_size = self.size_icon[0] - self.size_reduction
        qsize = QtCore.QSize(mini_size, mini_size)
        self.buttons['plus'].setFixedSize(qsize)
        self.buttons['minus'].setFixedSize(qsize)
        self.buttons['plus'].setIconSize(qsize)
        self.buttons['minus'].setIconSize(qsize)

    def button_press(self, name):
        print('button_press', name)


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
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.top_widget = QtWidgets.QFrame()
        self.side_widget = InputSide()
        self.box.addWidget(self.top_widget)
        self.box.addWidget(self.side_widget)
        self.parent = args[0]
        self.parent.setWindowTitle('Set Portal')

        self.check_portal = QtWidgets.QCheckBox()
        self.check_portal.setFixedSize(32, 32)
        # откуда

        self.start_id = QtWidgets.QLineEdit()
        # куда
        self.finish_level = QtWidgets.QLineEdit()
        self.finish_id = QtWidgets.QLineEdit()

        self.form = QtWidgets.QFormLayout(self.top_widget)

        self.form.setSpacing(20)
        label_portal = Label('Portal')
        label_portal.setMinimumWidth(40)
        self.form.addRow(label_portal, self.check_portal)
        # self.form.addRow(Label('ID входа'), self.start_id)




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
