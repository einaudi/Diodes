#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QLCDNumber, QHBoxLayout

class DiodeInterface( QWidget ):

    def __init__( self, label, parentSerial=None, unit='V' ):

        super().__init__()

        self.a = 1
        self.b = 0

        self.serial = parentSerial

        self.initUI( label, unit )

    def init_widgets( self, label, unit ):

        self.label = QLabel( label )
        self.lcd   = QLCDNumber()
        self.lcd.setSegmentStyle( 2 )
        self.unit  = QLabel( unit )

    def init_layout( self ):

        layout = QHBoxLayout()

        layout.addWidget( self.label )
        layout.addWidget( self.lcd, 1 )
        layout.addWidget( self.unit )

        self.setLayout( layout )

    def initUI( self, label, unit ):

        self.init_widgets( label, unit )
        self.init_layout()

    def measure( self, id ):

        val = self.serial.query( 'M{:0}'.format(id) )
        self.lcd.display( val )
