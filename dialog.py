'''
Created on Feb 20, 2017

@author: davea
'''
import sys
from Qt.QtCore import * 
from Qt.QtGui import *
from Qt.QtWidgets import *
from Qt import QtCore
from shiboken2 import wrapInstance

import dialog_ui
reload(dialog_ui)

from maya import OpenMayaUI as omui

try:
    from PySide2.QtUiTools import QUiLoader
except:
    from PySide.QtUiTools import QUiLoader
    
    
    
def get_maya_window():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    
    return mayaMainWindow

class dialog(QWidget):
    
    def __init__(self):
        super(dialog, self).__init__()
        
        # Parent widget under Maya main Window
        self.setParent(get_maya_window())
        self.setWindowFlags(Qt.Window)
        
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        # set the object name
        self.setObjectName('Dialog_uniqueId')
        #self.setWindowTitle('Dialog')
        #self.setGeometry(50,50,250,150)
        self.setup_ui()
        
    
    def setup_ui(self):
        
        print 'We got here!'
        self.ui = dialog_ui.Ui_Dialog()
        #print test.__file__
        self.ui.setupUi(self)
        

def main():
    ui = dialog()
    ui.show()
    return ui

print __file__
main()
