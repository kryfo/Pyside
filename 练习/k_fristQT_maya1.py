# -*- coding: utf-8 -*-
from PySide.QtCore import *
from PySide.QtGui import *

#创建mayaQT的窗口需要导入的
import maya.OpenMayaUI as omui
from shiboken import wrapInstance

#QTdesiner的路径
import sys
sys.path.append('E:/k/k_pyside/fproject')

import k_frist4
import shoudong_win

import time

class k_Cthread(QThread):

    k_processed = Signal(int)
    k_finished = Signal()

    def __init__(self,parent = None):
        super(k_Cthread, self).__init__(parent)


    def run (self):

        self.k_progress()


    def k_progress(self):

        parent = self.parent()


        parent.k_progressBar.setValue(0)
        parent.kmaxCount = parent.k_tabWidget.rowCount()
        parent.k_progressBar.setMinimum (0)
        parent.k_progressBar.setMaximum (parent.kmaxCount)

        parent.k_startT()


        for i in range(parent.kmaxCount):
            print 'haha'                       
            parent.k_tabWidget.removeRow(0)
            time.sleep(0.1)
            self.k_processed.emit(i +1)
        self.k_finished.emit()


class k_window(QWidget,k_frist4.Ui_k_widget):
    def __init__(self,parent=None):
        super(k_window,self).__init__()
        self.setupUi(self)


        self.setAcceptDrops(True)


        self.kextraThread = QThread()


        self.kthread = k_Cthread(self)


        self.kthread2 = k_Cthread()
        self.kthread2.moveToThread(self.kextraThread)
        

        self.k_Bopen.setDefault(True)
        go_button = QPushButton(u'手动添加')
        self.k_progressBar.setValue(0)


        self.k_wlayout.addWidget(go_button)
        

        go_button.clicked.connect(self.sd_win)
        self.k_button2.clicked.connect(self.cleartabItem)
        self.k_Bopen.clicked.connect(self.kop)
        self.k_Bclose.clicked.connect(self.kcl)


        krow=self.k_tabWidget.currentRow()



        cde = QFileSystemModel()
        cde.setRootPath(QDir.homePath())
        self.k_treeView.setModel(cde)

        self.k_tabWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.k_tabWidget.setColumnWidth(0,140)
        self.k_tabWidget.setColumnWidth(1,340)
        self.k_tabWidget.setColumnWidth(2,90)

        self.k_convert.clicked.connect(self.kthread.start)
        self.kthread.k_processed.connect(self.k_progressBar.setValue)
        self.kthread.k_finished.connect(self.k_finishedT)    


        self.k_progressBar.hide()



    def k_startT(self):
        self.k_progressBar.setValue(0)
        self.k_convert.setDisabled(True)

        self.k_progressBar.show()
        print  'starting k....thread'


    def k_finishedT(self):
        print  'finished k....thread'
        #self.btnCancel.setDisabled(True)
        self.k_convert.setEnabled(True)
        # self.extraThread.deleteLater()
        # self.worker.deleteLater()
        self.kextraThread.quit()
        self.k_progressBar.hide()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.cleartabItem()


    def sd_win(self):


        self.sdwin=shoudong_win()
        self.sdwin.exec_()

        k_ffname=self.sdwin.klinename.text()
        k_ffpath=self.sdwin.klinepath.text()
        k_ffsize=self.sdwin.klinesize.text()

        if k_ffname and k_ffpath:
            kItemname=QTableWidgetItem(k_ffname)
            kItempath=QTableWidgetItem(k_ffpath)
            kItemsize=QTableWidgetItem(str(k_ffsize))

            self.k_tabWidget.insertRow(0)
            self.k_tabWidget.setItem(0,0,kItemname)
            self.k_tabWidget.setItem(0,1,kItempath)
            self.k_tabWidget.setItem(0,2,kItemsize)


    def dragEnterEvent(self,event):
        event.acceptProposedAction()

    def dropEvent(self,event):
        #super(k_window,self).dropEvent(event)
        #print("file droping")
        mimeData = event.mimeData()
        files=[]
        for url in mimeData.urls():
            #print  url.toLocalFile()
            files.append(url.toLocalFile())
            
        
        self.k_getfile(files)



    def kop(self):
        k_files=QFileDialog.getOpenFileNames(self,caption=u'选择文件',\
        filter="Pyhon(*.py;*pyc);;TXT(*.txt)",options=0)

        self.k_getfile(k_files[0])


    def k_getfile(self,kfiles):
        for kfile in kfiles:
            fileInfo= QFileInfo(kfile)
            k_fname = fileInfo.fileName()
            k_fpath = fileInfo.path()
            k_fsize = fileInfo.size()
            ks = len(str(k_fsize))
            if ks > 9:
                k_fsize=k_fsize/1024./1024./1024.
                k_fsize = '{:.2f}G'.format(k_fsize)
            elif ks > 6:
                k_fsize=k_fsize/1024./1024.
                k_fsize = '{:.2f}M'.format(k_fsize)   
            elif ks > 3:
                k_fsize=k_fsize/1024.
                k_fsize = '{:.2f}k'.format(k_fsize)   
            else :
                k_fsize = '{:.2f}b'.format(k_fsize) 

            kItemname=QTableWidgetItem(k_fname)
            kItempath=QTableWidgetItem(k_fpath)
            kItemsize=QTableWidgetItem(str(k_fsize))

            self.k_tabWidget.insertRow(0)
            self.k_tabWidget.setItem(0,0,kItemname)
            self.k_tabWidget.setItem(0,1,kItempath)
            self.k_tabWidget.setItem(0,2,kItemsize)


    def cleartabItem(self):
        #self.k_tabWidget.clearContents()
        krow=self.k_tabWidget.currentRow()
        self.k_tabWidget.removeRow(krow)

    def kcl(self):
        #self.close()
        app.exit()



class shoudong_win(QDialog,shoudong_win.Ui_Dialog):
    def __init__(self,parent=None):
         super(shoudong_win,self).__init__()
         self.setupUi(self)
         self.setAcceptDrops(True)



#创建一个maya的PYQT mainWindow
mayaWin=omui.MQtUtil.mainWindow()
#将PYQT转换成PYSIDE
MayaQwin=wrapInstance(long(mayaWin),QWidget)

#实例化创建QMainWindow
Qmaya = QMainWindow(MayaQwin)


kwin = k_window()

#将kwin放入maya的实例化创建QMainWindow
Qmaya.setCentralWidget(kwin)

Qmaya.setMinimumSize(1100,800)

Qmaya.setWindowTitle(u'我是来做测试的')


Qmaya.show()





