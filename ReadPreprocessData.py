
              
import numpy as np
        
from osgeo import gdal
    
def RAP(filename1,filename2,filename3):
        
    # Read and Preprocess PRISMA Hyperspectral Data
    
    raster = gdal.Open(filename1)
       
    # Dimensions
       
    s1 = raster.RasterYSize
    s2 = raster.RasterXSize
    
    # Number of bands
    
    s3 = raster.RasterCount
            
    hc = np.zeros((s1,s2,s3))
    
    for k in range(1,s3):
        
        dataset = raster.GetRasterBand(k)
    
        hc[:,:,k] = dataset.ReadAsArray()
        
    
    bands = np.r_[99:110,142:160]
    
    global hsi
    
    hsi = np.delete(hc,bands,2)
    
    del hc
        
    s1,s2,s3 = np.shape(hsi)
       
    # Read cloud mask  
        
    cc = gdal.Open(filename2)
        
    global cloud
        
    cloud = cc.GetRasterBand(1).ReadAsArray().astype(float)
        
    # Read Land Cover
    
    lc = gdal.Open(filename3)
        
    global lcc
        
    lcc = lc.GetRasterBand(1).ReadAsArray().astype(float)
        
    # Find Error Pixels
    
    global Bg
    
    Bg = np.zeros((s1,s2))
        
    global Er
            
    Er = np.zeros((s1,s2))
        
    for i in range(s1):
        
        for j in range(s2):
    
            if (cloud[i,j]==-999)==True:
             
                t = hsi[i,j,1:s3]
                
                tt = (t == -999)
                
                if (all(tt))==True:
                    
                    Bg[i,j]=-1
                    
                    del t
                    
                else:
                        
                    Er[i,j]=1
                    
                if lcc[i,j]>10:
                                              
                    Er[i,j]=1
         
                    
    print ('Read and Preprocess Task has been completed')
    
        
