import numpy as np
from iapws import IAPWS97
import csv
import matplotlib.pyplot as plt

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
n = 10
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
    q.append(OutLetCalc(Thi, Tci, tho, tco, DIAco, DIAci,DIAh,MDOTc,5,L))
    plt.show("I'm always winnie")

Results = (main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc,MDOTh,L,n))
Results2 = (main(Thi, Tci, DIAco, DIAci,DIAh,MDOTc/2,MDOTh/2,L/2,n))
Results3 = Results[-1]
Tho, Tco, Q, REYo, REYi, UA, Hh, Hc, NUi, NUo = Results3
print (round(Tho,6))
print (Tco)
print (Q)




