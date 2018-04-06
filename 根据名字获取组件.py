#!/usr/bin/python
# -*- coding: utf-8 -*-
#rom PySide.QtWidgets import *
from PySide.QtGui import * 
from PySide.QtCore import * 
import sys 
 
 
def clickHandle():
    #button = main.sender()
    #print(button.objectName())
     
    array = []
    array.append(QLineEdit)
    #print array
     #根据名字获取组件 {your parent widget}.findChild({name class}, {your name})
    obj = main.findChild(array[0],"edit_1")
    print(type(obj))
    print obj.objectName()
    obj.setText('aaaaaa')
    #print(isinstance(obj, QLineEdit))
    #print(isinstance(obj, array[0]))
     
    #print(main.findChild(array[0],"edit_1").text())
    
    #print(main.findChild(QLineEdit,"edit_1").text())
    #print(edit_1.text())
 
 
if __name__ == '__main__':                  
    app=QApplication(sys.argv) 
    main=QWidget() 
     
    latout = QHBoxLayout()
    main.setLayout(latout)
     
    but_1 = QPushButton('but_1')
    but_1.setObjectName('but_1')
    but_1.clicked.connect(clickHandle)
    but_2 = QPushButton('but_2')
    but_2.setObjectName('but_2')
    but_2.clicked.connect(clickHandle)
     
    edit_1 = QLineEdit()
    edit_1.setObjectName('edit_1')
     
    edit_2 = QLineEdit()
    edit_2.setObjectName('edit_2')
     
    #edit_3 = QLineEdit()
    #edit_3.setObjectName('edit_3')

    latout.addWidget(but_1)
    latout.addWidget(but_2)
     
    latout.addWidget(edit_1)
    latout.addWidget(edit_2)
    #latout.addWidget(edit_3)
     
    main.show() 
    app.exec_()