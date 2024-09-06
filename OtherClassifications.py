

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

def Other_Classifications(filename1,filename2,filename3,filename4,filename5,filename6):
            
    s1,s2 = np.shape(filename1)
    
    for i in range(1,s1):
        
        for j in range(1,s2):
                                    
            if filename6[i,j] == -1:
                
                filename1[i,j] = 0
                
            elif filename4[i,j] == 1:
                        
                filename1[i,j] = np.nan
                                
            elif filename3[i,j] == 1:
                
                filename1[i,j] = -6
                
            elif filename5[i,j] == 1 and filename1[i,j] == 0:
                
                filename1[i,j] = -3
                
            elif filename5[i,j] == 2 and filename1[i,j] == 0:
                
                filename1[i,j] = -1
                
            elif filename5[i,j] == 0 and filename1[i,j] == 0:
                
                filename1[i,j] = -3
                
            elif filename5[i,j] == 3 and filename1[i,j] == 0:
                
                filename1[i,j] = -2
                
            elif filename5[i,j] == 5 and filename1[i,j] == 0:
                
                filename1[i,j] = -5
                
            elif filename5[i,j] == 6 and filename1[i,j] == 0:
                
                filename1[i,j] = -3
                
            elif filename5[i,j] == 10 and filename1[i,j] == 0:
                
                filename1[i,j] = -5
                
            elif filename5[i,j] == 255 and filename1[i,j] == 0:
                
                filename1[i,j] = -5
                
            elif filename2[i,j] == 1 and filename1[i,j] == 0:
                
                filename1[i,j] = -6
                
            elif filename5[i,j] == 4 and filename1[i,j] == 0:
                        
                filename1[i,j] = -4
                                
            elif filename5[i,j] != -999 and filename1[i,j] == 0:
                
                filename1[i,j] = np.nan
                
            elif filename6[i,j] == 0 and filename1[i,j] == 0:
                    
                filename1[i,j] = np.nan
    
    global mask
    mask = np.isnan(filename1)
    
    global Cl_f
    
    Cl_f = interpolate_missing_pixels(filename1,mask,'linear',0)
    
    print('Assignment of other classifications is completed')       

