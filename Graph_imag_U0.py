import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns
sns.set_theme()

import lmfit
from lmfit.lineshapes import gaussian2d




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
    def __init__(self, Docref, Docabs, Gau=False, Heat=False, Gau_fit=False,Gau_trD=False):
        self.Docref=Docref
        self.Docabs=Docabs
        self.Gau=Gau
        self.Heat=Heat
        self.Gau_fit=Gau_fit
        self.Gau_trD=Gau_trD
        
    def Print(self):
        print(0.65*10**(-6))
        
    def ODxy(self):
        
        Abs=Im(Docname=self.Docabs)
        Ref=Im(Docname=self.Docref)
        
        dataref=Ref.Getdata()
        dataabs=Abs.Getdata()
        
        offset=90
        
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
            Imin=110
            Imax=170
            Jmin=620
            Jmax=680
            
        elif self.Docref=='u7ref.csv':
            Magnification=1.95
            Cmin=-10
            Imin=642
            Imax=679
            Jmin=753
            Jmax=790
            
        elif self.Docref=='u6ref.csv':
            Magnification=1.95
            Cmin=-10
            Imin=642
            Imax=677
            Jmin=755
            Jmax=790
            
        elif self.Docref=='u3ref.csv':
            Magnification=0.65            
            Cmin=-10
            Imin=352
            Imax=405
            Jmin=764
            Jmax=817
            
        elif self.Docref=='u2ref.csv':
            Magnification=0.65
            Cmin=-10
            Imin=330
            Imax=426
            Jmin=749
            Jmax=845
            
        elif self.Docref=='u1ref.csv':
            Magnification=0.65
            Cmin=-10
            Imin=259
            Imax=532
            Jmin=672
            Jmax=945
            
        else :
            Magnification=0.65
            Cmin=-18
            Imin=222
            Imax=838
            Jmin=448
            Jmax=1064
            
        # for i in range(len(OD)):
        #     for j in range(len(OD[i])):
        
        for i in range(Imin,Imax,1):
            for j in range(Jmin,Jmax,1):
                
                if OD[i][j]<Cmin:
                    OD[i][j]=0
                
                N=N+(1/(Clebsch*sigma_0))*OD[i][j]*((Size_pixel)**2)/(Magnification**2)
                #print(OD[i][j])
        return (N,Imin,Imax,Jmin,Jmax)
    
    
    
    def Gaussian(self):
        Y=[]
        X=[]
        Yf=[]
        D=[]
        F=self.fit_Gau_2D()
        print(F[1][0][0],F[1][len(F[1])-1][len(F[1][len(F[1])-1])-1])
        T=0
        for i in range(0,len(F[0][0])):
        #for i in range(F[1][0][0],F[1][len(F[1])-1][len(F[1][len(F[1])-1])-1]):
            Seum=0
            Seumf=0
            for j in range(0,len(F[1][0])):
            #for j in range(F[0][0][0],F[0][len(F[0])-1][len(F[0][len(F[0])-1])-1]):
                Seum=Seum+F[2].tolist()[i][j]
                
                Seumf=Seumf+F[3].tolist()[i][j]
            DE=Seumf-Seum
            T+=1
            print(T,"/",len(F[0][0]))
            Y.append(Seum)
            Yf.append(Seumf)
            D.append(DE)
            X.append(i)
        return X,Y,Yf,D
    
    
    
    def fit_Gau_2D(self):
        
        OD=self.ODxy()
        Ninfo=self.Ntot()
        X1=[]
        Y1=[]
        Z1=[]
        for i in range(Ninfo[1],Ninfo[2]-1,1):
            Z11=[]
            X11=[]
            Y11=[]
            for j in range(Ninfo[3],Ninfo[4]-1,1):
                X11.append(j)
                Y11.append(i)
                Z11.append(OD[i][j])
                
            X1.append(X11)
            Y1.append(Y11)
            Z1.append(Z11)
        Z=np.array(Z1)
        X=np.array(X1)
        Y=np.array(Y1)
    
        model = lmfit.models.Gaussian2dModel()
        params = model.guess(Z.ravel(),x=X.ravel(),y=Y.ravel())
        result = model.fit(Z.ravel(), x=X.ravel(), y=Y.ravel(), params=params)
        lmfit.report_fit(result)
        
        fit = model.func(X, Y, **result.best_values)
        
        
        
        return (X,Y,Z,fit)
    
    
         
        
    def Plot(self,Gau=False,Heat=False,Gau_fit=False,Gau_trD=False):
        
        if Gau==True:
            G=self.Gaussian()
            plt.figure()
            plt.xlabel('$y$')
            plt.ylabel('$n_{2D}$')
            plt.plot(G[0],G[1],'.',color='blue', label='Data')
            plt.plot(G[0],G[2],'-r', label='fit')
            plt.plot(G[0],G[3],'-g', label='$\Delta$')
            plt.title(self.Docref)
            plt.legend()
            plt.show()
            
            
        if Gau_trD==True:
            L=self.fit_Gau_2D()
            X,Y,Z=L[0],L[1],L[2]
            plt.figure()
            ax = plt.axes(projection='3d')
            ax.contour3D(X, Y, Z, rstride=1, cstride=1,
                cmap='jet', edgecolor='none')
            
        if Gau_fit==True:
            F=self.fit_Gau_2D()
            ig, axs = plt.subplots(2, 2, figsize=(10, 10))

            vmax = np.nanpercentile(F[2], 99.9)

            ax = axs[0, 0]
            art = ax.pcolor(F[0], F[1], F[2], vmin=0, vmax=vmax, shading='auto', cmap='jet')
            plt.colorbar(art, ax=ax, label='z')
            ax.set_title('Data')

            ax = axs[0, 1]
            art = ax.pcolor(F[0], F[1], F[3], vmin=0, vmax=vmax, shading='auto', cmap='jet')
            plt.colorbar(art, ax=ax, label='z')
            ax.set_title('Fit')

            ax = axs[1, 0]
            
            art = ax.pcolor(F[0], F[1], F[2]-F[3], vmin=0, vmax=vmax, shading='auto', cmap='jet')
            plt.colorbar(art, ax=ax, label='z')
            ax.set_title('Data - Fit')

            for ax in axs.ravel():
                ax.set_xlabel('x')
                ax.set_ylabel('y')
            axs[1, 1].remove()
            plt.title(self.Docref)
            plt.show()

        
        if Heat==True:
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
    
    P=[0,1,2,3,6,7,8]
    # P=[1,2,3,6,7,8]
    P=[0,2]
    for i in P:
        U=Calulus('u'+str(i)+'ref.csv', 'u'+str(i)+'abs.csv')
        #U.Plot(Gau=True)
        U.Plot(Gau_fit=True)
        # ODD=U.ODxy()
        #U.Plot(Gau=True)
        NN=U.Ntot()[0]
        print('Nb atomes U'+str(i)+' = ',NN)
    
   
    


