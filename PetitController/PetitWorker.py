#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022 Hyo Sang Kim. All right reserved.
# This file is released under the "MIT License Agreement".
# Plase see the LICENSE file that should have been included as part of this package.
#

# A PetitWorker is a worker based on QT's controller/worker multi-thread example.
# It has only basic methods for interacting with the controller.
# DO NOT modify this file, and create a derived class for future improvement

import time
import pdb # for debug
from PyQt5.QtCore import QCoreApplication,  QObject,  QMutex, QMutexLocker,  pyqtSignal
DEBUG_CODE=3

class PetitWorker(QObject):
    msg_to_controller = pyqtSignal([list])
    worker_started = pyqtSignal(); worker_finished = pyqtSignal()
    STAT_BUSY=(1<<0); STAT_ERR=(1<<31); STAT_IN_BETWEEN=(1<<2)
    LOG_ERR=1;LOG_WARN=2;LOG_INFO=3;LOG_DEBUG=4;LOG_DBGDBG=5
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.status = 0; self.timerCount = 0; self.globalAbortAsked = False
        self.mainMutex = QMutex()
        self._initProperties()
        
    def _initProperties(self):
        pass
        
    def _setBusy(self,  bBusy):
        
        if (bBusy):
            self.status |= self.STAT_BUSY
        else:
            self.status &= ~(self.STAT_BUSY)
            
    def isBusy(self):
        # note that the controller should NOT send any messages while isBusy()==True 
        self.mainMutex.lock()
        isbusy =  ( (self.status & self.STAT_BUSY )==self.STAT_BUSY )
        self.mainMutex.unlock()
        return isbusy
        
    def msleep(self,  ms):
        # sleep for ms milliseconds
        time.sleep(0.001*ms)
        
    def onMsgFromController(self,  msg):
        self.worker_started.emit()
        if DEBUG_CODE >=3:
            print('Worker.onMsgFromController(): {}'.format(msg))
        self.mainMutex.lock()
        self._setBusy(True)
        self.mainMutex.unlock()
        cmd, v = msg[:2]
        try:
            self._handleMessage(msg) # this method should raise an exception when it failed.z   1q[[[p
            self.msleep(50)
            #pdb.set_trace()
            if DEBUG_CODE >= 3:
                print('Worker._handleMessage() finished.')
            self.msg_to_controller.emit([cmd,  0,  'Success'])
        except Exception as e:
            print(e)
            self.msg_to_controller.emit(['Log',  -1,  str(e)])
            self.msleep(50)
            self.msg_to_controller.emit([cmd,  -1,  'Fail'])
        finally:
            self.mainMutex.lock()
            self._setBusy(False)
            self.mainMutex.unlock()
            self.worker_finished.emit()

    def _handleMessage(self,  msg):
        # reimplement this function in the derived class
        cmd, v = msg[:2]
        if v==1: # abort
            # Make sure NOT to send abort command when the worker is busy
            self.mainMutex.lock()
            self.globalAbortAsked = True
            self.mainMutex.unlock()
            return
        elif cmd.upper()=='ShortWorkA'.upper():
            # to do something
            self.msg_to_controller.emit(['Log',  0,  'Starting Short Work A process'])
            # do short work
            self.msleep(500)
            self.msleep(5) # small sleep before send the message below
            self.msg_to_controller.emit(['Log',  0,  'Short Work A process finished'])
            self.msleep(5)
        elif cmd.upper()=='LongWorkA'.upper():
            self.doLongWorkA(msg)
        else:
            raise Exception('Woker._handleMessage(): Unknown command {}'.format(cmd))
        self.mainMutex.lock()
        self.globalAbortAsked = False
        self.mainMutex.unlock()
        
    def onTimer(self):
        # reimplement this function in the derived class
        if self.isBusy():
            if DEBUG_CODE > 1:
                print('Worker.onTimer() exits w/o action')
            return
        # @todo: add more code in the derived class
        self.self.timerCount += 1
            
    
    def doLongWorkA(self,  msg):
        if DEBUG_CODE>=3:
            print('Worker.doLongWorkA() Msg: {}'.format(msg))
        cmd,  v =msg[:2]
        # do Long work
        abortAsked = False
        try:
            nn = 40; nstep = 10
            for i in range(1, nn+1):
                # check signal during long work
                QCoreApplication.processEvents()
                if self.globalAbortAsked:
                    abortAsked = True
                    break
                self.msleep(50)  # one short action
                if ( (i % nstep) == 0):
                    self.msg_to_controller.emit(['Log',  0,  'Long Work A count {}'.format(i)])
        
        except Exception as e:
            raise e
        finally:
            # do something before leaving this method
            # then finally report the result.
            self.msleep(10)
            if abortAsked:
                self.msg_to_controller.emit(['Log',  0,  '{} aborted.'.format(cmd)])
            else:
                self.msg_to_controller.emit(['Log',  0,  '{} is finalizing.'.format(cmd)])
            self.msleep(20)
            
        
            
            
