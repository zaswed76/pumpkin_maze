# -*- coding: utf-8 -*-

import sys
import os
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from pumpkin import paths
import paths
from pumpkin.gui import guilib as gui
from pumpkin.gui.forms import output_point_form
from pumpkin.libs import mprint


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
        self.setMaximumWidth(600)
        self.setWindowTitle('Tiled gui lib')
        self.box = QtWidgets.QHBoxLayout(self)

        self.box.setContentsMargins(1, 1, 1, 1)

    def set_widget(self, widget):
        self.box.addWidget(widget)



class PortalDialog(QtWidgets.QFrame):
    def __init__(self, parent, level, gid, portal=None):
        """

        :param parent:
        :param level:
        :param gid: порядоковый номер
        :param portal: json конфиг
        """
        super().__init__()
        self.setWindowModality(True)
        self.parent = parent
        if portal is None:
            self.portal = {}
        else:
            self.portal = portal
        self.parent.setWindowTitle('Set Portal')
        self.init_ui()
        self.base_box.cancel_but.clicked.connect(self._close)
        self.base_box.ok_but.clicked.connect(self._press_ok)
        self.base_box.level_info.setText('Level - {}'.format(level))
        self.base_box.id_info.setText('Entry - {}'.format(gid))

        print("portal", self.portal)

    def _close(self):
        print('cancel')
        self.parent.close()

    def _press_ok(self):
        print('press_ok')
        self.parent.close()

    def init_ui(self):
        box = gui.Box(gui.Box.Horizontal, parent=self, margins=0,
                      spacing=0)
        self.base_box = gui.Form(self,
                                 paths.forms('portal_base_form.ui'))
        box.addWidget(self.base_box)

        self.side_widget = InputSide()
        self.base_box.input_box.addWidget(self.side_widget,
                                          alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                                          stretch=2)

        self.output_1 = gui.Form(None, paths.forms('output_point.ui'))

        self.base_box.output_box.addWidget(self.output_1,
                                           alignment=QtCore.Qt.AlignTop,
                                           stretch=2)



portal = PortalDialog


def show_portal_widget(widget, level, gid, portal=None):
    css_path = paths.css_path('gui_style.css')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(css_path, "r").read())
    main = Widget(None,
                  (QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint))
    dialog = widget(main, level, gid, portal=portal)
    main.set_widget(dialog)
    main.show()
    app.exec_()


