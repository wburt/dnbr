#Landsat.py
#Created October 2009
#Modified June 2013
#Reads and Landsat 5,7,8 Metadata files (.mtl) into object parameters for use in scripting tools
#Changelog
#Added Landsat 8 MTL object


import time

#inPath = r"W:\FOR\RSI\RSI\Projects\RGG\2009\037_Burn_Severity_Mapping\data\Source\TM5_48024_2009_09_08"
#inMTL = "L5048024_02420090908_MTL.txt"
#MTLfile = os.path.join(inPath,inMTL)

class TM_MTL(object):
    def __init__(self, mtlFile):
        # Constructor method
        # mtlFile - the Landsat MTL file (metatdata) for the acquired landsat scene
        self.mtlTxt = str(mtlFile)
        self.read()
    def read(self):
        rFile = open(self.mtlTxt)
        mtl = rFile.readlines()
        for line in mtl:
            #Metadata
            if line.split("=")[0].strip() == "SPACECRAFT_ID":
                self.SPACECRAFT = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "DATA_TYPE":
                self.PRODUCT_TYPE = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "SENSOR_ID":
                self.SENSOR_ID = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "DATE_ACQUIRED":
                self.AQUISITION_DATE = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "SUN_ELEVATION":
                self.SUN_ELEVATION = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "WRS_PATH":
                self.PATH = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "WRS_ROW":
                self.ROW = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_1":
                self.BAND1_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_2":
                self.BAND2_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_3":
                self.BAND3_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_4":
                self.BAND4_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_5":
                self.BAND5_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_6":
                self.BAND6_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_7":
                self.BAND7_FILE_NAME = line.split("=")[1].strip()
                #MIN_MAX_Radiance
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_1":
                self.LMAX_BAND1 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_1":
                self.LMIN_BAND1 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_2":
                self.LMAX_BAND2 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_2":
                self.LMIN_BAND2 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_3":
                self.LMAX_BAND3 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_3":
                self.LMIN_BAND3 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_4":
                self.LMAX_BAND4 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_4":
                self.LMIN_BAND4 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_5":
                self.LMAX_BAND5 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_5":
                self.LMIN_BAND5 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_6":
                self.LMAX_BAND6 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_6":
                self.LMIN_BAND6 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_7":
                self.LMAX_BAND7 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_7":
                self.LMIN_BAND7 = line.split("=")[1].strip()
            #MIN MAX PIXEL VALUE
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_1":
                self.QCALMAX_BAND1 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_1":
                self.QCAQCALMIN_BAND1 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_2":
                self.QCALMAX_BAND2 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_2":
                self.QCALMIN_BAND2 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_3":
                self.QCALMAX_BAND3 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_3":
                self.QCALMIN_BAND3 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_4":
                self.QCALMAX_BAND4 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_4":
                self.QCALMIN_BAND4 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_5":
                self.QCALMAX_BAND5 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_5":
                self.QCALMIN_BAND5 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_6":
                self.QCALMAX_BAND6 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_6":
                self.QCALMIN_BAND6 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_7":
                self.QCALMAX_BAND7 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_7":
                self.QCALMIN_BAND7 = line.split("=")[1].strip()
            #Projection Parameters
            if line.split("=")[0].strip()== "DATUM":
                self.REFERENCE_DATUM = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "ELLIPSOID":
                self.REFERENCE_ELLIPSOID = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "GRID_CELL_SIZE_REFLECTIVE ":
                self.CELL_SIZE = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "MAP_PROJECTION":
                self.MAP_PROJECTION = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "ZONE":
                self.UTM_ZONE = line.split("=")[1].strip()
        del line, rFile
    #end TM_MTL
    def getJulianDay(self):
        date = self.AQUISITION_DATE
        (year,month,day) = date.split('-')
        year = int(year)
        month = int(month)
        day = int(day)
        t= time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        JulianDay = time.gmtime(t)[7]
        return JulianDay

#end OBject
class Landsat8_MTL(object):
    def __init__(self, mtlFile):
        # Constructor method
        # mtlFile - the Landsat MTL file (metatdata) for the acquired landsat scene
        self.mtlTxt = str(mtlFile)
        self.read()
    def read(self):
        rFile = open(self.mtlTxt)
        mtl = rFile.readlines()
        for line in mtl:
            #Metadata
            if line.split("=")[0].strip() == "SPACECRAFT_ID":
                self.SPACECRAFT = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "DATA_TYPE":
                self.DATA_TYPE = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "SENSOR_ID":
                self.SENSOR_ID = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "DATE_ACQUIRED":
                self.AQUISITION_DATE = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "SUN_ELEVATION":
                self.SUN_ELEVATION = line.split("=")[1].strip()
            if line.split("=")[0].strip() == "WRS_PATH":
                self.PATH = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "WRS_ROW":
                self.ROW = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_1":
                self.BAND1_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_2":
                self.BAND2_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_3":
                self.BAND3_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_4":
                self.BAND4_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_5":
                self.BAND5_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_6":
                self.BAND6_FILE_NAME = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "FILE_NAME_BAND_7":
                self.BAND7_FILE_NAME = line.split("=")[1].strip()
##                #MIN_MAX_Radiance
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_1":
##                self.LMAX_BAND1 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_1":
##                self.LMIN_BAND1 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_2":
##                self.LMAX_BAND2 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_2":
##                self.LMIN_BAND2 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_3":
##                self.LMAX_BAND3 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_3":
##                self.LMIN_BAND3 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_4":
##                self.LMAX_BAND4 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_4":
##                self.LMIN_BAND4 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_5":
##                self.LMAX_BAND5 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_5":
##                self.LMIN_BAND5 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_6":
##                self.LMAX_BAND6 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_6":
##                self.LMIN_BAND6 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_7":
##                self.LMAX_BAND7 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_7":
##                self.LMIN_BAND7 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_8":
##                self.LMAX_BAND8 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_8":
##                self.LMIN_BAND8 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_9":
##                self.LMAX_BAND9 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_9":
##                self.LMIN_BAND9 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_10":
##                self.LMAX_BAND10 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_10":
##                self.LMIN_BAND10 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MAXIMUM_BAND_11":
##                self.LMAX_BAND11 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "RADIANCE_MINIMUM_BAND_11":
##                self.LMIN_BAND11 = line.split("=")[1].strip()
##            #min max reflectance
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_1":
##                self.LMAX_BAND1 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_1":
##                self.LMIN_BAND1 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_2":
##                self.LMAX_BAND2 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_2":
##                self.LMIN_BAND2 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_3":
##                self.LMAX_BAND3 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_3":
##                self.LMIN_BAND3 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_4":
##                self.LMAX_BAND4 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_4":
##                self.LMIN_BAND4 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_5":
##                self.LMAX_BAND5 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_5":
##                self.LMIN_BAND5 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_6":
##                self.LMAX_BAND6 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_6":
##                self.LMIN_BAND6 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_7":
##                self.LMAX_BAND7 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_7":
##                self.LMIN_BAND7 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_8":
##                self.LMAX_BAND8 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_8":
##                self.LMIN_BAND8 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_9":
##                self.LMAX_BAND9 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_9":
##                self.LMIN_BAND9 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_10":
##                self.LMAX_BAND10 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_10":
##                self.LMIN_BAND10 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MAXIMUM_BAND_11":
##                self.LMAX_BAND11 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "REFLECTANCE_MINIMUM_BAND_11":
##                self.LMIN_BAND11 = line.split("=")[1].strip()
##            #MIN MAX PIXEL VALUE
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_1":
##                self.QCALMAX_BAND1 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_1":
##                self.QCAQCALMIN_BAND1 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_2":
##                self.QCALMAX_BAND2 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_2":
##                self.QCALMIN_BAND2 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_3":
##                self.QCALMAX_BAND3 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_3":
##                self.QCALMIN_BAND3 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_4":
##                self.QCALMAX_BAND4 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_4":
##                self.QCALMIN_BAND4 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_5":
##                self.QCALMAX_BAND5 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_5":
##                self.QCALMIN_BAND5 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_6":
##                self.QCALMAX_BAND6 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_6":
##                self.QCALMIN_BAND6 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_7":
##                self.QCALMAX_BAND7 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_7":
##                self.QCALMIN_BAND7 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_8":
##                self.QCALMAX_BAND8 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_8":
##                self.QCALMIN_BAND8 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_9":
##                self.QCALMAX_BAND9 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_9":
##                self.QCALMIN_BAND9 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_10":
##                self.QCALMAX_BAND10 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_10":
##                self.QCALMIN_BAND10 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MAX_BAND_11":
##                self.QCALMAX_BAND11 = line.split("=")[1].strip()
##            if line.split("=")[0].strip()== "QUANTIZE_CAL_MIN_BAND_11":
##                self.QCALMIN_BAND11 = line.split("=")[1].strip()
            #REFLECTANCE MULTIPLICATIVE SCALING FACTOR
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_1":
                self.REFLECTANCE_MULT_BAND_1 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_2":
                self.REFLECTANCE_MULT_BAND_2 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_3":
                self.REFLECTANCE_MULT_BAND_3 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_4":
                self.REFLECTANCE_MULT_BAND_4 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_5":
                self.REFLECTANCE_MULT_BAND_5 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_6":
                self.REFLECTANCE_MULT_BAND_6 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_7":
                self.REFLECTANCE_MULT_BAND_7 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_8":
                self.REFLECTANCE_MULT_BAND_8 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_MULT_BAND_9":
                self.REFLECTANCE_MULT_BAND_9 = line.split("=")[1].strip()

            #additive scaling factors
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_1":
                self.REFLECTANCE_ADD_BAND_1 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_2":
                self.REFLECTANCE_ADD_BAND_2 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_3":
                self.REFLECTANCE_ADD_BAND_3 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_4":
                self.REFLECTANCE_ADD_BAND_4 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_5":
                self.REFLECTANCE_ADD_BAND_5 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_6":
                self.REFLECTANCE_ADD_BAND_6 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_7":
                self.REFLECTANCE_ADD_BAND_7 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_8":
                self.REFLECTANCE_ADD_BAND_8 = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "REFLECTANCE_ADD_BAND_9":
                self.REFLECTANCE_ADD_BAND_9 = line.split("=")[1].strip()



            #Projection Parameters
            if line.split("=")[0].strip()== "DATUM":
                self.REFERENCE_DATUM = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "ELLIPSOID":
                self.REFERENCE_ELLIPSOID = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "GRID_CELL_SIZE_REFLECTIVE":
                self.CELL_SIZE = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "MAP_PROJECTION":
                self.MAP_PROJECTION = line.split("=")[1].strip()
            if line.split("=")[0].strip()== "UTM_ZONE":
                self.UTM_ZONE = line.split("=")[1].strip()
        del line, rFile
    #end LANDSAT8_MTL
    def getJulianDay(self):
        date = self.AQUISITION_DATE
        (year,month,day) = date.split('-')
        year = int(year)
        month = int(month)
        day = int(day)
        t= time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        JulianDay = time.gmtime(t)[7]
        return JulianDay

#end Object
