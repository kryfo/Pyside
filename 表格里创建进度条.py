#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import sys, time, random
from PySide import QtGui
from PySide import QtCore
 
DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
QProgressBar::chunk {
    background-color: lightblue;
    width: 10px;
    margin: 1px;
}
"""
 
COMPLETED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
QProgressBar::chunk {
    background-color: #CD96CD;
    width: 10px;
    margin: 1px;
}
"""
class XProgressBar(QtGui.QProgressBar):
    def __init__(self, parent = None):
        QtGui.QProgressBar.__init__(self, parent)
        #self.setStyleSheet(DEFAULT_STYLE)
        self.step = 0
 
    def setValue(self, value):
        QtGui.QProgressBar.setValue(self, value)
        if value == self.maximum():
            pass
            #self.setStyleSheet(COMPLETED_STYLE)
 
class DownloadThread(Thread):
    def __init__(self, job):
        Thread.__init__(self)
        self.job = job
 
    def run(self):
        global JOBS
        while self.job.BAR.step < 100 and self.job.stauts=='run':
            self.job.BAR.step += 1
            time.sleep(random.randint(0, 1))
            #time.sleep(.1)
        else:
            self.job.stauts=='done'
 
class O(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
 
# ID, RUL, Path, BAR, OPT
JOBS = [
    O({'ID':1, "URL":'http://1', "Path":"C:/", "BAR":None, "OPT":None, "_dt":None, "stauts":"stop", "threads":4, "dinfo":None}),
    O({'ID':2, "URL":'http://2', "Path":"C:/", "BAR":None, "OPT":None, "_dt":None, "stauts":"stop", "threads":4, "dinfo":None}),
    O({'ID':3, "URL":'http://3', "Path":"C:/", "BAR":None, "OPT":None, "_dt":None, "stauts":"stop", "threads":4, "dinfo":None}),
    O({'ID':4, "URL":'http://4', "Path":"C:/", "BAR":None, "OPT":None, "_dt":None, "stauts":"stop", "threads":4, "dinfo":None}),
]
 
class dInfo(QtCore.QThread):
    _bar = QtCore.Signal(object)
    def __init__(self, ui, job):
        QtCore.QThread.__init__(self)
        self.running = True
        self.job = job
        self._bar.connect(ui.update_bar_info)
        self.start()
 
    def run(self):
        global JOBS
        while self.running and self.job.BAR is not None and self.job.stauts=='run':
            self._bar.emit(self.job.BAR)
            self.sleep(random.randint(0, 1))
        else:
            self.terminate()
 
class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.threads = []
        self.initUI()
 
    def initUI(self):
        global JOBS
        lab = ['URL','Progress','Time Remaining','Cur Speed','Avg Speed','Path','Size', 'ProgressBar', 'Opt']

        self.dltable = QtGui.QTableWidget(len(JOBS), len(lab))
        self.dltable.setHorizontalHeaderLabels(lab)
        for i, d in enumerate(JOBS):
            print d
            self.dltable.setItem(i, 0, QtGui.QTableWidgetItem(d.URL))
            self.dltable.setItem(i, 1, QtGui.QTableWidgetItem(''))
            self.dltable.setItem(i, 2, QtGui.QTableWidgetItem(''))
            self.dltable.setItem(i, 3, QtGui.QTableWidgetItem(''))
            self.dltable.setItem(i, 4, QtGui.QTableWidgetItem(''))
            self.dltable.setItem(i, 5, QtGui.QTableWidgetItem(d.Path))
            self.dltable.setItem(i, 6, QtGui.QTableWidgetItem(''))
            bar = XProgressBar(self)
            d.BAR = bar
            self.dltable.setCellWidget(i, 7, bar)
            opt = QtGui.QPushButton('Opt', self)
            self.connect(opt, QtCore.SIGNAL('clicked()'), self.doAction)
            d.OPT = opt
            self.dltable.setCellWidget(i, 8, opt)
             
        self.button = QtGui.QPushButton('Start', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.doAllAction)
 
        layout = QtGui.QGridLayout()
        layout.addWidget(self.dltable, 0, 0)
        layout.addWidget(self.button, 1, 0)
        self.setLayout(layout)
        self.setWindowTitle('ProgressBar')
        self.setGeometry(300, 300, 950, 450)
 
    def update_bar_info(self, bar):
        if bar.step <= 100:
            bar.setValue(bar.step)
 
    def doAction(self):
        global JOBS
        _but = self.sender()
        for d in JOBS:
            if _but == d.OPT:
                self.create(d)
 
    def create(self, d, all=False):
        if d.stauts=='stop':
            _download = DownloadThread(d)
            d._dt = _download
            d.stauts = 'run'
            _download.start()
            d.OPT.setText('Stop')
            _dInfo = dInfo(self, d)
            self.threads.append(_dInfo)
            d.dinfo = _dInfo
        elif d.stauts == 'run':
            d.stauts = 'stop'
            # d.dinfo.stop()
            d.OPT.setText('Start')
 
    def initDownload(self):
        global JOBS
        for d in JOBS:
            if d._dt is None:
                self.create(d)
 
    def doAllAction(self):
        self.initDownload()
 
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u"关闭系统", u"确定关闭系统吗?",
                            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.dInfo.running = False
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.ignore()
 
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()