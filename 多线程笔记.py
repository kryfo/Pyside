from PySide.QtCore import *
from PySide.QtGui import *
import os, time, platform, sys
class main(QDialog):
    def __init__(self, parent = None):
        super(main, self).__init__(parent)
        self.resize(300, 100)
        self.setMinimumSize(QSize(300, 100))
        self.setMaximumSize(QSize(300, 100))
        self.setWindowTitle("Test")
        self.buttonStart = QPushButton("Start")
        self.progressBar = QProgressBar()
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.buttonStart, 0, 1, 1, 1)
        self.connect(self.buttonStart, SIGNAL("clicked()"), self.startProgress)

        self.genericThread = GenericThread(self.test)
    def startProgress(self):
        self.genericThread.start()
    def test(self):
        print "started"
        for i in range(101):
            time.sleep(0.1)
            print i
            self.progressBar.setValue(i)
        print "done"
class GenericThread(QThread):
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def run(self):
        self.function(*self.args,**self.kwargs)
        return
app = QApplication(sys.argv)
start = main()
start.show()
app.exec_()