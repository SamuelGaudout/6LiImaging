import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py
import lmfit
from lmfit.lineshapes import gaussian2d


def fit_Gau_2D(ODxy):
    
    OD=ODxy
    X1=[]
    Y1=[]
    Z1=[]
    for i in range(0,len(OD)):
        Z11=[]
        X11=[]
        Y11=[]
        for j in range(0,len(OD[i])):
            X11.append(j)
            Y11.append(i)
            Z11.append(OD[i][j])
            
        X1.append(X11)
        Y1.append(Y11)
        Z1.append(Z11)
    Z=np.array(Z1)
    X=np.array(X1)
    Y=np.array(Y1)
    np.nan_to_num(Z,nan=0)
    np.nan_to_num(X,nan=0)
    np.nan_to_num(Y,nan=0)
    
    model = lmfit.models.Gaussian2dModel()
    params = model.guess(Z.ravel(),x=X.ravel(),y=Y.ravel())
    result = model.fit(Z.ravel(), x=X.ravel(), y=Y.ravel(), params=params)
    # lmfit.report_fit(result)
    
    fit = model.func(X, Y, **result.best_values)
    Sig = result.params
    
    
    return (X,Y,Z,fit,Sig)



sigmax=[]
sigmay=[]
L=["Data-temp/2022_06_26_17_30_45.hdf5",
      "Data-temp/2022_06_26_17_31_00.hdf5",
      "Data-temp/2022_06_26_17_31_15.hdf5",
      "Data-temp/2022_06_26_17_31_30.hdf5",
      "Data-temp/2022_06_26_17_31_45.hdf5",
      "Data-temp/2022_06_26_17_32_15.hdf5",
      "Data-temp/2022_06_26_17_32_30.hdf5"]

L2=["Data-temp/2022_06_26_17_32_45.hdf5",
    "Data-temp/2022_06_26_17_33_00.hdf5",
    "Data-temp/2022_06_26_17_33_30.hdf5",
    "Data-temp/2022_06_26_17_33_45.hdf5",
    "Data-temp/2022_06_26_17_34_00.hdf5",
    "Data-temp/2022_06_26_17_34_15.hdf5",
    "Data-temp/2022_06_26_17_34_30.hdf5"]

L3=[#"Data-temp/2022_06_26_17_34_45.hdf5",
    #"Data-temp/2022_06_26_17_35_00.hdf5",
    "Data-temp/2022_06_26_17_35_15.hdf5",
    "Data-temp/2022_06_26_17_35_30.hdf5",
    "Data-temp/2022_06_26_17_35_45.hdf5",
    "Data-temp/2022_06_26_17_36_00.hdf5",
    "Data-temp/2022_06_26_17_36_15.hdf5",
    "Data-temp/2022_06_26_17_36_30.hdf5"]

P=[L,L2,L3]

#L=["Data-temp/2022_06_26_17_30_45.hdf5"]

for y in range(len(L2)):
    shot=L2[y]
    # print(shot)
    with h5py.File(shot, 'r') as file:
        print(file.keys()) ## to see attributes
        pic = file.get('system.soft.avtcams.manta_2')
        print(pic.keys())
        pic, ref = pic.get('abs_1')[()].astype(float) - 100, pic.get('ref_1')[()].astype(float) - 100
        v = file.get('parameters').get('v')[()].astype(float) ## Expansion time in ms
    
    
    'ROI = np.s_[550:750, 650:900] ## Define ROI'
    ROI = np.s_[600:700, 720:830] ## Define ROI
    pic, ref = pic[ROI], ref[ROI]
    
    with np.errstate(divide='ignore', invalid='ignore'):
        OD = -np.log(pic/ref) ## Compute OD, ignore division and log errors
    
    # print(OD[4])
    # print(type(OD[0][2]))
    F=fit_Gau_2D(OD)
    print('oooooooooooooooooook')
    vmax = np.nanpercentile(F[2], 99.9)
    
    
    # plt.figure()
    # plt.pcolor(F[0], F[1], F[2], vmin=0, vmax=vmax, shading='auto', cmap='jet')
    # plt.colorbar(label='z')
    # plt.title('DATA')
    # plt.show()
    # plt.savefig('Plot Data '+str(y))
    
    
    plt.figure()
    plt.pcolor(F[0], F[1], F[3], vmin=0, vmax=vmax, shading='auto', cmap='jet')
    plt.colorbar(label='z')
    plt.title('fit')
    plt.show()
    plt.savefig('Plot fit '+str(y))
    
    
    print('sx = ',F[4]['sigmax'].value)
    sigmax.append(F[4]['sigmax'].value)
    sigmay.append(F[4]['sigmay'].value)
    
print('sX = ',sigmax)
print('sY = ', sigmay)
    
    
# t=[0,0.05,0.2,0.3,0.4,0.6,0.8]
# t=[0.05,0.2,0.3,0.4,0.6]
# plt.figure()
# plt.plot(t,sigmax,'ob', label='$\sigma_x$')
# plt.plot(t,sigmay,'or',label='$\sigma_y$')
# plt.title('Evolution gaussian width')
# plt.legend()
# plt.show()
    
  
    
  
SX1 =   [4.442457906205492, 4.890531300476735, 5.5732292293032515, 7.469437905011247, 9.605543217058065, 16.575549097218936, 18.70951943090836]
SY1 =   [5.555899425750255, 5.7775164316838055, 6.136205194416708, 8.108146963245483, 9.750801986992409, 17.506930021181056, 19.755465732167213]

SX2 =   [4.687090607742048, 4.863174303682268, 7.528886481484147, 10.072353010636208, 11.971740119258023, 16.2914259885423, 24.77863491336438]
SY2 =   [5.836776107790829, 5.797962289612405, 8.246268235024543, 9.99250322589987, 12.411006373055912, 17.390016627353877, 26.033308716387605] 
  
SX3 = [5.435987039981353, 7.671393858990982, 10.29294947818818, 12.450491622272109, 15.91363696462297]   
SY3 = [6.0287081613977005, 7.669909443173273, 10.316832904091097, 12.71459175320974, 14.46863023509293]
    
  
    
SX = [(SX1[0]+SX2[0])/2,
      (SX1[1]+SX2[1])/2, 
      (SX1[2]+SX2[2]+SX3[0])/3, 
      (SX1[3]+SX2[3]+SX3[1])/3,
      (SX1[4]+SX2[4]+SX3[2])/3,
      (SX1[5]+SX2[5]+SX3[3])/3,
      (SX1[6]+SX2[6]+SX3[4])/3]  
    
SXEc = [np.sqrt((1/2)*((SX1[0]-SX[0])**2+(SX2[0]-SX[0])**2)),
        np.sqrt((1/2)*((SX1[1]-SX[1])**2+(SX2[1]-SX[1])**2)),
        np.sqrt((1/3)*((SX1[2]-SX[2])**2+(SX2[2]-SX[2])**2+(SX3[0]-SX[2])**2)),
        np.sqrt((1/3)*((SX1[3]-SX[3])**2+(SX2[3]-SX[3])**2+(SX3[1]-SX[3])**2)),
        np.sqrt((1/3)*((SX1[4]-SX[4])**2+(SX2[4]-SX[4])**2+(SX3[2]-SX[4])**2)),
        np.sqrt((1/3)*((SX1[5]-SX[5])**2+(SX2[5]-SX[5])**2+(SX3[3]-SX[5])**2)),
        np.sqrt((1/3)*((SX1[6]-SX[6])**2+(SX2[6]-SX[6])**2+(SX3[4]-SX[6])**2))]
    

# t=[0,0.05,0.2,0.3,0.4,0.6,0.8]
# plt.figure()    
# plt.plot(t,SX,'ob', label='$\sigma_x$')
# plt.errorbar(t,SX,yerr=SXEc, fmt='none')
# # plt.plot(t,sigmay,'or',label='$\sigma_y$')
# plt.title('Evolution gaussian width')
# plt.legend()
# plt.show()  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
    
    # ig, axs = plt.subplots(1, 3, figsize=(15, 5))

    

    # ax = axs[0]
    # art = ax.pcolor(F[0], F[1], F[2], vmin=0, vmax=vmax, shading='auto', cmap='jet')
    # plt.colorbar(art, ax=ax, label='z')
    # ax.set_title('Data')

    # ax = axs[1]
    # art = ax.pcolor(F[0], F[1], F[3], vmin=0, vmax=vmax, shading='auto', cmap='jet')
    # plt.colorbar(art, ax=ax, label='z')
    # ax.set_title('Fit')

    # ax = axs[2]
    
    # art = ax.pcolor(F[0], F[1], F[2]-F[3], vmin=0, vmax=vmax, shading='auto', cmap='jet')
    # plt.colorbar(art, ax=ax, label='z')
    # ax.set_title('Data - Fit')

    # for ax in axs.ravel():
    #     ax.set_xlabel('x')
    #     ax.set_ylabel('y')
    # # axs[2].remove()
    # plt.title(shot)
    # plt.show()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # ## PLOTTING ##
    # fig, ax = plt.subplots(1, 3)
    # fig.set_size_inches(15, 5)
    
    # im = ax[0].matshow(pic, vmin = 0, vmax = 100, cmap = 'jet') ## Picture with atoms
    # # #divider = make_axes_locatable(ax[0])
    # # cax = divider.append_axes("right", size="5%", pad=0.05)
    # # plt.colorbar(im, cax=cax)
    
    # im = ax[1].matshow(ref, vmin = 0, vmax = 100, cmap = 'jet') ## Reference picture
    # # divider = make_axes_locatable(ax[1])
    # # cax = divider.append_axes("right", size="5%", pad=0.05)
    # # plt.colorbar(im, cax=cax)
    
    # im = ax[2].matshow(OD, vmin = 0, vmax = 1, cmap = 'jet') ## OD
    # # divider = make_axes_locatable(ax[2])
    # # cax = divider.append_axes("right", size="5%", pad=0.05)
    # # plt.colorbar(im, cax=cax)
    
    # for _ax in ax: ## Remove axis ticks
    #     _ax.set_yticks([])
    #     _ax.set_xticks([])
        
    # plt.show()
    
