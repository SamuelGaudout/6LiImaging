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
        ax = sns.heatmap(self.Getdata(),cmap='Blues_r')
        plt.title(self.Docname)
        # ax.xaxis.set_visible(False)
        # ax.yaxis.set_visible(False)
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.show()



class Calulus():
    def __init__(self, Docref, Docabs):
        self.Docref=Docref
        self.Docabs=Docabs
        
    def Print(self):
        print(0.65*10**(-6))
        
    def ODxy(self):
        
        Abs=Im(Docname=self.Docabs)
        Ref=Im(Docname=self.Docref)
        
        dataref=Ref.Getdata()
        dataabs=Abs.Getdata()
        
        offset=0
        
        od=[]
        for i in range(len(dataabs)):
            X=[]
            for y in range(len(dataabs[i])):
                
                if dataabs[i][y]-offset==0:
                    X.append(0)
                elif dataabs[i][y]>dataref[i][y]:
                    X.append(0)
                else:
                    X.append(np.log(abs(dataref[i][y]-offset)/abs(dataabs[i][y]-offset)))
            od.append(X)    
        #print(len(od))
        
        return od
    
    
    def Ntot(self):
        
        N=0
        OD=self.ODxy()
        sigma_0= 3*(670.977*10**(-9))**2 /(2*np.pi)
        Size_pixel=6.45*10**(-6)
        Clebsch=0.5
        
        if self.Docref=='u8ref.csv':
            Magnification=10  
            Cmin=-10
            Imin=120
            Imax=160
            Jmin=620
            Jmax=676
            
        elif self.Docref=='u7ref.csv':
            Magnification=1.95
            Cmin=-10
            Imin=648
            Imax=672
            Jmin=753
            Jmax=790
            
        elif self.Docref=='u6ref.csv':
            Magnification=1.95
            Cmin=-10
            Imin=340
            Imax=420
            Jmin=760
            Jmax=840
            
        elif self.Docref=='u3ref.csv':
            Magnification=0.65            
            Cmin=-10
            Imin=352
            Imax=405
            Jmin=770
            Jmax=810
            
        elif self.Docref=='u2ref.csv':
            Magnification=0.65
            Cmin=-10
            Imin=340
            Imax=416
            Jmin=763
            Jmax=830
            
        elif self.Docref=='u1ref.csv':
            Magnification=0.65
            Cmin=-10
            Imin=264
            Imax=528
            Jmin=672
            Jmax=945
            
        else :
            Magnification=0.65
            Cmin=-18
            Imin=264
            Imax=795
            Jmin=448
            Jmax=1064
            
        # for i in range(len(OD)):
        #     for j in range(len(OD[i])):
        
        for i in range(Imin,Imax,1):
            for j in range(Jmin,Jmax,1):
                
                if OD[i][j]<Cmin:
                    OD[i][j]=0
                
                N=N+(1/(Clebsch*sigma_0))*OD[i][j]*((Size_pixel)**2)/(Magnification)
                #print(OD[i][j])
        return (N,Imin,Imax,Jmin,Jmax)
    
    
    def Plot(self):
        Lmax=self.Ntot()
        plt.figure()
        sns.heatmap(self.ODxy(),cmap='jet')
        plt.xlim(Lmax[3],Lmax[4])
        plt.ylim(Lmax[1],Lmax[2])
        plt.title(self.Docref)
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.show()
        
        
    
if __name__ == "__main__":


    # U0abs=Im(Docname='u0abs.csv')
    # U0ref=Im(Docname='u0ref.csv')
    
    # U0ref.Plot()
    # U0abs.Plot()
    
    
    
    # U0=Calulus('u0ref.csv', 'u0abs.csv')
    # NN0=U0.Ntot()[0]
    # print('Nb atomes U0 = ',NN0)
    # U0.Plot()
    
    # U1=Calulus('u1ref.csv', 'u1abs.csv')
    # NN1=U1.Ntot()[0]
    # print('Nb atomes U1 = ',NN1)
    # U1.Plot()
    
    U2=Calulus('u2ref.csv', 'u2abs.csv')
    NN2=U2.Ntot()[0]
    print('Nb atomes U2 = ',NN2)
    U2.Plot()
    
    U3=Calulus('u3ref.csv', 'u3abs.csv')
    NN3=U3.Ntot()[0]
    print('Nb atomes U3 = ',NN3)
    U3.Plot()
    
    # U6=Calulus('u6ref.csv', 'u6abs.csv')
    # NN6=U6.Ntot()[0]
    # print('Nb atomes U6 = ',NN6)
    # U6.Plot()
    
    # U7=Calulus('u7ref.csv', 'u7abs.csv')
    # NN7=U7.Ntot()[0]
    # print('Nb atomes U7 = ',NN7)
    # U7.Plot()
    
    # U8=Calulus('u8ref.csv', 'u8abs.csv')
    # NN=U8.Ntot()[0]
    # print('Nb atomes U8 = ',NN)
    # U8.Plot()




