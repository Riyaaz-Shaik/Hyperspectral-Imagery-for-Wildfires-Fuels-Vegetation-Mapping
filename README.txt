
This README file describes about the steps to be followed for mapping fuel types using PRISMA Hyperspectral Imagery.


Georeferencing (https://github.com/IREA-CNR-MI/prismaread):

This algorithm used R software for Georeferencing and Masking Error Pixels utilizing the Error Matrix provided in the PRISMA package.
Two separate files for georeferencing were provided in the zip folder. Among them, it is recommended to provide the filepath of L2C in L1 algorithm
so that both the images will have same samples and lines.

Steps to be followed are as follows:
 1. For the first time, install package of "remotes" and then remotes::install_github("lbusett/prismaread",force = TRUE).
 1. Use GeoRef_L2C for georeferencing the L2C data.
 2. Then, Use GeoRef_L1 for georeferencing the L1 data.
 3. In GeoRef_L1, at in_L2_file, provide the filepath of L2C file.

Fuel Mapping:

This algorithm is developed in Python using packages such as numpy, spectral, matplotlib, time, scipy, math, scipy, pandas, pysptools, os and gdal. 
Program file (__mainprogram_.py)contains the main program and other py files will be called as function in this files. 
Steps to be followed for the fuel mapping are as follows:

1. Inputs for the processing of the data have to be given using the INPUT.txt file. The format and spacing as given in the INPUT.txt file should be followed.
   Inputs required for the algorithm are L2C_HCO_FULL.tif, L1_CLOUD.tif and L1_LAND_COVER.tif. Along with this, a) number of fuel types to be classified and,
   b) pixels corresponding to each fuel type have to be provided in the row(X) and column (Y) of the INPUT.txt.
2. Filepaths of georeferenced images have to be provided in the INPUT file. If any modifications are done in INPUT formatting, __mainprogram_.py have to be modified
   accordingly.
3. Fuel Model codes (Anderson/Scott Burgan) have to be provided corresponding to the each fuel type in the INPUT.
4. Finally, __mainprogram__.py have to be used to start the program for mapping fuel types 
5. Classification Map (Cl.tif) and Fuel Map (FM.tif) will be saved in the same folder of the INPUT.

Apart from the given classes, few more classes will be assigned using the Land Cover from (L1) which is as follows:
 
 -6 - clouds. [Anderson: 0]
 -5 - Not of all previous classifications. [0]
 -4 - Vegetation unclassified. [0]
 -3 - Urban component, water and Snow. [0]
 -2 - Crops. [0]
 -1 - Bare Soil. [0]




