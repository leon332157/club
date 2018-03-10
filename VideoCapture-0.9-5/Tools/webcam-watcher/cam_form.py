# Form implementation generated from reading ui file 'cam_form.ui'
#
# Created: Thu May 31 20:20:33 2001
#      by: The Python User Interface Compiler (pyuic)
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class Cam(QDialog):
    def __init__(self, parent=None, name=None, modal=0, fl=0):
        QDialog.__init__(self, parent, name, modal, fl)

        if name == None:
            self.setName('Cam')

        self.resize(124, 20)
        self.setCaption(self.tr('Cam'))
        vbox = QVBoxLayout(self)
        vbox.setSpacing(0)
        vbox.setMargin(0)

        self.PixmapLabel1 = QLabel(self, 'PixmapLabel1')
        vbox.addWidget(self.PixmapLabel1)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a, SIGNAL('lastWindowClosed()'), a, SLOT('quit()'))
    w = Cam()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
