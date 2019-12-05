#!/usr/bin/env python3

import PyQt5
import PyQt5.QtWidgets
import sys


#def sys_vals(Mp,ts):
#
#    return zeta,wn
#
#def place_poles(zeta, wn):
#
#    return s
#
#def for_the_gui(Mp,ts):
#
#    return k                            

class MainWindow(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        # Define menus
        #   defintes file menu
        self.menuFile = self.menuBar().addMenu("&Help")
        self.actionHelp = PyQt5.QtWidgets.QAction("&YouCanHelp", self)
        self.actionHelp.triggered.connect(self.Help)
        self.menuFile.addActions([self.actionHelp])
        
        # Define and set main widgets
        widget = PyQt5.QtWidgets.QWidget()
        self.mfh = PyQt5.QtWidgets.QLineEdit("Mass Flow Rate Hot [kg/s]")
        self.mfc = PyQt5.QtWidgets.QLineEdit("Mass Flow Rate Cold [kg/s]")
        self.length = PyQt5.QtWidgets.QLineEdit("Length of Heat Exchanger [m]")
        num=["Number of Heat Exchangers","1","2"]
        self.heatex = PyQt5.QtWidgets.QComboBox()
        self.heatex.addItems(num)
        self.output = PyQt5.QtWidgets.QLineEdit("Output")
        self.button = PyQt5.QtWidgets.QPushButton("Solve",self)
        self.button.clicked.connect(self.buttonEvent)

        widget.setFixedSize(400,225)
        layout = PyQt5.QtWidgets.QVBoxLayout()
        layout.addWidget(self.mfh)
        layout.addWidget(self.mfc)
        layout.addWidget(self.length)
        layout.addWidget(self.heatex)
        layout.addWidget(self.button)
        layout.addWidget(self.output)
        widget.setLayout(layout)  
        self.setCentralWidget(widget)
    
    #message displayed by Help    
    def Help(self):
        self.output.setText("You can help by giving us 100%")
        
    #When button is pushed call for_the_gui() to get kVals and return to self.output
    def buttonEvent(self):
        #ensures that the inputs are floats or ints
        try:
            #call funciton to Solve
            #display solution
            pass
        except (ValueError):
            self.output.setText("Overshoot and Settling Time must be floats or ints")


if __name__ == '__main__':
    #runs the gui
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()