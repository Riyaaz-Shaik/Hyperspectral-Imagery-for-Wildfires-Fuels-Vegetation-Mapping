# Please read README.txt before starting the program

Input_Txt_File = 'D:\FirEUrisk\FuelMap_Portugal_2\INPUT_20220707.txt'

## INPUT for the FUEL MAPPING using PRISMA Hyperspectral Imagery

lines = []
with open(Input_Txt_File) as f:
    lines = f.readlines()

count = 0
for line in lines:
    count += 1
    print(f'line {count}: {line}')

# Filepath for HCO, WVL, CLD and LCC

filepath_h = lines[2][6::]
filepath_HCO = filepath_h[:-1]

filepath_w = lines[4][6::]
filepath_WVL = filepath_w[:-1]

filepath_c = lines[6][6::]
filepath_CLD = filepath_c[:-1]

filepath_lc = lines[8][6::]
filepath_LCC = filepath_lc[:-1]

NumOfFTs = int(lines[12][23::]) # Number of Fuel Types

import numpy as np

NumOfLines = np.shape(lines)

nos = NumOfFTs + 1

PixCodes = np.zeros((nos,4))

d = 1

for i in range(17,NumOfLines[0]):
    
    if lines[i] != '\n':
        
        PixelX = lines[i][2:7]
        PixelY = lines[i][7:12]
        Code = lines[i][12:15]
        
        PixCodes [d,1] = PixelX
        PixCodes [d,2] = PixelY
        PixCodes [d,3] = Code
        
        d = d + 1

print(PixCodes)

import time

# Read and Preprocess Data

from ReadPreprocessData import RAP

RAP(filepath_HCO,filepath_CLD,filepath_LCC)

from ReadPreprocessData import hsi,cloud,Er,lcc,Bg

time.sleep(10)

# Correct Error lines, Remove Error bands and NaN Values

from CorrectErrPixels import CorrectErrPixels

CorrectErrPixels(hsi,cloud,Bg)

from CorrectErrPixels import hsi3,s4

time.sleep(10)

# Remove Clouded Pixels

del hsi

from Cloud import cloudremoval

cloudremoval(hsi3,cloud)

from Cloud import hc

time.sleep(10)

# Denoising of hypercube

del hsi3

from Denoising import filtering

filtering(hc)

from Denoising import hcf

time.sleep(10)

del hc

# Endmembers

import numpy as np
from matplotlib import pyplot as plt

ems = np.zeros((nos,s4),dtype = float)
ee = np.zeros((s4,nos),dtype = float)

for i in range(1,nos):
    
    P1 = PixCodes[i,1].astype(int)
    P2 = PixCodes[i,2].astype(int)
    
    ems[i,:] = hcf[P1,P2,:]
    ee[:,i-1] = hcf[P1,P2,:]

plt.plot(ee[:,1:nos-1])
plt.xlabel("Bands")
plt.ylabel("Reflectances")
plt.title('Spectral Signatures')
plt.show()    

if np.isnan(ems).any()==False:
      
    print('Spectral Signatures are considered for further processing')       
              
    # Dataset Preparation and Classification
    
    from DatasetAndClassfication import dataset_classification
    
    dataset_classification(hcf,ems,s4)
    
    from DatasetAndClassfication import F
    
    time.sleep(10)
    
    # Spectral Unmixing
    
    from SpectralUnmixing import Spectral_Unmixing
    
    Spectral_Unmixing(hcf,s4,lcc,F,ems)
    
    from SpectralUnmixing import Cll,sh
    
    time.sleep(10)
    
    # Other Classifications
    
    from OtherClassifications import Other_Classifications
    
    Other_Classifications(Cll,sh,cloud,Er,lcc,Bg)
    
    from OtherClassifications import Cl_f,mask
    
    time.sleep(10)
    
    # Fuel Mapping
    
    import numpy as np
    
    FMn = np.zeros((nos,1))
    
    for i in range(1,nos):
        
        Code = PixCodes[i,3].astype(int)
        
        FMn[i,:] = Code
    
    from FuelMap import Fuel_Mappping
    
    Fuel_Mappping(FMn,Cl_f,Bg,mask,nos)
    
    from FuelMap import Fm
    
    time.sleep(10)
    
    # Save file GTIff
    
    from SaveGTiff import read_geotiff,write_geotiff
    
    # Classification and Fuel Map Writing
    
    nlcd01_arr, nlcd01_ds = read_geotiff(filepath_HCO)
    
    write_geotiff("Cl_20220707.tif", Cl_f, nlcd01_ds)
        
    write_geotiff("FM_20220707.tif", Fm, nlcd01_ds)
    
    print('Classification and Fuel Maps are saved in the folder of this program')
          
elif np.isnan(ems).any()==True:
    
    print('Spectral Signatures contain NaN - Please modify and rerun the program')
    
    