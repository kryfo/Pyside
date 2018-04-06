# -*- coding: utf-8 -*-
import os
#command = 'taskkill /F /IM python.exe'
#os.system(command)

pid = 72084
os.popen('taskkill.exe /pid:'+str(pid))