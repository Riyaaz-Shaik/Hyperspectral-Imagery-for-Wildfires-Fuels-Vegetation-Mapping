    
import math

import numpy as np

from scipy import interpolate

def interpolate_missing_pixels(
        image: np.ndarray,
        mask: np.ndarray,
        method: str = 'linear',
        fill_value: int = 0
):
    
    """
    :param image: a 2D image
    :param mask: a 2D boolean image, True indicates missing values
    :param method: interpolation method, one of
        'nearest', 'linear', 'cubic'.
    :param fill_value: which value to use for filling up data outside the
        convex hull of known pixel values.
        Default is 0, Has no effect for 'nearest'.
    :return: the image with missing values interpolated
    """
    
    from scipy import interpolate

    h, w = image.shape[:2]
    xx, yy = np.meshgrid(np.arange(w), np.arange(h))

    known_x = xx[~mask]
    known_y = yy[~mask]
    known_v = image[~mask]
    missing_x = xx[mask]
    missing_y = yy[mask]

    interp_values = interpolate.griddata(
        (known_x, known_y), known_v, (missing_x, missing_y),
        method=method, fill_value=fill_value
    )

    interp_image = image.copy()
    interp_image[missing_y, missing_x] = interp_values

    return interp_image
    

import numpy as np
    
import math

import time
    
def CorrectErrPixels (filename1,filename2,filename3):
        
    t = 1
    
    tt = 1
    
    p = 1
    
    s1,s2,s3 = np.shape(filename1)
    
    erper = np.zeros((s3))
    
    band = 0
    
    err = 0
    
    for k in range(1,s3):
          
        h = filename1[:,:,k]
                
        b = (h == -999)
           
        bb = np.zeros((s1,s2))
           
        for i in range(s1):
               
            for j in range(s2):
                   
                if (filename2[i,j] == 0) == True:
                                    
                    if (filename3[i,j] == 0) == True:
                       
                        if b[i,j] == True:
                           
                            bb[i,j] = 1
                        
        del h
                                                
        erpix = np.count_nonzero(bb)
                      
        tot = np.count_nonzero(filename2 == 0)
                                   
        erper[k] = np.divide(erpix, tot)
        
        del erpix,b,bb,tot
            
        if (erper[k] > 0.1)== True:
                            
            band = np.append(band,k)
                
            err = np.append(err,erper[k])
               
    hsi2 = np.delete(filename1,band,2)
    
    print ('Band Removal has been completed')
    
    # Removal of Negative and NaN values
    
    global s4
    
    s1,s2,s4 = np.shape(hsi2)
    
    hsi2[hsi2 < 0] = np.nan
            
    global hsi3
            
    hsi3 = np.zeros((s1,s2,s4))  
    
    print('Filling up the missing pixels -  The band count goes as follows')
       
    for k in range(1,s4):
        
        h = hsi2[:,:,k]
       
        masc = np.zeros((s1,s2),dtype=bool)
       
        for i in range(s1):
               
            for j in range(s2):
               
                if (filename3[i,j] == 0) == True:
                   
                    if (np.isnan(h[i,j])) == True:
       
                        masc[i,j] = np.isnan(h[i,j])
       
        hh = interpolate_missing_pixels(h,masc,'linear',0)
       
        time.sleep(0.5)
                  
        hsi3[:,:,k] = hh
       
        del hh,masc,h
               
        print(k)
       
    print ('Correction of Noisy Pixels has been completed')
       
                