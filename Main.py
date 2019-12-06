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


            
            
            
"""
Hey Bryce I'm just gonna dump the whole file here then once you get the variables figured out we can clean this up
A few notes, I think we should re examine the equations/solution process with the group because it reaches its solution...
after one solution which seems odd
"""

import numpy as np
from iapws import IAPWS97


# These properties all need to be input via the GUI
#Properties of hot inlet
Thi = 365 # degrees kelvin
MDOTh = 10 # Kg / s
DIAh = 0.040 #m


#Properties of cold inlet

Tci = 285 # degrees kelvin
MDOTc = 8 # Kg / s
DIAco = 0.090 # m
DIAci = 0.060 #m

# OTher propeties
L = 80

def ReyNumCalc(rho,vel,dia,mu): #Where rho is density, vel is mean velocity, dia is diameter of the thing and mu is viscosity
    """
    This function calculates the Reynolds number

    """
    return rho * vel * dia/ mu

    
    
def OutletCalc(Thi, Tci, Tho, Tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L):
    """
    This function takes a bunch of inputs and outputs useful information
    """
    Ks = 237 #Thermal conductivity of the center pipe
    DIAhyd = DIAco - DIAci #Hydraulic diameter
    Thm = (Thi + Tho)/2 # Calculate average temp for hot water properties
    Tcm = (Tco + Tci)/2 # ^^^ but for cold
    print(Thm,Tcm)
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
    REYo = ReyNumCalc(RHOc,VELc, DIAhyd, MUc)
    REYi = ReyNumCalc(RHOh,VELh,DIAh,MUh)
    
    #Step 2
    #Get the Nusset numvers for both
    NUi = 0.0243 * REYi**(4/5) * PRh**0.4
    NUo = 0.0265 * REYo**(4/5) * PRc**0.5

    #Step3
    #Calculate h from the NU nums
    Hh = Ks * NUi / DIAh
    Hc = Ks * NUo / (DIAhyd)
    
    #Step 4
    #First calculate all the areas
    Ahyd = np.pi * (DIAhyd) * L #Hydraulic area
    Ao = np.pi * DIAci * L
    Ai = np.pi * DIAh * L
    U = 1/Ai * (1/(Hc * Ao) + np.log(DIAco/DIAci)/(2*np.pi*Ks*L)+1/(Hh*Ahyd))**-1
   
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

    return Tho, Tco, Q, REYo, REYi, U*Ai, Hh, Hc

def main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L):
    # Assume both outlet temperature are the average of the two inlet temps
    tho = (Thi + Tci)/2
    tco = tho
    n = 10
    i = 0
    #Bunch of lists to store data
    results = [("Tho", "Tco", "Q", "REYo", "REYi", "U*Ai", "Hh", "Hc")]

    while i < n:
       results.append(OutletCalc(Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,MDOTh,L))
       
       tho = float(results[i+1][0])
       tco = float(results[i+1][1])
       
       i += 1
    return results
Results = (main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L))
print(Results)
    

if __name__ == '__main__':
    #runs the gui
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
