from  PyQt4 import  QtCore,QtGui
from  ui.ui_mapConvert import  Ui_mapConvertForm
import  os

CMD =  "imf_copy"
OPTION = "-vgfp"

class JobThread(QtCore.QThread):
    def __init__(self,parent = None):
        super(JobThread, self).__init__(parent)

    convertDoneSig = QtCore.pyqtSignal(int)


    def run (self):
        print ("start converting......")
        self.convert()

    def convert(self):
        parent = self.parent()
        tableWidget=parent.ui.tableWidget
        progressBar=parent.ui.progressBar

        self.convertDoneSig.connect(progressBar.setValue)

        maxCount = tableWidget.rowCount()
        progressBar.setMinimum(0)
        progressBar.setMaximum(maxCount)
        print("the maxcount",maxCount)

        while tableWidget.rowCount():
            fileName = tableWidget.item(0,0).text()
            location = tableWidget.item(0,1).text()

            inFile = location +"/"+fileName
            outFile = parent.ui.outLineEdit.text()+"\\"+fileName
            outFile = outFile.replace("\\","/")

            self.convertDoneSig.emit(maxCount-tableWidget.rowCount()+1)
            self.doConvert(inFile,outFile,fileName)
            tableWidget.removeRow(0)

            #QtCore.QThread.sleep(1)


    def doConvert(self,inFile,outFile,fileName):
        global CMD
        global OPTION
        parent = self.parent()

        if QtCore.QFile(inFile).exists():
            imageFormat = parent.ui.formatComboBox.currentText()

            cmd = parent.ui.cmdLineEdit.text()+"\\"+CMD
            cmd = cmd.replace("\\","/")

            arguments=[OPTION,inFile,outFile,imageFormat]

            process = QtCore.QProcess()
            process.start(cmd,arguments)
            process.waitForStarted()
            process.waitForFinished()

        else:
            print ("the file",inFile,"is not exist")

class MapConvert(QtGui.QWidget):
    def __init__(self,parent = None):
        super(MapConvert,self).__init__(parent)

        self.ui=Ui_mapConvertForm()
        self.ui.setupUi(self)

        self.setUpGui()

    def setUpGui(self):
        self.setMinimumWidth(840)
        self.setAcceptDrops(True)

        jobThread = JobThread(self)

        self.helpWidget = QtGui.QDialog()

        closeButton = self.ui.closeButton
        cmdButton = self.ui.cmdButton
        outButton = self.ui.outButton
        saveOptButton = self.ui.saveOptButton
        loadOptButton = self.ui.loadOptButton

        addFilesButton= self.ui.addFilesButton
        convertButton = self.ui.convertButton

        #checkBox = self.ui.checkBox
        tableWidget = self.ui.tableWidget
        progressBar = self.ui.progressBar
        helpButton = self.ui.helpButton

        closeButton.clicked.connect(self.close)
        cmdButton.clicked.connect(self.getCmdDir)
        outButton.clicked.connect(self.getOutDir)
        addFilesButton.clicked.connect(jobThread.start)
        helpButton.clicked.connect(self.help)

        saveOptButton.clicked.connect(self.saveOpt)
        loadOptButton.clicked.connect(self.loadOpt)

        #tableWidget.setAcceptDrops(True)
        tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tableWidget.setColumnWidth(0,250)
        tableWidget.setColumnWidth(1,450)
        tableWidget.setColumnWidth(2,100)

        progressBar.setValue(0)

    def getCmdDir(self):
        dir= QtGui.QfileDialog.getExistingDirectory(parent=self,caption='选择文件',directory=QtCore.QDir.currentPath(),filter='',options=QtGui.QFileDialog.ShowDirsOnly)
        cmdLineEdit = self.ui.cmdLineEdit
        cmdLineEdit.setText(dir)
        #print (dir)

    def getOutDir(self):
        dir= QtGui.QfileDialog.getExistingDirectory(parent=self,caption='选择文件',directory=QtCore.QDir.currentPath(),filter='',options=QtGui.QFileDialog.ShowDirsOnly)
        cmdLineEdit = self.ui.cmdLineEdit
        cmdLineEdit.setText(dir)

    def saveOpt(self):
        configFileName="convertOptFile.cfg"
        homePath = os.getenv("HOMEPATH")
        homeDrive = os.getenv("HOMEDRIVE")
        os.chdir(homeDrive+homePath)
        home = os.getcwd()

        with open (home +"\\"+configFileName,mode = "w") as configFile:
            configFile.write(self.ui.cmdLineEdit.text()+"\n")
            configFile.write(str(self.ui.formatComboxBox.currentIndex()))+"\n"
            configFile.write(self.ui.outLineEdit.text()+"\n")


        print(home)

    def loadOpt(self):
        configFileName = "convertOptFile.cfg"
        homePath = os.getenv("HOMEPATH")
        homeDrive = os.getenv("HOMEDRIVE")
        os.chdir(homeDrive+homePath)
        home = os.getcwd()

        with open (home +"\\"+configFileName,mode = "w") as configFile:
            cmdPath = configFile.readline()
            imageFormatIndex = int(configFile.readline().replace("\n",""))
            outPath = configFile.readline()

            self.ui.cmdLineEdit.setText(cmdPath)
            self.ui.formatComboxBox.setCurrentIndex(imageFormatIndex)
            self.ui.outLineEdit.setText(outPath)

    def addFiles(self):
        files= QtGui.QfileDialog.getOpenFileNames(parent=self,caption='选择文件',directory=QtCore.QDir.currentPath(),filter='',options=QtGui.QFileDialog.ReadOnly)

        self.addToTable(files)

    def dragEnterEvent(self,event):
        #print ("drag file entering")
        event.acceptProposedAction()

    def dropEvent(self,event):
        super(MapConvert,self).dropEvent(event)
        #print("file droping")
        mimeData = event.mimeData()

        if mimeData.hasUrls():
            files = []
            for url in mimeData.urls():
                files.append(url.toLocalFile())

            self.addToTable(files)

    def addToTable(self,files):
        tableWidget = self.ui.tableWidget

        for file in files:
            fileInfo=QtCore.QFileInfo(file)

            name = fileInfo.compleBaseName() +"."+fileInfo.suffix()
            path = fileInfo.absolutePath()
            size = "{:.3f}M".format(fileInfo.size()/1024/1024)

            nameItem=QtGui.QTabWidgetItem(name)
            pathItem=QtGui.QTabWidgetItem(path)
            sizeItem=QtGui.QTabWidgetItem(str(size)+"M")

            tableWidget.insertRow(0)
            tableWidget.setItem(0,0,nameItem)
            tableWidget.setItem(0,1,pathItem)
            tableWidget.setItem(0,2,sizeItem)





    def help(self):
        helpText = "balabalabalbalb"
        helpLable = QtGui.QLabel(helpText)

        helpLayout = QtGui.QHBoxLayout()
        helpLayout.addWidget(helpLabel)

        self.helpWidget.setLayout(helpLayout)

        self.helpWidget.setFixedSize(400,200)
        self.helpWidget.setWindowTitle("help")

        print (helpText)

        self.helpWidget.show()

if __name__ == "__main__":
    import  sys

    app = QtGui.QApplication(sys.argv)

    mapConvert = MapConvert()
    mapConvert.show()

    app.exec_()







