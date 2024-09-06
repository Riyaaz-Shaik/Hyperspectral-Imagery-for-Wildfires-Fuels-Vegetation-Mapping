
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def apply_convolution(sig):
    window = 1.5
    conv = np.repeat([0., 1., 0.], window)
    filtered = signal.convolve(sig, conv, mode='same') / window
    return filtered
    
def filtering(filename1):
           
    s1,s2,s3 = np.shape(filename1)
    
    global hcf
    
    hcf = np.zeros((s1,s2,s3))
    
    for i in range(s1):
        
        for j in range(s2):
            
            h = filename1[i,j,:]
            
            h2 = apply_convolution(h)
            
            hcf [i,j,:] = h2
                             
    print ('Processing for Denoising the Hypercube has been completed')
  