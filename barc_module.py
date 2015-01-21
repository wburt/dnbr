#W:\FOR\RSI\RSI\Projects\RGG\2009\037_Burn_Severity_Mapping\scripts\python
#--------------------------------------------------------------------------------------------
#Title: barc_module.py
#Purpose: Contains Functions for calculating Burn Severity Classification using USGS landsat TM 5
#Author:  WBurt
#Revision Date: October 21, 2009
#Requirements: Landsat.py, ESRI ArcGIS 9.2 ArcInfo, ESRI Spatial Analyst extention
#Inputs:
#           1. Folder path containing USGS processed imagery and metadata file
#           2. Metatadata (MTL) file - full path
#           3. Band numbers to be processed (string semi-colon deliminated) ie. "'4';'7'"
#           4. Output folder path
#--------------------------------------------------------------------------------------------
#Revision Date June, 2013
#Revisions:  Added Landsat 8 TOA functions and ability to defferentiate between satellites
#           Added Landsat 8 MTL reading functions to Landsat.py
# Sept 2014 gsmacgre Modified arcpy.sa to just sa and import sa extension
#


import Landsat
import os
import os.path
import sys
import arcgisscripting
import math
import time
import arcpy
from arcpy import sa


# Create the Geoprocessor object
gp = arcgisscripting.create()
arcpy.CheckOutExtension("Spatial")
gl_inraster_dict = {}
#main TOA function
def image_toa(inPath, inMTL,  outPath, strBandList = "4;7"):
    #Calculates Top of Atmosphere for Landsat TM5 image contained in folder inPath having metadatafile inMTL
    #for bands in strBandList default = "4;7", corrected imagery writen to outpath
    #Start
    global gl_inraster_dict
    outFile = inMTL #the full file location of the MTL file
    bandList = strBandList.split(";")
    #exception if band 6 is attempted
    if '6' in bandList:
        gp.adderror("This Script does not calculate TOA for Band 6")
        print "This Script does not calculate TOA for Band 6"
        sys.exit(0)
    #only process bands in this list
    for band in bandList:
        if band not in ['1','2','3','4','5','7']:
            gp.adderror('Input band [' + band + '] out of range')
            sys.exit(1)

    # Read metadata
    satellite = get_Satellite_Type(inMTL)
    if satellite == 'LANDSAT_8':
        MTL = Landsat.Landsat8_MTL(inMTL)
    elif satellite == 'LANDSAT_5':
        MTL = Landsat.TM_MTL(outFile) # create metadata object\
    elif satellite == 'LANDSAT_7':
        MTL = Landsat.TM_MTL(outFile)

    #Constants
    if satellite in ['LANDSAT_5', 'LANDSAT_7']:
        # TM5/7 ESUN - Exoatmospheric spectral irradiances post 2003
        sensor = MTL.SENSOR_ID.strip("\"")
        if sensor == "TM":
            ESUN_dict = {'1':1957, '2':1826, '3':1554, '4':1036, '5':215, '7':80.67}
        elif sensor == "ETM+":
            ESUN_dict = {'1':1969, '2':1840, '3':1551, '4':1044, '5':225, '7':82.07}
        elif sensor == "ETM":
            ESUN_dict = {'1':1969, '2':1840, '3':1551, '4':1044, '5':225, '7':82.07}

        lmax_dict = {'1':MTL.LMAX_BAND1.strip('\"'), '2':MTL.LMAX_BAND2.strip('\"'), \
                         '3':MTL.LMAX_BAND3.strip('\"'), '4':MTL.LMAX_BAND4.strip('\"'), \
                         '5':MTL.LMAX_BAND5.strip('\"'), '7':MTL.LMAX_BAND7.strip('\"')}
        lmin_dict = {'1':MTL.LMIN_BAND1.strip('\"'), '2':MTL.LMIN_BAND2.strip('\"'), \
                         '3':MTL.LMIN_BAND3.strip('\"'), '4':MTL.LMIN_BAND4.strip('\"'), \
                         '5':MTL.LMIN_BAND5.strip('\"'), '7':MTL.LMIN_BAND7.strip('\"')}
        qcalmax_dict = {'1':MTL.QCALMAX_BAND1.strip('\"'), '2':MTL.QCALMAX_BAND2.strip('\"'), \
                         '3':MTL.QCALMAX_BAND3.strip('\"'), '4':MTL.QCALMAX_BAND4.strip('\"'), \
                         '5':MTL.QCALMAX_BAND5.strip('\"'), '7':MTL.QCALMAX_BAND7.strip('\"')}


    inraster_dict = {'1':MTL.BAND1_FILE_NAME.strip('\"'), '2':MTL.BAND2_FILE_NAME.strip('\"'), \
                     '3':MTL.BAND3_FILE_NAME.strip('\"'), '4':MTL.BAND4_FILE_NAME.strip('\"'), \
                     '5':MTL.BAND5_FILE_NAME.strip('\"'), '7':MTL.BAND7_FILE_NAME.strip('\"')}
    gl_inraster_dict = inraster_dict

    # Set workspace
    gp.workspace = inPath

    #sub TOA function
    def calculate_TOAR(outPath, BAND): # For use by IMAGE_TOA only
        #Calculates Top of Atmosphere Reflectance for USGS processed TM5 imagery with MTL metadata file
        #Band to process
        #exec("inRaster = MTL.BAND" + BAND + "_FILE_NAME.strip('\"')")
        global gl_inraster_dict
        inRaster = gl_inraster_dict.get(BAND)
        try:
            # Set the output raster name for Radiance calculation
            outRasterRAD = inRaster[:-4] + "_RAD" + ".IMG"
            outRasterRAD = os.path.join(outPath, outRasterRAD)
            # Set the output raster name for TOA calculation
            outRasterTOAR = inRaster[:-4] + "_TOAR" + ".TIF"
            outRasterTOAR = os.path.join(outPath, outRasterTOAR)
            # Check out Spatial Analyst extension license
            gp.CheckOutExtension("Spatial")
            #Conversion to Radiance
            #exec("LMAX = MTL.LMAX_BAND" + BAND + ".strip()")
            LMAX = lmax_dict.get(BAND)
            #exec("LMIN = MTL.LMIN_BAND" + BAND + ".strip()")
            LMIN = lmin_dict.get(BAND)
            #exec("QCALMAX = MTL.QCALMAX_BAND" + BAND + ".strip()")
            QCALMAX = qcalmax_dict.get(BAND)
            # Process: Create Constant Raster
            r0 = (float(LMAX) - float(LMIN))/float(QCALMAX) #calculation factor

            # expression to calculate at-sensor spectral radiance
            #saExpRAD = "(" + str(r0) + " * " + inRaster + ") + (" + LMIN + ")"

            #Calculate TOA Reflectance
            #Calulate the Julian Day
            JD = MTL.getJulianDay()
            #-- Calculate earth sun distance REF - http://earth.esa.int/pub/ESA_DOC/landsat_FAQ/#_Toc235345965
            d = 1/(1-0.016729* math.cos(0.9856*(JD - 4)))
            d0 = 1/d #sun-earth distance in astronomical units
            #product portion of equation
            p1 = math.pi * pow(float(d0),2) #top of equation
            #quotiant portion of equation
            q1 = ESUN_dict.get(BAND) * math.sin(math.radians(float(MTL.SUN_ELEVATION)))#bottom of equation
            # Expression to apply to raster - scale by 400
            #saExpTOAR = "((" + str(p1) + " * " + outRasterRAD + ") / " + str(q1) + ") * 400"  #1/0.00255 scales the image to 1-255
            print "Calculating Radiance... Band " + BAND
            #gp.SingleOutputMapAlgebra_sa(saExpRAD, outRasterRAD)
            print "Calculating TOA Reflectance... Band " + BAND
            #gp.SingleOutputMapAlgebra_sa(saExpTOAR, outRasterTOAR)
            outRadRaster = (r0 * sa.Raster(inRaster)) + float(LMIN)
            outToaRaster = ((p1 * (outRadRaster)) / q1) * 400
            outToaRaster.save(outRasterTOAR)
            #gp.delete(outToaRaster)
            print "done TOA"

        except:
            # If an error occurred while running a tool, then print the messages
            print gp.addmessage(gp.GetMessages())

    def calculate_OLI_TOA(outPath,BAND):
        global gl_inraster_dict
        inRaster = gl_inraster_dict.get(BAND)
        outRasterTOAR = inRaster[:-4] + "_TOAR" + ".TIF"
        outRasterTOAR = os.path.join(outPath, outRasterTOAR)

        try:
            #multiplicative rescaling factor
            Mp_Dict = {'1':MTL.REFLECTANCE_MULT_BAND_1,'2':MTL.REFLECTANCE_MULT_BAND_2,'3':MTL.REFLECTANCE_MULT_BAND_3,\
            '4':MTL.REFLECTANCE_MULT_BAND_4,'5':MTL.REFLECTANCE_MULT_BAND_5,'6':MTL.REFLECTANCE_MULT_BAND_6,\
            '7':MTL.REFLECTANCE_MULT_BAND_7,'8':MTL.REFLECTANCE_MULT_BAND_8,'9':MTL.REFLECTANCE_MULT_BAND_9}
            #additive rescaling factor dictionary
            Ap_Dict = {'1':MTL.REFLECTANCE_ADD_BAND_1,'2':MTL.REFLECTANCE_ADD_BAND_2,'3':MTL.REFLECTANCE_ADD_BAND_3,\
            '4':MTL.REFLECTANCE_ADD_BAND_4,'5':MTL.REFLECTANCE_ADD_BAND_5,'6':MTL.REFLECTANCE_ADD_BAND_6,\
            '7':MTL.REFLECTANCE_ADD_BAND_7,'8':MTL.REFLECTANCE_ADD_BAND_8,'9':MTL.REFLECTANCE_ADD_BAND_9}
            #create TOA
            arcpy.env.overwriteOutput = 1
            toaRaster = ((float(Mp_Dict.get(BAND)) * sa.Raster(inRaster)) + float(Ap_Dict.get(BAND)))/math.sin(math.radians(float(MTL.SUN_ELEVATION)))
            toaRaster.save(outRasterTOAR)
            print 'Done OLI TOA'
        except:
            print 'OLI TOA ERROR'

    # Calculate TOA for each band
    for band in bandList:
        gp.addmessage("Calculating reflectance for Band " + band)

        try:
            if satellite in ['LANDSAT_5', 'LANDSAT_7']:
                calculate_TOAR(outPath, band)
            elif satellite == 'LANDSAT_8':
                calculate_OLI_TOA(outPath, band)
        except:
            gp.adderror("Failed Band " + band)
            gp.adderror(gp.getmessages())
            sys.exit(1)
            
    #main dNBR function
def calculate_dnbr(imgT1Band4, imgT1Band7, imgT2Band4, imgT2Band7, out):

        #Calculates the differenced normalized burn ratio for top of atmosphere
        #corrected landsat 5 images.
        outFile = out

        #set temp workspace
        gp.overwriteoutput = 1
        gp.workspace = "T:/"

        #process T1 and T2
        gp.addmessage("Starting DNBR processing...")
        imgT1 = [imgT1Band4, imgT1Band7]
        imgT2 = [imgT2Band4, imgT2Band7]
        imgList = [imgT1, imgT2]
        x = 1
        for img in imgList:
            T1NIR = img[0]
            T1SWIR = img[1]
            T2NIR = img[0]
            T2SWIR =  img[1]
            TxP1 = "T" + str(x) + "P1"
            TxP2 = "T" + str(x) + "P2"
            TxP3 = "T" + str(x) + "NBR"
            if x == 1:
                # Calculate NIR - SWIR
                gp.minus_sa(T1NIR, T1SWIR, TxP1)
                # Calculate NIR + SWIR
                gp.plus_sa(T1NIR, T1SWIR, TxP2)
            if x == 2:
                # Calculate NIR - SWIR
                gp.minus_sa(T2NIR, T2SWIR, TxP1)
                # Calculate NIR + SWIR
                gp.plus_sa(T2NIR, T2SWIR, TxP2)
            #convert to floating point
            TxP1f = gp.float_sa(TxP1, TxP1 + "f")
            TxP2f = gp.float_sa(TxP2, TxP2 + "f")
            #divide (NIR - SWIR) / (NIR + SWIR)
            TxP3f = gp.divide_sa(TxP1f,TxP2f,TxP3)
            #clean up intermediates
            gp.delete(TxP1)
            gp.delete(TxP2)
            gp.delete(TxP1f)
            gp.delete(TxP2f)
            x = x + 1

        #Calculate dBR
        #dNBR = T1BR - T2BR
        gp.minus_sa("T1NBR","T2NBR","DiffNBR")
        DNBR = "DiffNBR"
        DNBR2 = "ScaleDNBR2"

        #scale the DNBR
        saExpr = "(" + DNBR + " * 1000 + 275) / 5"
        gp.SingleOutputMapAlgebra_sa(saExpr, DNBR2)
        DNBR3 = "ScaleDNBR3"
        gp.int_sa(DNBR2,out)

        gp.addmessage("\t...done")
        gp.addmessage("Cleaning up...")

        #cleanup
        gp.delete("T1NBR")
        gp.delete("T2NBR")
        gp.delete(DNBR)
        gp.delete(DNBR2)
        gp.addmessage("\t...done")
        print "complete"


def get_Satellite_Type(mtlFile):
    f = open(mtlFile,'r')
    for line in f:
        if line.split('=')[0].strip() == 'SPACECRAFT_ID':
            satelliteType = line.split('=')[1].strip().strip('"')
    f.close()
    return satelliteType

def get_transformation_default(from_sr, to_sr):
    #determines transformation method for gp.project_management tool
    #Spatial Reference Name : Spheroid
    transformation_dict = {'NAD_1983_BC_Environment_Albers':'NAD_1983', 'BCAlbers83': 'NAD_1983', \
                           'NAD_1983_Albers':'NAD_1983','PCS_Albers': 'NAD_1983', \
                           'NAD_1983_UTM_Zone_11N': 'NAD_1983', 'NAD_1983_UTM_zone_11N': 'NAD_1983',\
                           'NAD_1983_UTM_Zone_10N': 'NAD_1983', 'NAD_1983_UTM_Zone_9N':'NAD_1983', 'NAD_1983_UTM_zone_10N': 'NAD_1983',\
                           'NAD_1983_UTM_Zone_8N': 'NAD_1983', 'GCS_WGS_1984': 'WGS_1984', \
                           'WGS_1984_UTM_Zone_11N': 'WGS_1984', 'WGS_1984_UTM_Zone_10N': 'WGS_1984','WGS_1984_UTM_zone_10N': 'WGS_1984','WGS_1984_UTM_zone_11N': 'WGS_1984',\
                           'WGS_1984_UTM_Zone_9N': 'WGS_1984', 'WGS_1984_UTM_Zone_8N': 'WGS_1984', 'WGS_1984_UTM_zone_9N': 'WGS_1984',\
                           'WGS_1984_UTM_Zone_7N': 'WGS_1984'}

    from_sphere = transformation_dict.get(from_sr.Name)
    to_sphere = transformation_dict.get(to_sr.Name)
    if from_sphere != to_sphere:
        if from_sphere in ['NAD_1983', 'WGS_1984'] and to_sphere in ['NAD_1983', 'WGS_1984']:
            return 'NAD_1983_To_WGS_1984_1'
        else:
            return 0 #spheriod not in dictionary
    else:
        return '' #spheroids identicle no transformation nessasary.

def get_raster_min_max(strRaster):
    #returns list [min,max] of input raster
    image = r"T:\TOA\45025_dNBR.tif"
    rows = gp.SearchCursor(image)
    row = rows.next()
    values = []
    while row:
        a_tup = (row.VALUE, row.COUNT)
        values.append(a_tup)
        row = rows.next()
    image_dict = dict(values)
    min = 999999999
    max = -99999999
    sum = 0
    count = 0
    for key in image_dict.keys():
        if key < min:
            min = key
        if key > max:
            max = key
        sum = sum + key * image_dict.get(key)
        count = count + image_dict.get(key)
    return [min, max]

class Metadata:
    #This class contains methods to create and maintain a metadata file for BARC mapping

    def __init__(self, outputFolder, fileName):
        '''This is the constructor method for metaData Class
        outputFolder   - the folder in which the metadata will be written
        fileName       - the name of the metadata file
        '''
        self.metadata = [] #metadata dictionary
        self.mText = []
        tStart = time.localtime() #the time the object was created
        self.doc = os.path.join(outputFolder,fileName) #metadata file
        self.description = 'These data products are derived from \
Landsat Thematic Mapper data. The pre-fire and post-fire subsets included \
were used to create a differenced Normalized Burn Ratio (dNBR) image.  The \
dNBR image attempts to portray the variation of burn severity within a fire.\
The severity ratings are influenced by the effects to the canopy.  The \
severity rating is based upon a composite of the severity to the understory \
(grass, shrub layers), midstory trees and overstory trees.  Because there is \
often a strong correlation between canopy consumption and soil effects, this \
algorithm works in many cases for teams whose objective is a soil burn \
severity assessment.  It is not, however, appropriate in all ecosystems or \
fires.' #heading for metadata file
        self.purpose = 'These data were created by the BC MFR\
Geomatics to support Post Wildfire Risk Assements' #product purpose
        self.creationDate = str(tStart.tm_hour) + ':' + str(tStart.tm_min) + ' ' + \
        str(tStart.tm_mday) + '-' + str(tStart.tm_mon) + '-' + str(tStart.tm_year)
        self.author = os.environ.get("USERNAME") #gis operator
        self.modifiedDate = "" # Date of last modification
        self.modifiedAuthor = "" # Author of last modification
        self.preFireImageDate = "" #Image date for before fire image
        self.preFirePathRow = "" #Path/Row of prefire image
        self.postFirePathRow = "" #Path/Row of postfire image
        self.postFireImageDate = "" #Image date for after fire image
        self.preFireSensor = "" #before fire image sensor (ETM, TM)
        self.postFireSensor = "" #after fire image sensor (ETM, TM)
        self.perimeterArea = "" #area of fire
        self.datasetProjection = ""
        self.UTMzone = ""
        self.spheroid = ""
        self.DNBRfile = "" #DNBR file name
        self.BARCfile = "" #BARC file name
        self.BARClastUpdated = "" #date of last BARC update
        self.BARCcalibration = "" #True if BARC calibrated with ground truthing
        self.BARClow = 76 #Unburned/Low severity dnbr breakpoint (default = 76)
        self.BARCmod = 110 #Low/Moderate severity dnbr breakpoint (default = 110)
        self.BARChigh = 187 #Moderate/high severity dnbr breakpoint (default = 187)
        self.classDisc = '''\n\tUnchanged:    This means the area after the fire was\
indistinguishable from pre-fire conditions. This does not always indicate the \
area did not burn.\n\t\
Low:    This severity class represents areas of surface fire with little change \
in cover and little change in cover and mortality of the dominant vegetation.\n\t\
Moderate:    This severity class is between low and high and means there is a \
mixture of effects on the dominant vegetation.\n\t\
High:    This severity class represents areas where the canopy has high to complete consumption.'''
        self.__load() # This will load up existing metadata if it exists
    def __build(self):
        # Builds a list of metadata fields and values
        self.metadata.append(['DESCRIPTION', self.description])
        self.metadata.append(['PURPOSE', self.purpose])
        self.metadata.append(['CREATION DATE', self.creationDate])
        self.metadata.append(['CREATED BY', self.author])
        self.metadata.append(['MODIFIED DATE', self.modifiedDate])
        self.metadata.append(['MODIFYING AUTHOR', self.modifiedAuthor])
        self.metadata.append(['PRE-FIRE SENSOR', self.preFireSensor])
        self.metadata.append(['PRE-FIRE IMAGE DATE', self.preFireImageDate])
        self.metadata.append(['PRE-FIRE PATH/ROW', self.preFirePathRow])
        self.metadata.append(['POST-FIRE SENSOR', self.postFireSensor])
        self.metadata.append(['POST-FIRE IMAGE DATE', self.postFireImageDate])
        self.metadata.append(['POST-FIRE PATH ROW', self.postFirePathRow])
        self.metadata.append(['DATASET PROJECTION', self.datasetProjection])
        self.metadata.append(['UTM ZONE', self.UTMzone])
        self.metadata.append(['SPHEROID', self.spheroid])
        self.metadata.append(['FIRE HECTARES', self.perimeterArea])
        self.metadata.append(['DNBR FILE NAME', self.DNBRfile])
        self.metadata.append(['BARC FILE NAME', self.BARCfile])
        self.metadata.append(['BARC CREATION DATE', self.BARClastUpdated])
        self.metadata.append(['BARC CALIBRATION', self.BARCcalibration])
        self.metadata.append(['LOW DNBR MIN', self.BARClow])
        self.metadata.append(['MODERATE DNBR MIN', self.BARCmod])
        self.metadata.append(['HIGH DNBR MIN', self.BARChigh])
        self.metadata.append(['BARC DESCRIPTIONS', self.classDisc])

        for i in self.metadata:
            self.mText.append(str(i[0]) + ' :: ' + str(i[1]) + '\n')
        print 'metadata built'
    def __load(self):
        #loads and populates updatable metadata fields
        if os.path.exists(self.doc):
            metaDict = {}
            f = open(self.doc, 'r')
            prevKey = ""
            for line in f.readlines():
                try:
                    k, v = line.split("::")
                except: # split fails where "::" does not exist in line
                    k = prevKey
                    v = metaDict[k] + line
                k = k.strip()
                v = v.strip()
                metaDict[k] = v
                prevKey = k
            f.close()
            #populate self
            self.creationDate = metaDict['CREATION DATE']
            self.author = metaDict['CREATED BY']
            self.preFireSensor = metaDict['PRE-FIRE SENSOR']
            self.preFireImageDate = metaDict['PRE-FIRE IMAGE DATE']
            self.preFirePathRow = metaDict['PRE-FIRE PATH/ROW']
            self.postFireSensor = metaDict['POST-FIRE SENSOR']
            self.postFireImageDate = metaDict['POST-FIRE IMAGE DATE']
            self.postFirePathRow = metaDict['POST-FIRE PATH ROW']
            self.datasetProjection = metaDict['DATASET PROJECTION']
            self.UTMzone = metaDict['UTM ZONE']
            self.spheroid = metaDict['SPHEROID']
            self.perimeterArea = metaDict['FIRE HECTARES']
            self.DNBRfile = metaDict['DNBR FILE NAME']
            self.BARCfile = metaDict['BARC FILE NAME']
            self.BARClastUpdated = metaDict['BARC CREATION DATE']
            self.BARCcalibration = metaDict['BARC CALIBRATION']
            self.BARClow = metaDict['LOW DNBR MIN']
            self.BARCmod = metaDict['MODERATE DNBR MIN']
            self.BARChigh = metaDict['HIGH DNBR MIN']

    def write(self):
        #writes metadata to txt file
        self.__build()
        afile = open(self.doc, "w")
        afile.writelines(self.mText)
        afile.close()
    #end class Metadata

#mtlFile =r"W:\FOR\RSI\RSI\Projects\RGG\2009\037_Burn_Severity_Mapping\data\Source\Landsat8Test\LC80440252013106LGN01_MTL.txt"
#mtl = Landsat.Landsat8_MTL(mtlFile)
#oPath = r"T:/"
#print get_Satellite_Type(mtlFile)
#image_toa("T:/test/oli","T:/test/oli/LC80440252013106LGN01_MTL.txt","T:/test/output","5;7")