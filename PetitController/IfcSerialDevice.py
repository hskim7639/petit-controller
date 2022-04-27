#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022 Hyo Sang Kim. All right reserved.
# This file is released under the "MIT License Agreement".
# Plase see the LICENSE file that should have been included as part of this package.
#

import sys
import serial  # pip install pyserial
from serial.tools import list_ports
import time


class IfcSerialDevice():
    LOG_NONE=0; LOG_ERR=1; LOG_WARN=2; LOG_INFO=3; LOG_DEBUG=4; LOG_DBGDBG=5
    def __init__(self):
        self.connected = False
        self.devName = None
        #self.ser = None
        self.ser = serial.Serial()
        self.baudrate = 115200
        self.timeout_ms = 50
        self.logLevel = self.LOG_INFO
        self._initProperties()
        
    def __del__(self):
        if self.isConnected():
            self.disconnect()
        
    def _initProperties(self):
        pass

    def log(self, level, msg):
        # reimplement this method in the derived class
        if (level<=self.logLevel):
            print('IfcSerialDevice: {}'.format(msg))

    def isConnected(self):
        return self.connected
    
    def connect(self,  devname,  **kwargs):
        if self.isConnected() == False:
            try:
                if devname==None and 'sn' in kwargs.keys():
                    devsn = kwargs.pop('sn')
                    devs = self.findPorts(sn=devsn)
                    if len(devs)==0:
                        raise Exception("No vaild device found.")
                    devname = devs[0]['device']

                if 'baudrate' in kwargs.keys() and isinstance(kwargs['baudrate'],  int):
                    self.baudrate = kwargs.pop('baudrate')
                #self.ser = serial.Serial(devname,  baudrate=self.baudrate,  **kwargs)
                self.ser.port = devname; self.ser.baudrate = self.baudrate; self.ser.setDTR(False)
                self.ser.open()
                self.setTimeoutMS(self.timeout_ms)
                self.connected = True
            except Exception as e:
                self.ser = None
                raise e
        
    def disconnect(self):
        if isinstance(self.ser, serial.Serial):
            self.ser.close()
            self.connected = False
        
    def read(self,  nread=1000):
        return self.ser.read(nread)

    def read_until(self, expected=b'\n', size=None):
        return self.ser.read_until(expected, size)
        
    def write(self,  data):
        if isinstance(data, str):
            data = bytes(data,  'utf-8')
        self.ser.write(data)
        
    def clear_read_buf(self):
        old = self.setTimeoutMS(0.1)
        dummy = self.read()
        self.setTimeoutMS(old)

    def setTimeoutMS(self,  ms):
        if isinstance(self.ser, serial.Serial):
            old = self.ser.timeout
            self.ser.timeout = 0.001*ms
            if old == None:
                old = self.getTimeoutMS()
            return old

    def getTimeoutMS(self):
        if isinstance(self.ser, serial.Serial):
            return (1000.0*self.ser.timeout)
            
    def msleep(self,  ms):
        time.sleep(0.001*ms)
    
    @staticmethod
    def findPorts(**kwargs):
        # search serial comm devices
        portlist = []
        #list_portinfo = serial.tools.list_ports.comports()
        list_portinfo = list_ports.comports()
        if len(list_portinfo)>0:
            for port in list_portinfo:
                portinfo = { 'device':port.device,  'name':port.name,  'vid':port.vid,  'pid':port.pid,  'sn':port.serial_number,  'hwid':port.hwid}
                if 'vid' in kwargs.keys() and kwargs['vid']!=portinfo['vid']:
                    continue
                if 'pid' in kwargs.keys() and kwargs['pid']!=portinfo['pid']:
                    continue
                if 'sn' in kwargs.keys() and kwargs['sn']!=portinfo['sn']:
                    continue
                    
                portlist.append(portinfo)
        return portlist
    

if __name__=='__main__':
    sn = '397F36753438'
    listofports = IfcSerialDevice.findPorts() # '8D70139C5656'
    print(listofports)
    
    if len(listofports)==0:
        print('No serial port found')
    else:
        ser = IfcSerialDevice()
        try:
            if type(sn)==type('') and len(sn)>0:
                ser.connect(None, sn=sn,  baudrate=115200)
            else:
                if sys.platform == 'win32':
                    devname = 'OOM3'
                else:
                    devname = '/dev/ttyACM0'
                ser.connect(devname,  baudrate=115200)
            print('comm port open')
            ser.msleep(50)
            ser.write(b'idn?\n')
            ser.msleep(100)
            xx = ser.read()
            print(xx)
            ser.msleep(10)
            ser.disconnect()
        except Exception as e:
            print(str(e))
    ##
    print('bye')
