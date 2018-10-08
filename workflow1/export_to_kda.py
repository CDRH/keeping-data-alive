'''
Created on Sep 25, 2018

@author: Jessica Dussault

Exports scene and individual models created from shapefile + rule application
along with attributes, RPK, and log, for use with Keeping Data Alive grant

Center for Digital Research in the Humanities
University of Nebraska-Lincoln
'''

import datetime
import json
import os
from scripting import *

# Get a CityEngine instance
ce = CE()

###########
# HELPERS #
###########

# create directory if it does not exist
def createDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# defines settings for the selection of shapes and exports DAE
# this uses "scene" in the KDA sense, NOT in the CityEngine sense
def exportScene(toExport, directory, name):
    exportSceneMetadata(toExport, directory, name)
    exportDae(toExport, directory, name)

# defines settings for each object and exports as DAE
def exportShape(toExport, directory, name):
    exportShapeMetadata(toExport, directory, name)
    exportDae(toExport, directory, name)

def exportSceneMetadata(toExport, directory, name):
    # Note: cannot select attributes for selections, expects single object

    data = {
        "coordinates" : {
            "selection_centered" : selectionCoords,
            "prj_system" : coordinateSystem[0],
            "prj_label" : coordinateSystem[1]
        },
        "info" : generalInfo
    }
    filename = directory+"/"+name+".json"
    writeJson(filename, data)

# create JSON sidecar file with shape attribute information
def exportShapeMetadata(toExport, directory, name):
    attrs = ce.getAttributeList(toExport)

    # assemble rules specific to this shape
    ruleFile = ce.getRuleFile(toExport)
    startRule = ce.getStartRule(toExport)

    try:
        if len(ruleFile) > 0:
            # export RPK file if there are associated rules
            rpkSettings = RPKExportSettings()
            rpkSettings.setRuleFile(ce.getRuleFile(toExport))
            rpkSettings.setFile(ce.toFSPath(directory+"/"+name+".rpk"))
            rpkSettings.addFilesAutomatically()
            ce.exportRPK(rpkSettings)
    except Exception:
        print "Something went wrong, try manually sharing your rule files as a RPK to see warnings and errors"

    data = {
        "attributes" : {},
        "coordinates" : {
            "shape_centered" : ce.getPosition(toExport),
            "selection_centered" : selectionCoords,
            "prj_system" : coordinateSystem[0],
            "prj_label" : coordinateSystem[1]
        },
        "info" : generalInfo,
         "rules" : {
             "file" : ruleFile,
             "start" : startRule,
         }
    }

    for attr in attrs:
        data["attributes"][attr] = ce.getAttribute(toExport, attr)

    # City Engine is using a very old version of python and this
    # is the only method of writing to a file that I was able to get to work
    filename = directory+"/"+name+".json"
    writeJson(filename, data)
    
# export shape(s) to DAE file
def exportDae(toExport, directory, name):
    settings = DAEExportModelSettings()

    ####################
    # GENERAL SETTINGS #
    ####################
    # set the export path and name of associated files
    settings.setOutputPath(directory)
    settings.setBaseName(name)
    # export the models but default to start shape if problem
    settings.setExportGeometry("MODEL_GEOMETRY_FALLBACK")
    # export associated terrain
    settings.setTerrainLayers("TERRAIN_ALL_SELECTED")
    # simplification of terrain
    settings.setSimplifyTerrainMeshes(True)

    ########################
    # GRANULARITY SETTINGS #
    ########################
    # export to a single file (instead of one per material)
    settings.setFileGranularity("MEMORY_BUDGET")
    # memory budget set to default from export wizard
    settings.setMemoryBudget(500)
    # create a node with shape's name
    settings.setCreateShapeGroups(True)
    # "Reuse asset instances, merge generated meshes by material"
    settings.setMeshGranularity("INSTANCED")

    #####################
    # GEOMETRY SETTINGS #
    #####################
    # allow vertices to be shared between faces
    settings.setVertexIndexing("INDEXED")
    # vertex normals set to "Write vertex normals"
    settings.setVertexNormals("PASS")
    # write all texture coordinates
    settings.setTextureCoordinates("ALL")
    # ignoring local offset
    # "zero" the object(s) to remove geographic coordinates for global offset
    position = ce.getPosition(toExport)
    settings.setGlobalOffset([-position[0], -position[1], -position[2]])
    # vertex precision set to default from export wizard
    settings.setVertexPrecision(0.001)
    # normal precision set to default from export wizard
    settings.setNormalPrecision(0.001)
    # texture coord precision set to default from export wizard
    # settings.setTexcoordPrecision(1.0E-4)
    # shares vertices within precision
    settings.setMergeVertices(True)
    # shares normals within precision
    settings.setMergeNormals(True)
    # shares texture coordinates within precision
    settings.setMergeTexcoords(True)
    # does not triangulate meshes, required for google earth
    settings.setTriangulateMeshes(False)
    # allow holes
    settings.setFacesWithHoles("PASS")

    #####################
    # MATERiAL SETTINGS #
    #####################
    # include material information
    settings.setIncludeMaterials(True)

    ####################
    # TEXTURE SETTINGS #
    ####################
    # include textures
    settings.setCollectTextures(True)
    # do not create texture atlases that combine texture atlases
    settings.setCreateTextureAtlases(False)
    # therefore do not need texture atlas max dimension
    # therefore do not need texture atlas border dimensions

    #####################
    # ADVANCED SETTINGS #
    #####################
    # output log
    settings.setWriteLog(True)
    # beware, collada 1.5.x doesn't seem to work when exporting these
    settings.setCOLLADAVersion(colladaVersion)
    # delineater for shape name clashes
    settings.setShapeNameDelimiter("_")
    # overwrite any existing files at that location!!!
    settings.setExistingFiles("OVERWRITE")
    # no reports
    ce.export(toExport, settings)
    
def writeJson(filepath, data):
    f = open(filepath, "w")
    print >> f, json.dumps(data, indent=4, sort_keys=True)
    f.close()

################
# EXPORT HOOKS #
################

# Called for each shape after generation.
def finishModel(exportContextOID, shapeOID, modelOID):
    ctx = ScriptExportModelSettings(exportContextOID)
    shape = Shape(shapeOID)
    # export shape with unique id to subdirectory
    # NOTE: this is not the same name that is in the DAE scene's XML
    name = ce.getName(shape).replace(" ", "_")
    oid = ce.getOID(shape)
    
    shapeName = layerName + "_" + name + "_" + str(oid)
    shapeDir = baseDir + "/" + name + "_" + str(oid)
    createDirectory(shapeDir)
    print "--- " + shapeName
    exportShape(shape, shapeDir, shapeName)
    
# Called after all shapes are generated.
def finishExport(exportContextOID):
    ctx = ScriptExportModelSettings(exportContextOID)
    # export scene containing all selected shapes
    sceneName = layerName + "_scene"
    print "=== " + sceneName
    exportScene(selection, baseDir, sceneName)
    print "Finished export of all scenes and shapes"

###############
# SCRIPT BODY #
###############

print "Beginning export to KDA based on viewport selection"

# get current selection and exit if no objects selected
selection = ce.selection()

if selection == None or len(selection) == 0:
    print("No shapes found in selection! Cancelling export")
    quit()

# get the centered position of the selected items
selectionCoords = ce.getPosition(selection)

colladaVersion = "COLLADA_1_4_1"
coordinateSystem = ce.getSceneCoordSystem()
if coordinateSystem == None:
    coordinateSystem = ["None", "None"]

# general info like software version, username, etc
generalInfo = {
            "collada_version" : colladaVersion,
            "creator" : os.getlogin(),
            "date" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "software" : ce.getVersionString(),
        }

# choose the first selected object's layer name as directory name
# which will be saved to models/ path
layerName = ce.getName(ce.getLayer(selection[0])).replace(" ", "_")
baseDir = ce.toFSPath("models/" + layerName)
createDirectory(baseDir)
print("Exporting scene and shapes to models/" + layerName)
