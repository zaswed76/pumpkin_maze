# -*- coding: utf-8 -*-



import sys
from PyQt5 import QtWidgets, uic
import paths
from pumpkin.gui import guilib as gui
from pumpkin.gui.forms import output_point_form





class Form(QtWidgets.QFrame):
   def __init__(self, parent, form, *args, **kwargs):
      super().__init__(parent, *args, **kwargs)
      uic.loadUi(form, self)







class Widget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        box = QtWidgets.QHBoxLayout(self)
        form = Form(self, paths.forms('output_point.ui'))
        form2 = Form(self, paths.forms('output2_point.ui'))
        form2.line.setText('222')

        box.addWidget(form)
        box.addWidget(form2)
        form.label.setText("@@@@@@@")

    def set_style(self, path):
        self.setStyleSheet(open(path, "r").read())




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open(paths.css_path('example_style.css'), "r").read())
    main = Widget()
    # main.set_style(paths.css_path('example_style.css'))
    main.show()
    sys.exit(app.exec_())
