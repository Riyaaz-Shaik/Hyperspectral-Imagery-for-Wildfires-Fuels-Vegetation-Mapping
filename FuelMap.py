
import numpy as np
       
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

def Fuel_Mappping(filename1,filename2,filename3,filename4,filename5):
        
    s1,s2 = np.shape(filename2)
    
    global Fm
    
    Fm = np.zeros((s1,s2))
    
    for i in range(1,s1):
        for j in range(1,s2):
            for k in range(1,filename5):
                                
                if filename3[i,j] == -1:
                    
                    Fm[i,j] = -1
                           
                elif filename2[i,j] == k:
                
                    Fm[i,j] = filename1[k]
                        
    Fm = interpolate_missing_pixels(Fm,filename4,'linear',0)
                 
    print('Fuel Map has been generated')
    
    