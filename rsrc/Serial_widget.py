#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import glob
import serial

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFormLayout, QComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


def converter( x ):

    return {
        'NONE' : serial.PARITY_NONE,
        'EVEN' : serial.PARITY_EVEN,
        'ODD'  : serial.PARITY_ODD,
        '1'    : serial.STOPBITS_ONE,
        '1.5'  : serial.STOPBITS_ONE_POINT_FIVE,
        '2'    : serial.STOPBITS_TWO,
    }.get( x, None )

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        return False

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Serial_com( serial.Serial ):

    def __init__( self ):

        super().__init__()

        self.port     = None
        self.baudrate = 9600
        self.bytesize = 8
        self.parity   = converter( 'NONE' )
        self.stopbits = converter( '1' )

    def connect( self, port=None ):

        self.port = port

        try:
            self.open()
            return True
        except serial.SerialException:
            return False

    def disconnect( self ):

        if self.is_open:
            try:
                self.close()
                return True
            except:
                return False
        else:
            return True

    def set_settings( self, baudrate, bytesize, parity, stopbits ):

        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity   = converter( parity )
        self.stopbits = converter( stopbits )

    def write_( self, data ): #data is string

        if self.is_open:
            try:
                self.write( str(data).encode() )
                time.sleep( 0.001 )
            except Exception as e:
                print( e )
                return False
            return True
        else:
            print( 'Port is not open' )
            return False

    def readline_( self ):

        if self.is_open:
            try:
                return self.readline()
            except:
                return False
        else:
            return False

    def query( self, data ):

        if self.write_( data ):
            return self.readline_()
        else:
            return False

class QSerial( QDialog ):

    # Initialisation
    def __init__( self ):

        super().__init__()
        self.rs = Serial_com()

        self.ports = serial_ports()

        self.initUI()

    def init_widgets( self ):

        self.portsCombo    = QComboBox()
        self.portsCombo.insertItems( 0, self.ports )
        self.baudrateCombo = QComboBox()
        self.baudrateCombo.insertItems( 0, ['9600'] )
        self.bytesizeCombo = QComboBox()
        self.bytesizeCombo.insertItems( 0, ['8', '7', '6', '5'] )
        self.parityCombo   = QComboBox()
        self.parityCombo.insertItems( 0, ['NONE', 'EVEN', 'ODD'] )
        self.stopbitsCombo = QComboBox()
        self.stopbitsCombo.insertItems( 0, ['1', '1.5', '2'] )

        self.connectButton    = QPushButton( 'Connect' )
        self.disconnectButton = QPushButton( 'Disconnect' )
        self.refreshButton    = QPushButton( 'Refresh' )

    def init_layout( self ):

        layout = QVBoxLayout()
        settings = QFormLayout()
        buttonsLayout = QHBoxLayout()

        settings.addRow( 'Ports:', self.portsCombo )
        settings.addRow( 'Baudrate:', self.baudrateCombo )
        settings.addRow( 'Bytesize:', self.bytesizeCombo )
        settings.addRow( 'Parity:', self.parityCombo )
        settings.addRow( 'Stopbits:', self.stopbitsCombo )

        buttonsLayout.addWidget( self.connectButton )
        buttonsLayout.addWidget( self.disconnectButton )
        buttonsLayout.addWidget( self.refreshButton )

        layout.addLayout( settings )
        layout.addLayout( buttonsLayout )
        self.setLayout( layout )

    def initUI( self ):

        self.init_widgets()
        self.init_layout()

        self.refreshButton.clicked.connect( self.refresh )
        self.connectButton.clicked.connect( self.connect )
        self.disconnectButton.clicked.connect( self.disconnect )

    # Actions
    def connect( self ):

        if self.rs.is_open:
            return True
        else:
            port = self.portsCombo.currentText()
            baudrate = int(self.baudrateCombo.currentText())
            bytesize = int(self.bytesizeCombo.currentText())
            parity = converter( self.parityCombo.currentText() )
            stopbits = converter( self.stopbitsCombo.currentText() )

            self.rs.set_settings( baudrate, bytesize, parity, stopbits )

            return self.rs.connect( port )

    def disconnect( self ):

        return self.rs.disconnect()

    def refresh( self ):

        self.ports = serial_ports()

        txt = self.ports.currentText()
        self.portsCombo.clear()
        self.portsCombo.insertItems( 0, self.ports )
        try:
            self.ports.comboBox.setCurrentText( txt )
        except:
            pass

    # Serial communication

    def write( self, data ):

        return self.rs.write( data )

    def readline( self ):

        return self.rs.readline()

    def query( self, data ):

        return self.rs.query( data )
