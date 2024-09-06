

import os
import os.path as osp
import numpy as np
from numpy import *

import pysptools.util as util
import pysptools.eea as eea
import pysptools.abundance_maps as amp
import pysptools.classification as cls
import pysptools.material_count as cnt

def Spectral_Unmixing(filename1,filename2,filename3,filename4,filename5):
            
    # nans to num
    
    where_are_NaNs = isnan(filename1)
    filename1[where_are_NaNs] = 0
    
    # Abundance Maps
    
    am = amp.FCLS()
    
    amaps = am.map(filename1,filename5)
    
    am.display(colorMap='jet',columns=5,suffix='S2IGI')
    
    s1,s2,s3 = np.shape(amaps)
    
    amapsT = np.zeros((s1,s2,s3))
    
    for k in range(1,s3):
        
        mapa = amaps[:,:,k]
        
        ma = mapa.max()
        
        ma = str(ma)
        
        Thres = np.divide(float(ma[2]),10)- 1/100
        #0.89#
        #Thres = (float(ma[2] + ma[3]))/100 - float(ma[3])/200
        #Thres = float(ma) - (float(ma) * 0.05 )
        
        mapaT = np.zeros((s1,s2))
        
        for i in range(1,s1):
        
            for j in range(1,s2):
                                    
                if mapa[i,j] > Thres:
                   
                    mapaT[i,j] = mapa[i,j]
                    
                    amapsT[i,j,k] = mapaT[i,j]
                   
    
    F2 = np.zeros((s1,s2))
                 
    for i in range(1,s1):
        
        for j in range(1,s2):
            
            if filename3[i,j]==4 or filename3[i,j]==5:
                
                max_val = max(amapsT[i,j,:])
                        
                max_pos = np.where(amapsT[i,j,:]==max_val)
            
                max_pos2 = max_pos[0].astype(float)
                        
                F2[i,j] = max_pos2[0]

    
    global Cll
    
    Cll = np.zeros((s1,s2))
    
    for i in range(1,s1):
        
        for j in range(1,s2):
            
            if filename4[i,j] == 0:
                
                Cll[i,j] = F2 [i,j]
                
            elif filename4[i,j] != 0:
                
                Cll[i,j] = filename4[i,j]
                
    
    # Principal Component Analysis
    
    from spectral import principal_components
    
    pc = principal_components(filename1)
    pc3 = pc.reduce(num=3)
    len(pc3.eigenvalues)
    hsip = pc3.transform(filename1)
    
    pc1 = hsip[:,:,1]
    a = pc1.min()
    b = pc1.min()/10
    
    global sh
    sh = [pc1>a] and [pc1<b][0]
    
    print('Spectral Unmixing is completed')
    
    