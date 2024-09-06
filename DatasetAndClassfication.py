 
import time
import os, sys
from math import exp, sqrt, log
import numpy as np

# Functions for Jeffries Matusita Distance

def jm_distance(a,ee,means, covars):
        
        m1, m2 = np.array(means)
        ss1, ss2 = np.array(covars)
        
        dm = (m1-m2)
        s12 = (abs(ss1[0])+abs(ss2[0]))/2
                                  
        # Mahalanobis distance (MH):
                 
        inv = np.power(s12,-1)
        tmp = np.core.dot(dm.T, inv)
        tmp = np.core.dot(tmp, dm)
        
        MH = sqrt(tmp)
        
        # Bhattacharyya distance (B):
        sqr = sqrt( abs(ss1[0]) *abs(ss2[0]))
        
        if sqr > 0:
            
            tmp = s12 / sqr
            tmp = log(tmp)
            B = MH/8.0 + tmp/2.0
            
            # J-M distance:
            L = 2* (1 - exp(-B))
            JM = sqrt(L)
            
            # Spectral Angle Mapper
                
            ang = (np.sum(np.multiply(a,ee)))/np.sqrt((np.multiply(np.sum(np.multiply(a,a)),np.sum(np.multiply(ee,ee)))))
            
            sam = np.arccos(ang)
            
            # Jeffries-Matusita Spectral Angle Mapper
            
            ang = np.tan(sam)
            
            JMSAM = np.multiply(JM,ang)
            
        else:
            
            JMSAM = 0
            
        return JMSAM
    
    
def dataset_classification(filename1,filename2,filename3):
    
    import numpy as np
          
    # Inputs for JM-SAM
    
    se1,se2 = np.shape(filename2)
    s1,s2,s3 = np.shape(filename1)
    
    Classes = np.zeros((s1,s2,se1))
    
    ClassesP = np.zeros((s1,s2,se1))
    
    for p in range(1,se1-1):
        
        scores = np.zeros((s1,s2))
        
        spec_sign = filename2[p,:]
        
        for i in range(1,s1):
            
            for j in range(1,s2):
                
                h = filename1[i,j,:]
                
                covars = np.cov([spec_sign,h])
                                
                means = np.mean([spec_sign,h],axis = 1)
                
                scores[i,j] = jm_distance(h,spec_sign,means,covars)
                       
        B = np.unique(scores[:,:])
                                  
        dataset = np.zeros((499,s3+1))
        
        s = scores[:,:]
        
        d = 300
        
        ii = 1
        
        num = 1
    
        while num  <= d:
                                    
            res = np.where(s == B[ii])
            
            if (np.shape(res)==(2,1))==False:
                
                res = res[0]
                
            hh = (filename1[res[0],res[1],:] == 0)
            
            hh2 = np.isnan(filename1[res[0],res[1],:])
            
            if np.count_nonzero(hh[1:filename3]) == 0:
                
                if np.count_nonzero(hh2[1:filename3]) == 0:
                
                    dataset[num,:] = np.append(filename1[res[0],res[1],:],1)
                
                    num = num + 1
                
            ii = ii + 1
        
        ## Incorrect data collection
            
        B = np.nan_to_num(B)
               
        M = B[ii] * 10
        
        dd = np.shape(B)
        
        E = []
        
        for i in range(dd[0]):
            
            if B[i] > M:
                
                E.append(B[i])          
         
        pb = np.count_nonzero(E)
                
        pp = np.round(np.linspace(1, pb-1, 200)).astype(int)
    
    
        for j in range(1,200):
               
            jj = pp[j]
            
            res = np.where(s == E[jj])
            
            if (np.shape(res)==(2,1))==False:
                
                res = res[0]
                
            hh = (np.isnan(filename1[res[0],res[1],:]))
             
            if np.count_nonzero(hh[1:filename3]) == 0:
                
                dataset[d,:] = np.append(filename1[res[0],res[1],:],0)
            
            d = d + 1
            
        X = dataset[:,0:s3]
        y = dataset[:,filename3]
                  
        ## SVM implementation
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import cross_val_score
        from sklearn.svm import SVC
        
        import matplotlib.pyplot as plt
        import matplotlib.tri as tri
        import numpy as np
        from hyperopt import fmin, tpe, Trials, hp, STATUS_OK
                
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.20)   
        
        from sklearn.model_selection import GridSearchCV
        
        classifier_df = SVC(kernel = 'rbf', random_state= 0,probability=True)
        
        parameters = [{'C': [1,10,100], 'kernel': ['rbf']}]
        svmclassifier = GridSearchCV(estimator= classifier_df, param_grid = parameters, scoring = 'accuracy',cv = 10)
        svmclassifier.fit(X_train, y_train)
        
        del dataset
       
        #yprob= svmclassifier.predict_proba(X_test)
        yprob = svmclassifier.decision_function(X_test)
        ypred = (yprob>=0)
               
        #print(time.process_time() - start)
        
        from sklearn.metrics import classification_report, confusion_matrix
        from sklearn.model_selection import cross_val_score
        
        print(confusion_matrix(y_test,ypred))       
        print(classification_report(y_test,ypred))
        
        scores = cross_val_score(svmclassifier, X_train, y_train, cv=10)
        
        Class = np.zeros((s1,s2))
        Classz = np.zeros((s1,s2))
        ClassP = np.zeros((s1,s2))
        
        h = np.zeros((1,s3))
        
        for i in range(s1):
            
            for j in range(s2):
                
                h = filename1[i,j,:]
                
                h = np.reshape(h,(1,filename3))
                
                if np.any(np.isnan(h))==True:
                    
                    Class[i,j] = 0             
                    
                else:
                    
                    yy = svmclassifier.decision_function(h)
                    
                    if (yy>=0)==True:
                        
                        Class[i,j] = 1
                        
                        ClassP[i,j] = yy
                        
        del svmclassifier, X_train, y_train
                        
        Classes[:,:,p] = Class
        
        ClassesP[:,:,p] = ClassP
        
        del ClassP,Class,scores,spec_sign
        
        print('/Classification under process/')
        
        time.sleep(10)
        
    print('/Classification process has been completed/')
       
    ClassesPT = ClassesP
                    
    global F
    
    F = np.zeros((s1,s2))           
           
    for i in range(1,s1):
        
        for j in range(1,s2):
            
            arr = ClassesPT[i,j,:]
            
            nnz = arr > 0
            
            if np.count_nonzero(nnz) == 1:
                        
                max_val = max(ClassesPT[i,j,:])
                
                max_pos = np.where(ClassesPT[i,j,:]==max_val)
                
                F[i,j] = max_pos[0]
                
            if np.count_nonzero(nnz) > 1:
                
                vals = arr[np.nonzero(arr)]
                 
                #min_val = min(vals)
                max_val = max(vals)
                
                #min_pos = np.where(ClassesPT[i,j,:]==min_val)
                max_pos = np.where(ClassesPT[i,j,:]==max_val)
            
                #F[i,j] = min_pos[0]
                F[i,j] = max_pos[0]
                            
    print('Classification using Support Vector Machine has been completed')
   
