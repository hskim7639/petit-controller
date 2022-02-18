#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022 Hyo Sang Kim. All right reserved.
# This file is released under the "MIT License Agreement".
# Plase see the LICENSE file that should have been included as part of this package.
#

# This code is based on the QThread example code that demonstrates controller/worker model
# DO NOT modify this file and '.py'. Instead, create derived classes.



import sys
# import qt modules
from PyQt5.QtCore import Qt,  QThread,  pyqtSignal,  QTimer
#from PyQt5.QtGui import QApplication
from PyQt5.QtWidgets import QApplication,  QMainWindow,  QWidget,  QLabel,  QTextEdit,  QVBoxLayout,  QHBoxLayout, \
        QPushButton,  QMessageBox
from  PetitWorker import *
from PetitControlWidgets import *

DEBUG_CODE=2 # 0 for normal operation

class PetitControlWindow(QMainWindow):
    """
    An example of  control window class based on the QThread "controller-worker" model 
    """
    msg_to_worker = pyqtSignal([list]) 
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer); self.timer.setInterval(500); self.timer.setSingleShot(True);
        self._initProperties()
        self._initUI() # reimplement
        self.timer.start()
        
    def __del__(self):
        self.workerThread.quit()
        self.workerThread.wait()
        
    def _initProperties(self,  **kwargs):
        # reimplement this function in the derived class
        # DO NOT call this method from the derived calss
        worker = PetitWorker() 
        self._initWorker(worker)
        
    def _initWorker(self,  worker):
        # setup worker thread
        self.worker = worker
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        # connect signals
        self.msg_to_worker.connect(self.worker.onMsgFromController)
        self.worker.msg_to_controller.connect(self.onMsgFromWorker)
        self.worker.worker_started.connect(self.onWorkerStarted)
        self.worker.worker_finished.connect(self.onWorkerFinished)
        
        # start worker thread
        self.workerThread.start()
        
    def _initUI(self,  **kwargs):
        # The code below is just an example. Reimplement this in the derived class
        mainWidget = QWidget(self)
        vbox = QVBoxLayout(mainWidget)
        # Short work
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('Short work:'))
        self.btnShortWorkA = QPushButton('Short Work')
        hbox1.addWidget( self.btnShortWorkA)
        vbox.addLayout(hbox1)
        # Work work
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel('Long work:'))
        self.btnLongWorkA = QPushButton('Long Work'); hbox2.addWidget( self.btnLongWorkA)
        self.btnLongWorkACancel = QPushButton('Abort'); hbox2.addWidget( self.btnLongWorkACancel)
        vbox.addLayout(hbox2)
        
        # log window
        self.logWin = LogWindow()
        vbox.addWidget(self.logWin)
        self.setCentralWidget(mainWidget)
        
        self.setWindowTitle('MainController')
        
        # connect signals
        self.btnShortWorkA.pressed.connect(self.onButtonShortWorkAClicked)
        self.btnLongWorkA.pressed.connect(self.onButtonLongWorkAClicked)
        self.btnLongWorkACancel.pressed.connect(self.onButtonLongWorkACancelClicked)
        
    def closeEvent(self,  event):
        # handle closeEvent (probably) caused when X button is closed.
        if DEBUG_CODE<=0:
            btn = QMessageBox.question(self, 'Quit', 'Do you want to close the application?')
            if btn != QMessageBox.Ok:
                return
        super().closeEvent(event)

    def onButtonShortWorkAClicked(self):
        # Send a message to the worker
        self.msg_to_worker.emit(['ShortWorkA',  0,  'Start'])
        
    def onButtonLongWorkAClicked(self):
        self.msg_to_worker.emit(['LongWorkA',  0,  'Start'])
        
    def onButtonLongWorkACancelClicked(self):
        if self.worker.isBusy()==True:
            self.msg_to_worker.emit(['LongWorkA',  1,  'Abort'])
        
    def onMsgFromWorker(self,  msg):
        if DEBUG_CODE>=2:
            print('onMsgFromWorker {}'.format(msg))
        self._handleMsgFromWorker(msg)
        

    def _handleMsgFromWorker(self,  msg):
        # reimplement this function in the derived class
        cmd,  v = msg[:2]
        cmd = cmd.upper()
        if False:
            pass
        elif cmd=='LOG':
            self.log(v, msg[2])
        else:
            # invalid msg
            print(msg)
            
    def onWorkerStarted(self):
        # reimplement this function in the derive class
        pass
        
    def onWorkerFinished(self):
        # reimplement this function in the derive class
        pass
        
    def onTimer(self):
        # reimplement this function in the derive class
        self.log(self.logWin.LogInfo, 'Hello.')
        pass
        
    def log(self,  level,  msg):
        self.logWin.append(level,  msg)
        
        
if __name__=='__main__':
    app = QApplication([])
    w = PetitControlWindow()
    w.show()
    sys.exit(app.exec_())
