import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py
import lmfit
from lmfit.lineshapes import gaussian2d


SX1 =   [4.442457906205492, 4.890531300476735, 5.5732292293032515, 7.469437905011247, 9.605543217058065, 16.575549097218936, 18.70951943090836]
SY1 =   [5.555899425750255, 5.7775164316838055, 6.136205194416708, 8.108146963245483, 9.750801986992409, 17.506930021181056, 19.755465732167213]

SX2 =   [4.687090607742048, 4.863174303682268, 7.528886481484147, 10.072353010636208, 11.971740119258023, 16.2914259885423, 24.77863491336438]
SY2 =   [5.836776107790829, 5.797962289612405, 8.246268235024543, 9.99250322589987, 12.411006373055912, 17.390016627353877, 26.033308716387605] 
  
SX3 = [5.435987039981353, 7.671393858990982, 10.29294947818818, 12.450491622272109, 15.91363696462297]   
SY3 = [6.0287081613977005, 7.669909443173273, 10.316832904091097, 12.71459175320974, 14.46863023509293]
    
  
 

#%% Average of the data
   
SX = [(SX1[0]+SX2[0])/2,
      (SX1[1]+SX2[1])/2, 
      (SX1[2]+SX2[2]+SX3[0])/3, 
      (SX1[3]+SX2[3]+SX3[1])/3,
      (SX1[4]+SX2[4]+SX3[2])/3,
      (SX1[5]+SX2[5]+SX3[3])/3,
      (SX1[6]+SX2[6]+SX3[4])/3]  


SY = [(SY1[0]+SY2[0])/2,
      (SY1[1]+SY2[1])/2, 
      (SY1[2]+SY2[2]+SY3[0])/3, 
      (SY1[3]+SY2[3]+SY3[1])/3,
      (SY1[4]+SY2[4]+SY3[2])/3,
      (SY1[5]+SY2[5]+SY3[3])/3,
      (SY1[6]+SY2[6]+SY3[4])/3] 



    
SYEc = [np.sqrt((1/2)*((SY1[0]-SY[0])**2+(SY2[0]-SY[0])**2)),
        np.sqrt((1/2)*((SY1[1]-SY[1])**2+(SY2[1]-SY[1])**2)),
        np.sqrt((1/3)*((SY1[2]-SY[2])**2+(SY2[2]-SY[2])**2+(SY3[0]-SY[2])**2)),
        np.sqrt((1/3)*((SY1[3]-SY[3])**2+(SY2[3]-SY[3])**2+(SY3[1]-SY[3])**2)),
        np.sqrt((1/3)*((SY1[4]-SY[4])**2+(SY2[4]-SY[4])**2+(SY3[2]-SY[4])**2)),
        np.sqrt((1/3)*((SY1[5]-SY[5])**2+(SY2[5]-SY[5])**2+(SY3[3]-SY[5])**2)),
        np.sqrt((1/3)*((SY1[6]-SY[6])**2+(SY2[6]-SY[6])**2+(SY3[4]-SY[6])**2))]
    
SXEc = [np.sqrt((1/2)*((SX1[0]-SX[0])**2+(SX2[0]-SX[0])**2)),
        np.sqrt((1/2)*((SX1[1]-SX[1])**2+(SX2[1]-SX[1])**2)),
        np.sqrt((1/3)*((SX1[2]-SX[2])**2+(SX2[2]-SX[2])**2+(SX3[0]-SX[2])**2)),
        np.sqrt((1/3)*((SX1[3]-SX[3])**2+(SX2[3]-SX[3])**2+(SX3[1]-SX[3])**2)),
        np.sqrt((1/3)*((SX1[4]-SX[4])**2+(SX2[4]-SX[4])**2+(SX3[2]-SX[4])**2)),
        np.sqrt((1/3)*((SX1[5]-SX[5])**2+(SX2[5]-SX[5])**2+(SX3[3]-SX[5])**2)),
        np.sqrt((1/3)*((SX1[6]-SX[6])**2+(SX2[6]-SX[6])**2+(SX3[4]-SX[6])**2))]


t=[0,0.05,0.2,0.3,0.4,0.6,0.8]


Wx=[]
Wy=[]
for i in range(len(SX)):
    Wx.append(1-SXEc[i]/SX[i])
    Wy.append(1-SYEc[i]/SY[i])


#%% Modeling the evolution of the gaussian wighdt



def fTemp(x,a,c):
    return np.sqrt(a*x**2 + c)




modelx = lmfit.Model(fTemp)
resultx = modelx.fit(SX,x=t,a=0,c=0,weights=Wx)
print(resultx.fit_report())





modely = lmfit.Model(fTemp)
resulty = modely.fit(SY,x=t,a=0,c=0,weights=Wy)
print(resulty.fit_report())



SXEp=[]
SXEm=[]
SYEp=[]
SYEm=[]
for i in range(len(SX)):
    SXEp.append(SX[i]+SXEc[i])
    SXEm.append(SX[i]-SXEc[i])
    SYEp.append(SY[i]+SYEc[i])
    SYEm.append(SY[i]-SYEc[i])
    
modelEpx = lmfit.Model(fTemp)
resultEpx = modelEpx.fit(SXEp,x=t,a=0,c=0)
modelEmx = lmfit.Model(fTemp)
resultEmx = modelEmx.fit(SXEm,x=t,a=0,c=0)

modelEpy = lmfit.Model(fTemp)
resultEpy = modelEpy.fit(SYEp,x=t,a=0,c=0)
modelEmy = lmfit.Model(fTemp)
resultEmy = modelEmy.fit(SYEm,x=t,a=0,c=0)


#%% Plot


plt.figure()    
plt.plot(t,SX,'o',color='black', label='$\sigma_x$')
plt.errorbar(t,SX,yerr=SXEc, fmt='none',ecolor='blue',capsize = 10)
plt.plot(t,resultx.best_fit,color='red', label='fit')
plt.plot(t,resultEpx.best_fit,"--",color='gray', label='error')
plt.plot(t,resultEmx.best_fit,"--",color='gray')
plt.title('Evolution gaussian width $\sigma_x$')
plt.legend()
plt.show()  

plt.figure()
plt.plot(t,SY,'o',color='black',label='$\sigma_y$')
plt.errorbar(t,SY,yerr=SYEc, fmt='none',ecolor='blue',capsize = 10)
plt.plot(t,resulty.best_fit,color='red', label='fit')
plt.plot(t,resultEpy.best_fit,"--",color='gray', label='error')
plt.plot(t,resultEmy.best_fit,"--",color='gray')
plt.title('Evolution gaussian width $\sigma_y$')
plt.legend()
plt.show()  



ax=resultx.params['a'].value
cx=resultx.params['c'].value

axe=resultEmx.params['a'].value

ay=resulty.params['a'].value
cy=resulty.params['c'].value
aye=resultEmy.params['a'].value

#%% Temperature Calculation



Size_pixel=6.45*10**(-6)
Magnification=0.65
m=9.9883414*10**(-27)
kb=1.380649*10**(-23)

Ax=ax* Size_pixel*10**(-3)/(Magnification)

Ax=ax*((Size_pixel)**2)/(((10**(-3))**2)*Magnification**2)
Axe=axe*((Size_pixel)**2)/(((10**(-3))**2)*Magnification**2)

Ay=ay*((Size_pixel)**2)/(((10**(-3))**2)*Magnification**2)
Aye=aye*((Size_pixel)**2)/(((10**(-3))**2)*Magnification**2)

print('Coeff dir x = ',Ax)

print('Température nuage (version x) = ', Ax*(m/kb)*10**6,'+/-',(Ax-Axe)*(m/kb)*10**6, '$\mu$K')


print('Coeff dir y = ',Ay)

print('Température nuage (version y) = ', Ay*(m/kb)*10**6,'+/-',(Ay-Aye)*(m/kb)*10**6, '$\mu$K')









    