#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022 Hyo Sang Kim. All right reserved.
# This file is released under the "MIT License Agreement".
# Plase see the LICENSE file that should have been included as part of this package.
#

from PyQt5.QtWidgets import QApplication,  QWidget,  QLabel,  QVBoxLayout,  QHBoxLayout
from qwt import QwtPlot


class Graph2D(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self._initProperties()
        self._initUI()
        
    def _initProperties(self):
        pass
        
    def _initUI(self):
        vbox = QVBoxLayout(self)
        plot = QwtPlot()
        vbox.addWidget(plot)
        pass
        
        
        
        
        
        
if __name__=='__main__':
    qApp = QApplication([])
    w = Graph2D()
    w.show()
    qApp.exec_()
