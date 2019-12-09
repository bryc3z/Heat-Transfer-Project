#!/usr/bin/env python3

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction,QHBoxLayout, QTableWidget,QTableWidgetItem,QVBoxLayout,QLabel,QLineEdit,QComboBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        # Define menus
        #   defintes file menu
        self.menuFile = self.menuBar().addMenu("&Help")
        self.actionHelp = PyQt5.QtWidgets.QAction("&YouCanHelp", self)
        self.actionHelp.triggered.connect(self.Help)
        self.menuFile.addActions([self.actionHelp])
        
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

        #create horizontal layouts 
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
        
        #Set size and vertical layouts (of horizontal ones)
        widget.setFixedSize(400,225)
        layout = QVBoxLayout()
        layout.addLayout(Hbox1)
        layout.addLayout(Hbox2)
        #layout.addLayout(Hbox3)
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
        #ensures that all inputs are valid before using them to call a function
        try:
            self.heatex
            TwoExchangers=bool(int(self.heatex.currentText())-1)
            float(self.mfh.text())
            float(self.mfc.text())
            self.output.setText(str(TwoExchangers))
            self.table.show()
            #pass
        except (ValueError):
            self.output.setText("Input Not Valid")
            

Thi = 365 # degrees kelvin
DIAh = 0.040 #m
#Properties of cold inlet
Tci = 285 # degrees kelvin
DIAco = 0.090 # m
DIAci = 0.060 #m

# OTher propeties
L = 80
#Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L = main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L)

mfr="-"
Red="-"
hcold="-"
hhot="-"
UA="-"
rel1="-"
rel2="-"
rel3="-"

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
 

        
        
    
            
#            
#"""
#Hey Bryce I'm just gonna dump the whole file here then once you get the variables figured out we can clean this up
#A few notes, I think we should re examine the equations/solution process with the group because it reaches its solution...
#after one solution which seems odd
#"""
#
#import numpy as np
#from iapws import IAPWS97
#
#
## These properties all need to be input via the GUI
##Properties of hot inlet
#Thi = 365 # degrees kelvin
#MDOTh = 10 # Kg / s
#DIAh = 0.040 #m
#
#
##Properties of cold inlet
#
#Tci = 285 # degrees kelvin
#MDOTc = 8 # Kg / s
#DIAco = 0.090 # m
#DIAci = 0.060 #m
#
## OTher propeties
#L = 80
#
#def ReyNumCalc(rho,vel,dia,mu): #Where rho is density, vel is mean velocity, dia is diameter of the thing and mu is viscosity
#    """
#    This function calculates the Reynolds number
#
#    """
#    return rho * vel * dia/ mu
#
#    
#    
#def OutletCalc(Thi, Tci, Tho, Tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L):
#    """
#    This function takes a bunch of inputs and outputs useful information
#    """
#    Ks = 237 #Thermal conductivity of the center pipe
#    DIAhyd = DIAco - DIAci #Hydraulic diameter
#    Thm = (Thi + Tho)/2 # Calculate average temp for hot water properties
#    Tcm = (Tco + Tci)/2 # ^^^ but for cold
#    print(Thm,Tcm)
#    PROPh = IAPWS97(T = Thm, x = 0) #Creates gets all the properties for the hot water
#    PROPc = IAPWS97(T = Tcm, x = 0) # ^^^ Same
#    
#    # The next two lines puts all the propeties into variables for ease of use
#    RHOh, MUh,Kh,CPh,PRh = PROPh.rho, PROPh.mu, PROPh.k, PROPh.cp, PROPh.Prandt
#    RHOc, MUc,Kc,CPc,PRc = PROPc.rho, PROPc.mu, PROPc.k, PROPc.cp, PROPc.Prandt
#    
#    #These two lines get the average velocity of the water in the pipes
#    VELc = MDOTc/(RHOc * np.pi/4 * (DIAco**2 - DIAci**2)) 
#    VELh = MDOTh/(RHOh * np.pi/4 * DIAh**2)
#    
#    
#    #Step 1
#    #Get the Reynold numbers for both flows
#    REYo = ReyNumCalc(RHOc,VELc, DIAhyd, MUc)
#    REYi = ReyNumCalc(RHOh,VELh,DIAh,MUh)
#    
#    #Step 2
#    #Get the Nusset numvers for both
#    NUi = 0.0243 * REYi**(4/5) * PRh**0.4
#    NUo = 0.0265 * REYo**(4/5) * PRc**0.5
#
#    #Step3
#    #Calculate h from the NU nums
#    Hh = Ks * NUi / DIAh
#    Hc = Ks * NUo / (DIAhyd)
#    
#    #Step 4
#    #First calculate all the areas
#    Ahyd = np.pi * (DIAhyd) * L #Hydraulic area
#    Ao = np.pi * DIAci * L
#    Ai = np.pi * DIAh * L
#    U = 1/Ai * (1/(Hc * Ao) + np.log(DIAco/DIAci)/(2*np.pi*Ks*L)+1/(Hh*Ahyd))**-1
#   
#    #Step 5
#    Cc = MDOTc * CPc
#    Ch = MDOTh * CPh
#    Cmin = Ch
#    Cmax = Cc
#    if Cc< Ch:
#        Cmin = Cc
#        Cmax = Ch
#    Cr = Cmin/Cmax
#    NTU = U * Ai / Cmin
#    eff = (1-np.exp(-NTU*(1-Cr)))/(1-Cr * np.exp(-NTU*(1-Cr)))
#    Qmax = Cmin * (Thi - Tci)
#    Tho = Thi - eff * Qmax / Ch
#    Tco = Tci + eff * Qmax / Cc
#    Q = eff * Qmax
#
#    return Tho, Tco, Q, REYo, REYi, U*Ai, Hh, Hc
#
#def main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L):
#    # Assume both outlet temperature are the average of the two inlet temps
#    tho = (Thi + Tci)/2
#    tco = tho
#    n = 10
#    i = 0
#    #Bunch of lists to store data
#    results = [("Tho", "Tco", "Q", "REYo", "REYi", "U*Ai", "Hh", "Hc")]
#
#    while i < n:
#       results.append(OutletCalc(Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L))
#       
#       tho = float(results[i+1][0])
#       tco = float(results[i+1][1])
#       
#       i += 1
#    return results
#Results = (main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L))
#print(Results)
    

if __name__ == '__main__':
    #runs the gui
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
