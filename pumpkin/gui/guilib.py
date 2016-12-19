# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, uic

_box_margin = [1, 1, 1, 1]
_box_spacing = 1


class Form(QtWidgets.QFrame):
   def __init__(self, parent, form, *args, **kwargs):
      super().__init__(parent, *args, **kwargs)
      uic.loadUi(form, self)


class Box(QtWidgets.QBoxLayout):
    Horizontal = QtWidgets.QBoxLayout.LeftToRight
    Vertical = QtWidgets.QBoxLayout.TopToBottom

    def __init__(self, direction, *widgets, parent=None, margins=_box_margin, spacing=_box_spacing):
        """
        :param direction: Box._horizontal \ Box._vertical
        :param QWidget_parent: QWidget
        :param margin: поле вокруг
        :param spacing: интервал (шаг) между виджетами
        """
        super().__init__(direction, parent)
        if isinstance(margins, int): margins = [margins] * 4
        self.setDirection(direction)
        self.setContentsMargins(*margins)
        self.setSpacing(spacing)
        if widgets: self.addWidgets(widgets)

    def addWidgets(self, widgets):
        for w in widgets:
            self.addWidget(w)