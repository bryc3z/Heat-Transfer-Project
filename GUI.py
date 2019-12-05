#!/usr/bin/env python3
#
import PyQt5
import PyQt5.QtWidgets
import sys

class MainWindow(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        # Define menus (e.g., File and Help)
        #   defintes file menu
        self.menuFile = self.menuBar().addMenu("&File")
        self.actionSaveAs = PyQt5.QtWidgets.QAction("&Save As", self)
        self.actionSaveAs.triggered.connect(self.saveas) # <-- need to define this!
        self.menuFile.addActions([self.actionSaveAs])
        #   defines help menu (which does nothing)
        self.menuFile = self.menuBar().addMenu("&Help")
        
        # Define and set main widgets
        widget = PyQt5.QtWidgets.QWidget()
        self.graph = MyCanvas()
        self.box1 = PyQt5.QtWidgets.QLineEdit("Enter Number")
        #self.drop2 = PyQt5.QtWidgets.QLineEdit("Another number")
        l=["1","2","3"]
        self.drop2 = PyQt5.QtWidgets.QComboBox()
        self.drop2.addItems(l)
        self.box3 = PyQt5.QtWidgets.QLineEdit("Here will be the numbers multiplied")
        button1 = PyQt5.QtWidgets.QPushButton("math",self)
        button2 = PyQt5.QtWidgets.QPushButton("button",self)


        layout = PyQt5.QtWidgets.QVBoxLayout()
        layout.addWidget(self.graph)
        layout.addWidget(self.box1)
        layout.addWidget(self.drop2)  
        layout.addWidget(self.box3)
        layout.addWidget(button1)
        layout.addWidget(button2)
        widget.setLayout(layout)  
        self.setCentralWidget(widget)
        
    def myslot(self):
        x=eval(self.box1.text())
        y=eval(self.drop2.text())
        self.box3.setText(str(y))
        
    def saveas(self):
        #name = str(PyQt5.QtWidgets.QFileDialog.getSaveFileName(self, 'Save File'))
        #print("saving as " + name)
        b1 = int(self.box1.text())
        b2 = int(self.drop2.currentText())
        self.box3.setText(str(b1*b2))

    def close(self):
        self.close()
        print("quitting...")
        
    

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MyCanvas(FigureCanvas):

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MyCanvas, self).__init__(fig)

        # Give it some default plot (if desired).  
        self.axes.plot([1,2,3,4,5], [1,4,9,16,25])
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')  
        #self.axes.set_title('default title')
        self.setParent(parent)
    
    def update_me(self):
        self.axes.draw()

app = PyQt5.QtWidgets.QApplication(sys.argv)
widget = MainWindow()
widget.show()
app.exec_()
