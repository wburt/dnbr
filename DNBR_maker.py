'''

#--------------------------------------------------------------------------------------------
#Title: DNBR_maker.py
#Purpose: Calculates dNBR Raster
#Author:  WBurt
#Revision Date: January 5, 2010
#Requirements: ESRI ArcGIS 9.2 ArcInfo, ESRI Spatial Analyst extention
#Inputs:
#           1. Fire Perimeter file
#           2. pre Fire Image Folder
#           3. post Fire Image Folder
#           4. output Folder
#           5. output Raster Name
Revisions: gsmacgre Sept 2014
- Modified if statments to look for LANDSAT_5 and LANDSAT_7. MTL file reference has changed
-Band names in MTL have changed to e.g. FILE_NAME_BAND_4
#--------------------------------------------------------------------------------------------
'''
import os, sys, arcgisscripting,Landsat, math, shutil, barc_module, time,arcpy

gp = arcgisscripting.create()

firePerimeter = sys.argv[1]
preFireImageFolder = sys.argv[2]
postFireImageFolder = sys.argv[3]
outFolder = sys.argv[4]
outName = sys.argv[5]

print firePerimeter
print preFireImageFolder
print postFireImageFolder
print outFolder
print outName

time.sleep(1)

try:

    inBands = r"4;7"

    #1 - Buffer and project fire boundary
    #2 - Clip input, output images
    #3 - TOA on input, output
    #4 - BARC
    #5 - Clip BARC to fire boundary
    #6 - slice BARC

    #Gather file information, metadata and move images to workspace
    #discover metadata files
    searchFolder = preFireImageFolder
    searchString = "_MTL.txt"
    fileList = os.listdir(searchFolder)

    for file in fileList:
        if not os.path.isdir(os.path.join(searchFolder,file)) and file.find(searchString) > -1:
            mtlFile = os.path.join(searchFolder,file)
    satellitepre = barc_module.get_Satellite_Type(mtlFile)
    # Read metadata for before image
    if satellitepre == 'LANDSAT_8':
        PRE_MTL = Landsat.Landsat8_MTL(mtlFile)
    elif satellitepre == 'LANDSAT_5':
        PRE_MTL = Landsat.TM_MTL(mtlFile) # create metadata object\
    elif satellitepre == 'LANDSAT_7':
        PRE_MTL = Landsat.TM_MTL(mtlFile)
    print 'The pre satellite is ' + satellitepre
    
    #read metadata for after image
    searchFolder = postFireImageFolder
    searchString = "_MTL.txt"
    fileList = os.listdir(searchFolder)
    for file in fileList:
        if not os.path.isdir(os.path.join(searchFolder,file)) and file.find(searchString) > -1:
            mtlFile = os.path.join(searchFolder,file)
    satellitepost = barc_module.get_Satellite_Type(mtlFile)
    # Read metadata for before image
    if satellitepost == 'LANDSAT_8':
        POST_MTL = Landsat.Landsat8_MTL(mtlFile)
    elif satellitepost == 'LANDSAT_5':
        POST_MTL = Landsat.TM_MTL(mtlFile) # create metadata object\
    elif satellitepost == 'LANDSAT_7':
        POST_MTL = Landsat.TM_MTL(mtlFile)
    print 'The post satellite is ' + satellitepost
    
    if satellitepre in['LANDSAT_5','LANDSAT_7']:
        preBand4 = PRE_MTL.BAND4_FILE_NAME.strip('\"')
        preBand7 = PRE_MTL.BAND7_FILE_NAME.strip('\"')
    if satellitepost in['LANDSAT_5','LANDSAT_7']:
        postBand4 = POST_MTL.BAND4_FILE_NAME.strip('\"')
        postBand7 = POST_MTL.BAND7_FILE_NAME.strip('\"')
    if satellitepre == 'LANDSAT_8':
        preBand4 = PRE_MTL.BAND5_FILE_NAME.strip('\"')
        preBand7 = PRE_MTL.BAND7_FILE_NAME.strip('\"')
    if satellitepost == 'LANDSAT_8':
        postBand4 = POST_MTL.BAND5_FILE_NAME.strip('\"')
        postBand7 = POST_MTL.BAND7_FILE_NAME.strip('\"')

    #get projection of the input images
    preSR = gp.describe(os.path.join(preFireImageFolder, preBand4)).SpatialReference
    postSR = gp.describe(os.path.join(preFireImageFolder, preBand4)).SpatialReference
    varpreSR = preSR.name
    varpostSR = postSR.name
    
    #make projections the same
    if preSR.name != postSR.name:
        preBand4 = gp.ProjectRaster_management(os.path.join(preFireImageFolder, preBand4),os.path.join(outFolder, preBand4[0:-4]))
        preBand7 = gp.ProjectRaster_management(os.path.join(preFireImageFolder, preBand7),os.path.join(outFolder, preBand7[0:-4]))
        postBand4 = os.path.join(postFireImageFolder, postBand4)
        postBand7 = os.path.join(postFireImageFolder, postBand7)
    else:
        postBand4 = os.path.join(postFireImageFolder, postBand4)
        postBand7 = os.path.join(postFireImageFolder, postBand7)
        preBand4 = os.path.join(preFireImageFolder, preBand4)
        preBand7 = os.path.join(preFireImageFolder, preBand7)

    #get projection of fire perimeter
    fireSR = gp.describe(firePerimeter).SpatialReference
    varfire = fireSR.name
    #project to be same as imagery if needed

    if fireSR.name != postSR.name:
        transform_method = barc_module.get_transformation_default(fireSR, postSR)
        if transform_method == 0:
            gp.adderror("Can't find transform method for an unknown spheriod")
            print "Can't find transform method for an unknown spheriod"
        else:
            firePerimeter = gp.Project_management(firePerimeter, os.path.join(outFolder, "DNBR_perimeter.shp"), postSR)
            #firePerimeter = gp.Project_management(firePerimeter, os.path.join(outFolder, "perimeter.shp"), postSR, transform_method)
    else:
        firePerimeter = gp.Copy_management(firePerimeter, os.path.join(outFolder, "DNBR_perimeter.shp"))
except:
    gp.adderror(gp.getmessages())
    gp.adderror("Failed Perimeter Reprojection")
    sys.exit(0)
    #clip images to fire perimeter buffer -output to outFolder
    #buffer the fire envelope
try:
    fEnv = gp.describe(firePerimeter).extent.split(" ")
    fEnvBuf = ""
    fEnvBuf = str(math.floor(float(fEnv[0])) - 1000) + " " + str(math.floor(float(fEnv[1])) - 1000)\
              + " " + str(math.floor(float(fEnv[2])) + 1000) + " " + str(math.floor(float(fEnv[3])) + 1000)
    fEnvBuf = fEnvBuf.strip()
    gp.XYDomain = fEnvBuf
    preBand4 = gp.Clip_Management(preBand4, gp.XYDomain, os.path.join(outFolder, os.path.basename(preBand4)))
    preBand7 = gp.Clip_Management(preBand7, gp.XYDomain, os.path.join(outFolder, os.path.basename(preBand7)))
    postBand4 = gp.Clip_Management(postBand4, gp.XYDomain, os.path.join(outFolder, os.path.basename(postBand4)))
    postBand7 = gp.Clip_Management(postBand7, gp.XYDomain, os.path.join(outFolder, os.path.basename(postBand7)))
except:
    gp.adderror("Failed image clip to fire envelope")
    gp.adderror(gp.getmessages())
    sys.exit(0)
try:
    #copy metadata
    shutil.copy(PRE_MTL.mtlTxt, outFolder)
    PRE_MTL_TXT = os.path.join(outFolder, os.path.basename(PRE_MTL.mtlTxt))
    shutil.copy(POST_MTL.mtlTxt, outFolder)
    POST_MTL_TXT = os.path.join(outFolder, os.path.basename(POST_MTL.mtlTxt))
    #run TOA
    #preSense = PRE_MTL.SPACECRAFT[1:-1]
    #postSense = POST_MTL.SPACECRAFT[1:-1]
    if satellitepre == 'LANDSAT_8':# and preSense == 'LANDSAT_8':
        barc_module.image_toa(outFolder, PRE_MTL_TXT, outFolder,  "5;7")
    if satellitepost == 'LANDSAT_8':# and postSense == 'LANDSAT_8':
        barc_module.image_toa(outFolder, POST_MTL_TXT, outFolder, "5;7")
    if satellitepre in ['LANDSAT_5', 'LANDSAT_7']:# and preSense in ['LANDSAT_5', 'LANDSAT_7']:
        barc_module.image_toa(outFolder, PRE_MTL_TXT, outFolder,  "4;7")
    if satellitepost in ['LANDSAT_5', 'LANDSAT_7']:# and postSense in ['LANDSAT_5', 'LANDSAT_7']:
        barc_module.image_toa(outFolder, POST_MTL_TXT, outFolder, "4;7")
        
    #run dNBR
    PathRow = PRE_MTL.PATH + "0" + PRE_MTL.ROW
    #Create object class

    barc_module.calculate_dnbr(preBand4[:-4] + "_TOAR" + preBand4[-4:], preBand7[:-4] + "_TOAR" + preBand7[-4:],\
                    postBand4[:-4] + "_TOAR" + postBand4[-4:], postBand7[:-4] + "_TOAR" + postBand7[-4:], \
                    os.path.join(outFolder, outName))
    #write metadata
    metaFile = os.path.basename(outName).split(".")[0] + "_meta.txt"
    meta = barc_module.Metadata(outFolder, metaFile)
    meta.preFireImageDate = PRE_MTL.AQUISITION_DATE
    meta.preFireSensor = PRE_MTL.SENSOR_ID
    meta.preFirePathRow = PRE_MTL.PATH + "/" + PRE_MTL.ROW
    meta.postFireSensor = POST_MTL.SENSOR_ID
    meta.postFireImageDate = POST_MTL.AQUISITION_DATE
    meta.postFirePathRow = POST_MTL.PATH + "/" + POST_MTL.ROW
    meta.dateasetProjection = POST_MTL.MAP_PROJECTION
    #meta.UTMzone = POST_MTL.UTM_ZONE Not working for some reason
    meta.spheroid = POST_MTL.REFERENCE_DATUM
    meta.DNBRfile = os.path.join(outFolder, outName)
    meta.BARClow = ""
    meta.BARCmod = ""
    meta.BARChigh = ""
    meta.write()

except:
    gp.adderror("Failed TOA/DNBR calculations")
    gp.adderror(gp.getmessages())
    sys.exit(0)

#Clean up
gp.delete(preBand4[:-4] + "_TOAR" + preBand4[-4:])
gp.delete(preBand4)
gp.delete(preBand7[:-4] + "_TOAR" + preBand7[-4:])
gp.delete(preBand7)
gp.delete(postBand4[:-4] + "_TOAR" + postBand4[-4:])
gp.delete(postBand4)
gp.delete(postBand7[:-4] + "_TOAR" + postBand7[-4:])
gp.delete(postBand7)
gp.workspace = outFolder
rl = gp.ListRasters("g_g_g*")
r = rl.next()
while r:
    gp.delete(r)
    r = rl.next()

print "done cleanup"
#end

