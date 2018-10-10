#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QMenu, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton

from rsrc.Serial_widget import QSerial
from rsrc.Qt_widgets import DiodeInterface, DiodeCalibration

class Diodes( QMainWindow ):

    # Initialisation
    def __init__( self ):

        super().__init__()

        self.d = list()

        self.initUI()

    def initUI( self ):

        self.init_widgets()
        self.init_layout()
        self.initMenu()

        self.setWindowTitle( 'Diodes readout' )
        self.show()

    def init_widgets( self ):

        self.serial = QSerial()

        for i in range(12):
            self.d.append( DiodeInterface( 'Diode {:0}'.format(i), self.serial ) )

        self.measureButton = QPushButton( 'Measure' )

        self.calibration = DiodeCalibration( self.d )

    def init_layout( self ):

        layout = QVBoxLayout()
        buttons = QHBoxLayout()

        grid = QGridLayout()
        grid.setVerticalSpacing( 0 )
        for i in range(3):
            for j in range(4):
                grid.addWidget( self.d[j+i*4], i, j )

        buttons.addStretch( 1 )
        buttons.addWidget( self.measureButton )

        layout.addLayout( grid )
        layout.addLayout( buttons )
        main_widget = QWidget( self )
        main_widget.setLayout( layout )
        self.setCentralWidget( main_widget )

    def initMenu( self ):

        menubar = self.menuBar()
        settMenu = menubar.addMenu( 'Settings' )

        connAct = QAction( 'Choose device', self )
        connAct.triggered.connect( self.serial.exec_ )

        calAct = QAction( 'Calibration', self )
        calAct.triggered.connect( self.calibration.exec_ )

        settMenu.addAction( connAct )
        settMenu.addAction( calAct )

    # Actions
    def close( self ):

        self.serial.disconnect()

if __name__ == '__main__':

    app = QApplication( sys.argv )
    ex = Diodes()
    sys.exit( app.exec_() )
