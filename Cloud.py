
import numpy as np
    
def cloudremoval(filename1,filename2):
           
    s1,s2,s3 = np.shape(filename1)
    
    for i in range(s1):
        
        for j in range(s2):
            
            if (filename2[i,j]==1)==True:
            
                filename1[i,j,:] = 0
    
    global hc
    
    hc = filename1    
                     
    print ('Clouded Pixels has been Removed')
           
                
            

