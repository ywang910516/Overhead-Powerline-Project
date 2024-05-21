import arcpy
import numpy


#Steps
#1. Project kids vulnerability polygons to NAD1983 NJ feet (done using ArcPro GUI batch project tool)
#2. Select all kid vulnerability polygons with gridcode=0 (function: removeFragmentsDissolve)
#3. Dissolve vulnerability layers to one single polygon (function: removeFragmentsDissolve)
    #These files are now named kids_mmdd_hh and they are the areas that cannot be traveled by walking. They
    #will be used as barriers in makeWalkRoutes
#4. Select from the banned boat area only the area that intersects the vulnerability area. This will now create layers
    #that are inaccessible by any means of transportation to be used as barriers in makeAllRoutes
#5. Run makeAllRoutes for each hour using the fire stations and evacuation point as facilities and the houses as incidents
#6. Run makeWalkRoutes for each hour using the evacuation point as a facility and the houses as incidents



arcpy.env.workspace = r"yourworkspacehere"

# Add the geoprocessing service as a toolbox.
# Check https://pro.arcgis.com/en/pro-app/arcpy/functions/importtoolbox.htm for
# other ways in which you can specify credentials to connect to a geoprocessing service.
arcpy.CheckOutExtension("network")
coordsys = arcpy.SpatialReference('NAD 1983 StatePlane New Jersey FIPS 2900 (US Feet)')


#Make projected vulnerability areas into feature layers. Select polygon features with gridcode=0. Dissolve inner lines
#Only do this once to prepare the vulnerability areas.
def removeFragmentsDissolve():
    hc = 1
    for x in range(26):
        if x < 23:
            in1 = "Human_vul_02SEP2021_"
            out2 = "_0902_"
        else:
            in1 = "Human_vul_03SEP2021_"
            out2 = "_0903_"
        if hc < 10:
            in2 = "0"+str(hc)+"_00_00_"
            out3 = "0"+str(hc)
        else:
            in2 = str(hc)+"_00_00_"
            out3 = str(hc)
        in3 = "kids_poly"
        out1 = "xkids"
        hc = hc + 1
        if hc == 24:
            hc = 0
        infile = in1+in2+in3
        outlayer = out1+out2+out3

        arcpy.MakeFeatureLayer_management(infile, outlayer)

        #Select polygon features with area > 3000 to exclude the small fragments
        arcpy.management.SelectLayerByAttribute(outlayer, 'NEW_SELECTION', '"gridcode" = 0')

        # Dissolve boundaries for selected polygon features vulnerability layer
        dissolved = outlayer[1:]
        arcpy.management.Dissolve(outlayer, dissolved)


#Function to get vulnerability file name
def getVulnArea(date, hour):
    str1 = "kids_"
    if date == 2:
        str2 = "0902_"
    else:
        str2 = "0903_"
    if hour < 10:
        str3 = "0"+str(hour)
    else:
        str3 = str(hour)
    return str1 + str2 + str3


#Function to get banned boat area file name
def getBannedBoat(date, hour):
    if date == 2:
        str1 = "I:\Manville-Powerline\high-veg\output\ASC\Banned_zone_for_boat"+r"\b"+"anned_zone_for_boat_sitting_height_considered_polygon\polygon_mask_WSE_urban_02SEP2021 "
    else:
        str1 = "I:\Manville-Powerline\high-veg\output\ASC\Banned_zone_for_boat"+r"\b"+"anned_zone_for_boat_sitting_height_considered_polygon\polygon_mask_WSE_urban_03SEP2021 "
    if hour < 10:
        str2 = "0"+str(hour)
    else:
        str2 = str(hour)
    return str1+str2+" 00 00"



#Erase banned boat area from vulnerability area to use as barrier for makeAllRoutes
#Use savecode=1 to make the layer. Use savecode=0 to just get the layer name.
def getBoatVulnIntersect(date, hour,savecode):
    vuln = getVulnArea(date, hour)
    #bannedBoat = getBannedBoat(date, hour)
    if hour < 10:
        boatVulnInter = "bb_090" + str(date) + "_0" + str(hour)
    else:
        boatVulnInter = "bb_090" + str(date) + "_" + str(hour)
    if savecode == 1:
        print(1)
        #arcpy.analysis.Clip(bannedBoat, vuln, boatVulnInter)
    else:
        return boatVulnInter


#Use closest facility layer to get evacuation routes
def makeAllRoutes(date, hour):
    age = "kids"
    outlayerstr = "cf_" + age + "_090" + str(date) + "_hr" + str(hour)
    output_layer_file = outlayerstr+".lyrx"
    print(outlayerstr)

    #Make closest facility layer
    result_object = arcpy.na.MakeClosestFacilityAnalysisLayer("https://www.arcgis.com/", outlayerstr, "Walking Distance", "FROM_FACILITIES", "", 1, line_shape="ALONG_NETWORK")
    layer_object = result_object.getOutput(0)

    #Get the names of all the sublayers within the closest facility layer.
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    #Stores the layer names that we will use later
    facilities_layer_name = sublayer_names["Facilities"]
    incidents_layer_name = sublayer_names["Incidents"]
    barrier_layer_name = sublayer_names["PolygonBarriers"]

    #Add facilities, incidents, barriers
    incname = "ManvilleBldg1ftPlus"
    barrname = getBoatVulnIntersect(date, hour, 0)
    arcpy.na.AddLocations(layer_object, facilities_layer_name, "rescueBoatLocs", append="CLEAR")
    arcpy.na.AddLocations(layer_object, incidents_layer_name, incname, search_tolerance=60, append="CLEAR")
    arcpy.na.AddLocations(layer_object, barrier_layer_name, barrname, append="CLEAR")
    print(incname)
    print(barrname)

    #solve
    arcpy.na.Solve(layer_object, "SKIP")


#Use closest facility layer to get evacuation routes for walking only using human vulnerability (kids) shapefiles
def makeWalkRoutes(date, hour):
    tmode = "walk"
    outlayerstr = "cf_" + tmode + "_090" + str(date) + "_hr" + str(hour)
    output_layer_file = outlayerstr+".lyrx"
    print(outlayerstr)

    #Make closest facility layer
    result_object = arcpy.na.MakeClosestFacilityAnalysisLayer("https://www.arcgis.com/", outlayerstr, "Walking Distance", "FROM_FACILITIES", "", 1, line_shape="ALONG_NETWORK")
    layer_object = result_object.getOutput(0)

    #Get the names of all the sublayers within the closest facility layer.
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    #Stores the layer names that we will use later
    facilities_layer_name = sublayer_names["Facilities"]
    incidents_layer_name = sublayer_names["Incidents"]
    barrier_layer_name = sublayer_names["PolygonBarriers"]

    #Add facilities, incidents, barriers
    incname = "ManvilleBldg1ftPlus"
    barrname = getVulnArea(date, hour)
    arcpy.na.AddLocations(layer_object, facilities_layer_name, "evacPoint", append="CLEAR")
    arcpy.na.AddLocations(layer_object, incidents_layer_name, incname, search_tolerance=60, append="CLEAR")
    arcpy.na.AddLocations(layer_object, barrier_layer_name, barrname, append="CLEAR")
    print(incname)
    print(barrname)

    #solve
    arcpy.na.Solve(layer_object, "SKIP")




#Steps 2 and 3
#removeFragmentsDissolve()

#Step 4
'''s2 = 1
s3 = 0
for x in range(26):
    if x < 23:
        getBoatVulnIntersect(2, s2, 1)
        s2 = s2 + 1
    else:
        getBoatVulnIntersect(3, s3, 1)
        s3 = s3 + 1'''



#Step 5
#Running it one at a time. Date can be 2 or 3. Hour can be 1-23 with date=2 and 0-2 with date=3
#makeAllRoutes(2, 5)

#Step 6
#Redoing the walking routes using the kids human vulnerability as barriers and finding walking routes from all homes to
#the evacuation point only.
#makeWalkRoutes(3, 2)