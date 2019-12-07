#!/usr/bin/env python3

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction,QHBoxLayout, QTableWidget,QTableWidgetItem,QVBoxLayout,QLabel,QLineEdit,QComboBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

#        # Define menus
#        #   defintes file menu
#        self.menuFile = self.menuBar().addMenu("&Help")
#        self.actionHelp = PyQt5.QtWidgets.QAction("&YouCanHelp", self)
#        self.actionHelp.triggered.connect(self.Help)
#        self.menuFile.addActions([self.actionHelp])
        
        # Define and set main widgets
        widget = QWidget()
        self.mfhtext = QLabel("Hot  Stream  Mass Flow Rate :  ")
        self.mfh = QLineEdit("")
        self.mfhunits = QLabel("kg/s")
        self.mfctext = QLabel("Cold Stream  Mass Flow Rate : ")
        self.mfc = QLineEdit("")
        self.mfcunits = QLabel("kg/s")
        self.lentext = QLabel("Length of Heat Exchanger(s) :  ")
        self.length = QLineEdit("")
        self.lenunits = QLabel(" m  ")
        self.heatextext = QLabel("Number  of Heat Exchangers :")
        self.heatex = QComboBox()
        self.heatex.addItems(["1","2"])
        self.output = QLineEdit("Output")
        self.space = QLabel("")
        self.button = QPushButton("Solve",self)
        self.button.clicked.connect(self.buttonEvent)

       
        Hbox1 = QHBoxLayout()
        Hbox1.addWidget(self.mfhtext)
        Hbox1.addWidget(self.mfh)
        Hbox1.addWidget(self.mfhunits)
        
        Hbox2 = QHBoxLayout()
        Hbox2.addWidget(self.mfctext)
        Hbox2.addWidget(self.mfc)
        Hbox2.addWidget(self.mfcunits)
        
        Hbox3 = QHBoxLayout()
        Hbox3.addWidget(self.lentext)
        Hbox3.addWidget(self.length)
        Hbox3.addWidget(self.lenunits)
        
        Hbox4 = QHBoxLayout()
        Hbox4.addWidget(self.heatextext)
        Hbox4.addWidget(self.heatex)
        
        Hbox5 = QHBoxLayout()
        Hbox5.addWidget(self.space)
        Hbox5.addWidget(self.button)
        Hbox5.addWidget(self.space)
        
        widget.setFixedSize(400,225)
        layout = QVBoxLayout()
        
        layout.addLayout(Hbox1)
        layout.addLayout(Hbox2)
        layout.addLayout(Hbox3)
        layout.addLayout(Hbox4)
        layout.addWidget(self.space)
        layout.addLayout(Hbox5)
        layout.addWidget(self.button)
        layout.addWidget(self.output)
        widget.setLayout(layout)  
        self.setCentralWidget(widget)
        
        self.table = TableView(Contents, 1, 8)
    #message displayed by Help    
    def Help(self):
        self.output.setText("You can help by giving us 100%")
        
    #When button is pushed call for_the_gui() to get kVals and return to self.output
    def buttonEvent(self):
        #ensures that the inputs are floats or ints
        self.table.show()
        try:
            self.heatex
            TwoExchangers=bool(int(self.heatex.currentText()))
            
            #call funciton to Solve
            self.output.setText(str(TwoExchangers))
            #pass
        except (ValueError):
            self.output.setText("You didnt change everything")

mfr="10"
Red="10e6"
hcold="5"
hhot="6"
UA="what is this?"
rel1="fill this in"
rel2="fill this in"
rel3="fill this in"


Contents = {'Mass Flow Rate (kg/s)':[mfr],
    'Reynolds d': [Red],
    'h cold stream (W/m^2 K)':[hcold],
    'h hot stream (W/m^2 K)' :[hhot],
    'UA (Units)' : [UA],
    'relevant Info1' : [rel1],
    'relevant Info2' : [rel2],
    'relevant Info3' : [rel3]}
 
class TableView(QTableWidget):
    def __init__(self, Contents, *args):
        QTableWidget.__init__(self, *args)
        self.contents = Contents
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setFixedSize(1000,100)
        
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.contents.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.contents[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
 

        
        
    
    
if __name__ == '__main__':
    #runs the gui
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()