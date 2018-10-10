#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QLCDNumber, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QDialog

class DiodeInterface( QWidget ):

    def __init__( self, label, parentSerial=None, unit='V' ):

        super().__init__()

        self.a = 1
        self.b = 0
        self.label = label
        self.unit = unit

        self.serial = parentSerial

        self.initUI( label, unit )

    def init_widgets( self, label, unit ):

        self.labelWidget = QLabel( label )
        self.lcd   = QLCDNumber()
        self.lcd.setSegmentStyle( 2 )
        self.unitWidget  = QLabel( unit )

    def init_layout( self ):

        layout = QHBoxLayout()

        layout.addWidget( self.labelWidget )
        layout.addWidget( self.lcd, 1 )
        layout.addWidget( self.unitWidget )

        self.setLayout( layout )

    def initUI( self, label, unit ):

        self.init_widgets( label, unit )
        self.init_layout()

    def measure( self, id ):

        val = self.serial.query( 'M{:0}'.format(id) )
        self.lcd.display( self.a*val + self.b )

    def set_settings( self, a, b, label, unit ):

        self.a = a
        self.b = b
        self.label = label
        self.unit = unit

        self.labelWidget.setText( label )
        self.unitWidget.setText( unit )

class DiodeCalibration( QDialog ):

    def __init__( self, d ): # d - list with DiodeInterface instances

        super().__init__()

        self.d = d

        self.initUI()

    def init_widgets( self ):

        self.id    = QComboBox()
        self.id.insertItems( 0, [str(i) for i in range(len(self.d))] )
        self.label = QLineEdit( self.d[0].label )
        self.unit  = QLineEdit( self.d[0].unit )
        self.a     = QLineEdit( str(self.d[0].a) )
        self.b     = QLineEdit( str(self.d[0].b) )

        self.saveButton = QPushButton( 'Save' )

    def init_layout( self ):

        layout = QFormLayout()

        layout.addRow( 'Choose diode:', self.id )
        layout.addRow( 'Label:', self.label )
        layout.addRow( 'Unit:', self.unit )
        layout.addRow( 'a:', self.a )
        layout.addRow( 'b:', self.b )
        layout.addRow( self.saveButton )

        self.setLayout( layout )

    def initUI( self ):

        self.init_widgets()
        self.init_layout()

        self.saveButton.clicked.connect( self.save )
        self.id.currentIndexChanged.connect( self.update )

    def save( self ):

        i = int(self.id.currentText())
        self.d[i].set_settings( float(self.a.text()), float(self.b.text()), self.label.text(), self.unit.text() )

    def update( self ):

        i = int(self.id.currentText())
        self.label.setText( self.d[i].label )
        self.unit.setText( self.d[i].unit )
        self.a.setText( str(self.d[i].a) )
        self.b.setText( str(self.d[i].b) )
