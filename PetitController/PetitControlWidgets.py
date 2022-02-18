#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022 Hyo Sang Kim. All right reserved.
# This file is released under the "MIT License Agreement".
# Plase see the LICENSE file that should have been included as part of this package.
#

from PyQt5.QtCore import Qt,  QSize,  QRect,  QPoint,  QTimer
from PyQt5.QtGui import QPainter,  QBrush,  QColor,  QPen
from PyQt5.QtWidgets import QApplication,  QWidget,  QVBoxLayout,  QPlainTextEdit,  QPushButton

class LEDWidget(QWidget):
    ''' LED showing status: color, blink once, blink cont '''
    STAT_ON = 1; STAT_OFF = 0
    MODE_STATIC = 0; MODE_BLINK_SINGLE =1; MODE_BLINK_CONT = 2
    def __init__(self,  parent=None,  **kwargs):
        super().__init__(parent)
        self.status = self.STAT_OFF; self.mode = self.MODE_STATIC
        self._initProperties()
        if 'color' in kwargs.keys() and isinstance(kwargs['color'],  QColor):
            self.setColor(kwargs['color'])
        if 'size' in kwargs.keys() and isinstance(kwargs['size'],  QSize):
            sz = kwargs['size']; self.rect = QRect(0, 0,  sz.width(),  sz.height())
        if 'toolTip' in kwargs.keys():
            self.toolTip = kwargs['toolTip']
        if 'interval' in kwargs.keys() and isinstance(kwargs['interval'],  int):
            self.interval_ms = kwargs['interval']
            
        self._initUI()
        self.setFixedSize(self.rect.size())
        self.timer = QTimer(); self.timer.setInterval(self.interval_ms); self.timer.timeout.connect(self.onTimer)
        self.blink()
        
    def _initProperties(self):
        self.toolTip = 'Tool Tip'
        self.color = QColor('#FF0000'); self.penWidth = 2
        self.rect = QRect(0, 0, 24, 24)
        self.interval_ms = 500
        pass
        
    def _initUI(self):
        self.setToolTip(self.toolTip)
        pass
        
    def minimumSizeHint(self):
        return QSize(10, 10)
        
    def sizeHint(self):
        return QSize(20, 20)
        
    def resizeEvent(self,  event):
        sz = event.size(); w = sz.width(); h = sz.height()
        x = (w*10)//100; y = (h*10)//100; ew = (w*80)//100; eh = (h*80)//100
        self.rect = QRect(x, y,  ew,  eh)
        print('resize {},{}'.format(w, h))
    
    def paintEvent(self,  event):
        color = self.colors[self.status]
        painter = QPainter(self); 
        painter.setBrush(QBrush(color)); 
        pen = QPen(self.colors[1].lighter(170)); pen.setWidth(self.penWidth)
        painter.setPen(pen); 
        painter.drawEllipse(self.rect)
        
    def setColor(self,  color):
        # two different colors
        self.colors = [color.darker(),  color];  # [0]: off, [1]: on
        
    def _setLED(self,  bOn):
        # draw ..
        if bOn:
            self.status = self.STAT_ON
        else:
            self.status = self.STAT_OFF
        self.repaint()
        
    def onTimer(self):
        print("onTimer")
        if (self.mode==self.MODE_BLINK_CONT):
            self._setLED(self.status!=self.STAT_ON)
        elif (self.mode==self.MODE_BLINK_SINGLE):
            self._setLED(False)
        else: # static
            pass
        
    def blink(self,  **kwargs):
        blinkCont = False
        if ('cont' in  kwargs.keys()):
            blinkCont = kwargs['cont']
        self.timer.setSingleShot(not blinkCont)
        if (blinkCont==False):
            self.mode=self.MODE_BLINK_SINGLE
        else:
            self.mode=self.MODE_BLINK_CONT
        self._setLED(True)
        self.timer.start()
        
    def turnLED(self,  bOn):
        self.timer.stop() # timer off
        self.mode = self.MODE_STATIC
        self._setLED(bOn)
        if (bOn==False):
            pass
        else:
            pass
        

class LogWindow(QWidget):
    """
    A widget that displays log meassages
    """
    LogNone=0; LogErr=1;LogWarn=2;LogInfo=3;LogDebug=4;LogDbgDbg=5;
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.logLevel=self.LogInfo;
        self.logList = []; 
        self.initProperties()
        self.initUI()
        
    def initProperties(self):
        self.linecntmax = 200
        self.cnt = 0
        
    def initUI(self):
        vbox = QVBoxLayout(self)
        self.edit = QPlainTextEdit(); self.edit.setReadOnly(True); self.edit.setMaximumBlockCount(self.linecntmax )
        vbox.addWidget(self.edit)
        
    def clear(self):
        # clear meassage in the window
        self.edit.clear()

    def append(self,  logLevel,  msg):
        # append log messages
        if (logLevel<=self.logLevel):
            self.edit.appendPlainText(msg.strip())
            #print('cnt: {}'.format(self.edit.blockCount()))

    
        
if __name__=='__main__':
    qApp = QApplication([])
    if True:
        led = LEDWidget(None,  toolTip='Status',  color=QColor('#FF00FF'), interval=1000)
        led.setFixedSize(QSize(30, 30))
        led.blink(cont=True)
        led.show()
    if True:
        w = LogWindow()
        w.show()
        w.append(w.LogInfo, 'second')
    qApp.exec_()
    
        
        
