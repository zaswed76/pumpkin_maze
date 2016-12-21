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
    def __init__(self, parent, level, gid, included_levels,
                 portal=None):
        """

        :param parent:
        :param level:
        :param gid: порядоковый номер
        :param portal: json конфиг
        """
        super().__init__()
        self.included_levels = included_levels
        self.gid = gid
        self.level = level
        self.setWindowModality(True)
        self.parent = parent
        if portal is None:
            self.portal = {}
        else:
            self.portal = portal
        self.parent.setWindowTitle('Set Portal')
        self.__init_settings()
        self.__init_ui()
        self.__init_options()
        self.__init_actions()



        print("portal", self.portal)

    def __init_options(self):
        self.base_box.level_info.setText('Level - {}'.format(self.level))
        self.base_box.id_info.setText('Entry - {}'.format(self.gid))
        self.output_forms[self.out_form_count].comboBox.addItems(self.included_levels)

    def __init_settings(self):
        self.out_form_count = 0

    def __init_actions(self):
        self.base_box.cancel_but.clicked.connect(self._close)
        self.base_box.ok_but.clicked.connect(self._press_ok)
        self.base_box.add_out.clicked.connect(self._press_add_out)
        self.base_box.del_out.clicked.connect(self._press_del_out)

    def _press_add_out(self):
        self.out_form_count += 1
        self.output_forms[self.out_form_count] = gui.Form(None, paths.forms(
            'output_point.ui'))
        self.base_box.output_box.addWidget(self.output_forms[self.out_form_count],
                                           alignment=QtCore.Qt.AlignTop,
                                           stretch=2)
        self.output_forms[self.out_form_count].comboBox.addItems(self.included_levels)

        print('_press_add_out')

    def _press_del_out(self):
        if self.out_form_count > 0:
            self.output_forms[self.out_form_count].deleteLater()
            self.base_box.output_box.removeWidget(self.output_forms[self.out_form_count])
            self.out_form_count -= 1

        # while self.base_box.count() > 0:
        # item = self.base_box.itemAt(1)
           # if not item:
           # continue
           # w = item.widget()
           # print(w)
           # if w:
           #     w.deleteLater()

    def _close(self):
        print('cancel')
        self.parent.close()

    def _press_ok(self):
        print('press_ok')
        self.parent.close()

    def __init_ui(self):
        box = gui.Box(gui.Box.Horizontal, parent=self, margins=0,
                      spacing=0)
        self.base_box = gui.Form(self,
                                 paths.forms('portal_base_form.ui'))
        box.addWidget(self.base_box)

        self.side_widget = InputSide()
        self.base_box.input_box.addWidget(self.side_widget,
                                          alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                                          stretch=2)
        self.output_forms = {}
        self.output_forms[self.out_form_count] = gui.Form(None, paths.forms(
            'output_point.ui'))

        self.base_box.output_box.addWidget(
            self.output_forms[self.out_form_count],
            alignment=QtCore.Qt.AlignTop,
            stretch=2)

    def itemAt(self):
        pass

portal = PortalDialog


def show_portal_widget(widget, level, gid, included_levels,
                       portal=None):
    css_path = paths.css_path('gui_style.css')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(css_path, "r").read())
    main = Widget(None,
                  (QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint))
    dialog = widget(main, level, gid, included_levels, portal=portal)
    main.set_widget(dialog)
    main.show()
    app.exec_()
    print(main)
