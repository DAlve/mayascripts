'''
Created on Feb 20, 2017

@author: davea
'''
import sys
from Qt import QtCore, QtGui, QtWidgets
from maya import OpenMayaUI as omui
#from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

import dialog_ui
reload(dialog_ui)



try:
    from shiboken2 import wrapInstance
except:
    from shiboken import wrapInstance
    
    

def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QtWidgets.QWidget)

class dialog(QtWidgets.QWidget):
    
    def __init__(self):
        super(dialog, self).__init__()
        
        
        self.ui = dialog_ui.Ui_Form()
        self.ui.setupUi(self)
        
        # Parent widget under Maya main Window
        self.setParent(get_maya_window())
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        
        # set the object name
        self.setObjectName('Dialog_uniqueId')
        #self.setWindowTitle('Dialog')
        #self.setGeometry(50,50,250,150)
        self.setup_ui()
        
        
    
    def setup_ui(self):
        print 'We got here!'
        

def main():
    ui = dialog()
    ui.show()
    return ui

#print __file__
main()
