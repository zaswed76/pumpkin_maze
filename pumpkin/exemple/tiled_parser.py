

import sys
from PyQt5 import QtWidgets

class Widget(QtWidgets.QLabel):
    def __init__(self, *__args):

        super().__init__(*__args)
        self.resize(500, 500)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())

