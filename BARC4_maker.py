# HELLO.PY
# Slices raster into classes, simplifies and exports to polygon
# Author:  Wburt
# Last Revision: November 4, 2009
''' inputs  1 - output folder as string
            2 - input raster full path and name (ie DNBR)
            3 - output file name and path for classification result
            4 - Fire perimeter file created by DNBR maker
            5 - break values at which to classify the input with. Semi-colon separated values as string
                Default should be '75;109;187'
            6 - calibration indicator True False
'''

import os, sys, arcgisscripting,Landsat, math, shutil, subprocess, barc_module, time,arcpy
gp = arcgisscripting.create()
gp.CheckOutExtension("Spatial")

gp.workspace = sys.argv[1] # output folder
inRaster = sys.argv[2] # input Raster #full path and name
outPoly = sys.argv[3] # output polygon #full path and name
perimeter = sys.argv[4] #fire perimeter created by DNBR maker
breakValues = sys.argv[5] # BreakValues, if none then use Natural Breaks else use semi-colon separated break points.
calibration = sys.argv[6] # TRUE or FALSE : The breaklist values are calibrated by field data

def get_min_max(raster): #returns list [min, max]
    rastObj = arcpy.Raster(raster)
    min = rastObj.minimum
    max = rastObj.maximum
    return min, max
def main(workspace, inRaster, outPoly, breakValues = ""):
    try:
        outRaster = os.path.basename(outPoly)[0:-4] + ".tif"
        if breakValues != "": #no break values provided
            min, max = get_min_max(inRaster)
            breakList = breakValues.split(";")
            breakStr = str(min)
            for i, value in enumerate(breakList):
                print i+1, value
                if i == 0:
                    breakStr = breakStr + " " + str(value) + " " + str(i + 1)
                else:
                    breakStr =  breakStr + ";" + str(int(breakList[i-1]) + 1) + " " + str(value) + " " + str(i + 1)
            breakStr = breakStr + ";" + str(breakList[-1]) + " " + str(max) + " " + str(len(breakList)+1)
            outRaster2 = gp.CreateUniqueName(inRaster, gp.workspace)
            gp.Reclassify_sa(inRaster, "Value", breakStr, outRaster2, "DATA")
        else: #build string from break values
            outRaster2 = gp.CreateUniqueName(inRaster, gp.workspace)
            gp.slice_sa(inRaster, outRaster2, 4, "NATURAL_BREAKS",1)
    except:
        print "failed reclassification"
        gp.adderror("failed reclassification")
        print gp.getmessages()

    try: #simplify Raster
        outRaster3 = gp.CreateUniqueName(outRaster2, gp.workspace)
        gp.RegionGroup_sa(outRaster2, outRaster3, "FOUR", "WITHIN","ADD_LINK")
        outRaster4 = gp.CreateUniqueName(outRaster3, gp.workspace)
        gp.SetNull_sa(outRaster3, outRaster3, outRaster4, "\"COUNT\" < 10")
        gp.Nibble_sa(outRaster2, outRaster4, outRaster, "DATA_ONLY")

    except:
        print "failed raster simplification"
        gp.adderror("failed raster simplification")
        print gp.getmessages()
        if gp.exists(outRaster2):
            gp.delete(outRaster2)
        if gp.exists(outRaster3):
            gp.delete(outRaster3)
        if gp.exists(outRaster4):
            gp.delete(outRaster4)
        sys.exit(0)

    try: #cleanup
        if gp.exists(outRaster2):
            gp.delete(outRaster2)
        if gp.exists(outRaster3):
            gp.delete(outRaster3)
        if gp.exists(outRaster4):
            gp.delete(outRaster4)
        #delete temp rasters
        rl = gp.ListRasters("g_g_g*")
        r = rl.next()
        while r:
            gp.delete(r)
            r = rl.next()
        #done cleanup
    except:
        print "failed cleanup"
        gp.adderror("failed cleanup")
        print gp.getmessages()
    try: # create polygons
        outPoly1 = gp.RasterToPolygon_conversion(outRaster, "rast2poly_temp.shp", "SIMPLIFY")
        inPoly = outPoly1
    except:
        print "failed raster to polygon conversion"
        gp.adderror("failed raster to polygon conversion")
        print gp.getmessages()

    try:
        gp.AddField_management(inPoly, "BurnSev", "TEXT","" , "", 20)
    except:
        gp.adderror(gp.getmessages())
    pyTxt = "def getclass(GRIDCODE):\n\
        if GRIDCODE == 4: \n\
            return \"High\" \n\
        elif GRIDCODE == 3:\n\
            return \"Medium\"\n\
        elif GRIDCODE == 2:\n\
            return \"Low\"\n\
        elif GRIDCODE == 1:\n\
            return \"Unburned\""
    try:
        gp.CalculateField_management(inPoly, "BurnSev", "getclass(!GRIDCODE!)", "PYTHON", pyTxt)
    except:
        print gp.getmessages()
        gp.adderror(gp.getmessages())
    try:
        gp.Clip_analysis(inPoly, perimeter, outPoly)
        gp.delete(inPoly)
    except:
        gp.adderror(gp.getmessages())
    #write metadata
    metaFile = os.path.basename(inRaster).split(".")[0] + "_meta.txt"
    metaFolder = os.path.dirname(inRaster)
    #break list to int
    bList = []
    for b in breakList:
        bList.append(int(b))
    
    if gp.exists(os.path.join(metaFolder, metaFile)):
        meta = barc_module.Metadata(metaFolder, metaFile)
        bList.sort()
        tStart = time.localtime()
        meta.modifiedDate = str(tStart.tm_hour) + ':' + str(tStart.tm_min) + ' ' + \
        str(tStart.tm_mday) + '-' + str(tStart.tm_mon) + '-' + str(tStart.tm_year)
        meta.modifiedAuthor = os.environ.get("USERNAME")
        meta.BARClow = str(bList[0])
        meta.BARCmod = str(bList[1])
        meta.BARChigh = str(bList[2])
        meta.BARCfile = os.path.join(gp.workspace, outRaster)
        meta.BARCcalibration = str(calibration)
        
        meta.BARClastUpdated = str(tStart.tm_hour) + ':' + str(tStart.tm_min) + ' ' + \
        str(tStart.tm_mday) + '-' + str(tStart.tm_mon) + '-' + str(tStart.tm_year)
        meta.write()
    else:
        print "No existing metadata"
    print "done"

main(gp.workspace, inRaster, outPoly, breakValues)