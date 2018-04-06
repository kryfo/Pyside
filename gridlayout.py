#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from PySide import QtGui
import json

path='E:/work/7_0616_CheckNode/'
if not path in sys.path:
    sys.path.append(path)

jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')
checkBoxKeys=jsDir.keys()
checkBoxKeys.sort()

#print checkBoxKeys
k_preset=[]
for i in checkBoxKeys:
    k_presets=jsDir[i][5]
    #print k_presets 
    for preset in k_presets:
        if preset not in k_preset:
            k_preset.append(preset)
print k_preset 




class GridLayout(QtGui.QWidget):
    global k_preset
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('grid layout')
        '''
        names = ['Cls', 'Bck', '', 'Close', '7', '8', '9', '/',
                 '4', '5', '6', '*', '1', '2', '3',
                 '-', '0', '.', '=','+', '0', '.', '=','+', '0', '.', '=','+']
        '''
        krow=6
        kclo=4
        ksize=len(k_preset)
        kclosize=ksize/krow
        hass=ksize%krow
        if hass:
            kclosize=kclosize+1
        #print ksize
        #print kclosize
        grid= QtGui.QGridLayout()
        pos = [(x, y) for x in range(kclosize) for y in range(krow)]
        #print pos
        for i in range(len(k_preset)):
            button = QtGui.QPushButton(k_preset[i])

            try:
                grid.addWidget(button, pos[i][0], pos[i][1])
            except:
                pass
        self.setLayout(grid)
        
app = QtGui.QApplication(sys.argv)
box = GridLayout()
box.show()
sys.exit(app.exec_())