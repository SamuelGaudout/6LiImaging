import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns
sns.set_theme()


class Im():
    def __init__(self,Docname):
        
        self.Docname = Docname
    
    def Getdata(self) :
        with open(self.Docname, 'r') as ECP:
            obj1 = csv.reader(ECP)
            
            DataO=[]
            for ligne in obj1:
                DataO.append(ligne)
            Data=[]
            for i in range(len(DataO)):
                X=[]
                for y in range(len(DataO[i])):
                    X.append(float(DataO[i][y]))
                Data.append(X)
        return Data
    
    def Plot(self):
        
        plt.figure()
        sns.heatmap(self.Getdata(),cmap='seismic')
        plt.show()



class Calulus():
    def __init__(self, Docref, Docabs):
        self.Docref=Docref
        self.Docabs=Docabs
        
    def ODxy(self):
        
        Abs=Im(Docname=self.Docabs)
        Ref=Im(Docname=self.Docref)
        
        dataref=Ref.Getdata()
        dataabs=Abs.Getdata()
        
        od=[]
        for i in range(len(dataabs)):
            X=[]
            for y in range(len(dataabs[i])):
                X.append(np.log(dataref[i][y]/dataabs[i][y]))
            od.append(X)    
        print(len(od))
        
        return od
    
    def Plot(self):
        
        plt.figure()
        sns.heatmap(self.ODxy(),cmap='jet')
        plt.show()
        
        
    



# U0abs=Im(Docname='u0abs.csv')
# U0ref=Im(Docname='u0ref.csv')



# U0ref.Plot()
# U0abs.Plot()



U0=Calulus('u0ref.csv', 'u0abs.csv')
U0.Plot()

U1=Calulus('u1ref.csv', 'u1abs.csv')
U1.Plot()

U2=Calulus('u2ref.csv', 'u2abs.csv')
U2.Plot()

U3=Calulus('u3ref.csv', 'u3abs.csv')
U2.Plot()

U6=Calulus('u6ref.csv', 'u6abs.csv')
U6.Plot()

U7=Calulus('u7ref.csv', 'u7abs.csv')
U7.Plot()

U8=Calulus('u8ref.csv', 'u8abs.csv')
U8.Plot()




