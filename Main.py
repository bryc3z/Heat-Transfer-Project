#!/usr/bin/env python3

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction,QHBoxLayout, QTableWidget,QTableWidgetItem,QVBoxLayout,QLabel,QLineEdit,QComboBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys

import numpy as np
from iapws import IAPWS97
import csv
import matplotlib.pyplot as plt

#The following GUI code is by Bryce Zimmerman

#Impliment GUI
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
        self.Dhitext = QLabel("Hot  Tube  Inner  Diameter    :  ")
        self.Dhi = QLineEdit("40")
        self.Dhiunits = QLabel("mm")
        self.Dhotext = QLabel("Hot  Tube  Outer  Diameter   :  ")
        self.Dho = QLineEdit("60")
        self.Dhounits = QLabel("mm")
        self.Dctext = QLabel("Cold  Tube  Diameter             : ")
        self.Dc = QLineEdit("90")
        self.Dcunits = QLabel("mm")
        self.lentext = QLabel("Heat Exchanger Total Length : ")
        self.length = QLineEdit("80")
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
        Hbox4.addWidget(self.Dhitext)
        Hbox4.addWidget(self.Dhi)
        Hbox4.addWidget(self.Dhiunits)
        
        Hbox5 = QHBoxLayout()
        Hbox5.addWidget(self.Dhotext)
        Hbox5.addWidget(self.Dho)
        Hbox5.addWidget(self.Dhounits)
        
        Hbox6 = QHBoxLayout()
        Hbox6.addWidget(self.Dctext)
        Hbox6.addWidget(self.Dc)
        Hbox6.addWidget(self.Dcunits)
        
        Hbox7 = QHBoxLayout()
        Hbox7.addWidget(self.heatextext)
        Hbox7.addWidget(self.heatex)
        
        Hbox8 = QHBoxLayout()
        Hbox8.addWidget(self.space)
        Hbox8.addWidget(self.button)
        Hbox8.addWidget(self.space)
        
        #Set size and vertical layouts (of horizontal ones)
        widget.setFixedSize(400,325)
        layout = QVBoxLayout()
        layout.addLayout(Hbox1)
        layout.addLayout(Hbox2)
        layout.addLayout(Hbox4)
        layout.addLayout(Hbox5)
        layout.addLayout(Hbox6)
        layout.addLayout(Hbox3)
        layout.addLayout(Hbox7)
        layout.addWidget(self.space)
        layout.addLayout(Hbox8)
        layout.addWidget(self.button)
        layout.addWidget(self.output)
        widget.setLayout(layout)  
        self.setCentralWidget(widget)
        
    #message displayed by Help    
    def Help(self):
        self.output.setText("You can help by giving us 100%")
        
    #When button is pushed call for_the_gui() to get kVals and return to self.output
    def buttonEvent(self):        
        #ensures that all inputs are valid before using them to call a function
        try:
            self.heatex
            #getting values from text boxes
            TwoExchangers=bool(int(self.heatex.currentText())-1)
            mfh=float(self.mfh.text())
            mfc=float(self.mfc.text())
            DIAh=float(self.Dhi.text())/1000
            DIAco=float(self.Dc.text())/1000
            DIAci=float(self.Dho.text())/1000
            L=float(self.length.text())
            Contents = contents(mfh,mfc, DIAh, DIAco, DIAci, L, TwoExchangers)
            self.table = TableView(Contents, 1, 11)
            self.output.setText("Valid Input")  
            self.table.show()
            #pass
        except (ValueError):
            self.output.setText("Input Not Valid")
            
def contents(MDOTh, MDOTc, DIAh, DIAco, DIAci, L, T):
    #Default
    Thi = 365 # degrees kelvin
    Tci = 285 # degrees kelvin
    
    #if there are 2 exchangers
    if T:
        Tho, Tco, Q, REYo, REYi, UA, Hh, Hc, NUi, NUo = main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc/2,MDOTh/2,L/2,10)[-1]
        MDOTh=MDOTh/2
    #if there is only 1 echanger
    else:
        Tho, Tco, Q, REYo, REYi, UA, Hh, Hc, NUi, NUo = main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L,10)[-1]
    #set contents and round correctly
    Contents = {'Temp of hot flow out (K)' : [str(round(Tho,3))],
                'Temp of cold flow out (K)' : [str(round(Tco,3))],
                'Total Heat Transfer (KW)' : [str(round(Q,3))],
                'Reynolds out': [str(round(REYo,3))],
                'Reynolds in': [str(round(REYi,3))],
                '   UA  ' : [str(round(UA,3))],
                'h of cold stream (W/m2 K)':[str(round(Hc,3))],
                'h of hot stream (W/m2 K)' :[str(round(Hh,3))],
                '  NUi  ' : [str(round(NUi,3))],
                '  NUo  ' : [str(round(NUo,3))],
                'Mass Flow Rate (kg/s)':[str(round(MDOTh,3))]}
    return Contents

#table class
class TableView(QTableWidget):
    def __init__(self, Contents, *args):
        QTableWidget.__init__(self, *args)
        self.contents = Contents
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setFixedSize(1500,60)
        
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.contents.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.contents[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


'''
Following are the functions doing the actual calculation created by Caleb Huss
'''
def ffact(Rey):
    return (0.790* np.log(Rey) - 1.64)**-2
def NumCalcs(rho,vel,dia,mu,Pr): #Where rho is density, vel is mean velocity, dia is diameter of the thing and mu is viscosity
    """
    This function calculates the Reynolds number

    """
    rey = rho * vel * dia/ mu
    f = ffact(rey)
    nu = ((f/8)*(rey - 1000) * Pr)/(1 + 12.7 * (f/8)**2 * (Pr**(2/3)-1))   
    return rey, nu

    
    
def OutletCalc(Thi, Tci, Tho, Tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L):
    """
    This function takes a bunch of inputs and outputs useful information
    """
    Ks = 237 #Thermal conductivity of the center pipe
    DIAhyd = DIAco - DIAci #Hydraulic diameter
    Thm = (Thi + Tho)/2 # Calculate average temp for hot water properties
    Tcm = (Tco + Tci)/2 # ^^^ but for cold

    PROPh = IAPWS97(T = Thm, x = 0) #Creates gets all the properties for the hot water
    PROPc = IAPWS97(T = Tcm, x = 0) # ^^^ Same
    
    # The next two lines puts all the propeties into variables for ease of use
    RHOh, MUh,Kh,CPh,PRh = PROPh.rho, PROPh.mu, PROPh.k, PROPh.cp, PROPh.Prandt
    RHOc, MUc,Kc,CPc,PRc = PROPc.rho, PROPc.mu, PROPc.k, PROPc.cp, PROPc.Prandt
    
    #These two lines get the average velocity of the water in the pipes
    VELc = MDOTc/(RHOc * np.pi/4 * (DIAco**2 - DIAci**2)) 
    VELh = MDOTh/(RHOh * np.pi/4 * DIAh**2)
    
    
    #Step 1
    #Get the Reynold numbers for both flows

    #Step 2
    #Get the Nusset numbers for both
    REYi, NUi = NumCalcs(RHOh,VELh,DIAh,MUh,PRh)
    REYo, NUo = NumCalcs(RHOc,VELc,DIAhyd,MUc,PRc)
        
    #Step3
    #Calculate h from the NU nums
    Hh = Kh * NUi / DIAh
    Hc = Kc * NUo / (DIAhyd)
    
    #Step 4
    #First calculate all the areas
    Ahyd = np.pi * (DIAhyd) * L #Hydraulic area
    Ao = np.pi * DIAci * L
    Ai = np.pi * DIAh * L
    U = 1/Ai * (1/(Hc * Ao) + np.log(DIAci/DIAh)/(2*np.pi*Ks*L)+1/(Hh*Ahyd))**-1
   
    #Step 5
    Cc = MDOTc * CPc
    Ch = MDOTh * CPh
    Cmin = Ch
    Cmax = Cc
    if Cc< Ch:
        Cmin = Cc
        Cmax = Ch
    Cr = Cmin/Cmax
    NTU = U * Ai / Cmin
    eff = (1-np.exp(-NTU*(1-Cr)))/(1-Cr * np.exp(-NTU*(1-Cr)))
    Qmax = Cmin * (Thi - Tci)
    Tho = Thi - eff * Qmax / Ch
    Tco = Tci + eff * Qmax / Cc
    Q = eff * Qmax

    return Tho, Tco, Q, REYo, REYi, U*Ai, Hh, Hc, NUi,NUo

def main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L,n):
    # Assume both outlet temperature are the average of the two inlet temps
    #tho = (Thi + Tci)/2
    #tco = tho
    tho = 400
    tco = 279
    i = 0
    #Bunch of lists to store data
    results = [("Tho", "Tco", "Q", "REYo", "REYi", "U*Ai", "Hh", "Hc","NUi", "NUo")]

    while i < n:
       results.append(OutletCalc(Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L))
       
       tho = float(results[i+1][0])
       tco = float(results[i+1][1])
       
       i += 1
    return results

def qvsm(Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L):
    """
    This function will compare f with from mcodonalsd
    """
    q=[]
    q.append(OutletCalc(Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,5,L))
    plt.show("I'm always winnie")
#
#Results = (main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L,n))
#Results2 = (main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc/2,MDOTh/2,L/2,n))
    

if __name__ == '__main__':
    #runs the gui
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
