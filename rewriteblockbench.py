import json
import os

import numpy as np

#user adjustable variables
#file
filepath = "D:\SourceCode\Python\Mine imator\Blendbench\converted\OuterTaleGasterBlaster_convert.mimodel"
newFilepath = "D:\SourceCode\Python\Mine imator\Blendbench\converted"

#setting
offset = False
a = 1.05
round = 0
multiplier = 3.75
UVmultiplier = 20
# file variables
filetype = [".json",".mimodel"]
file = os.path.split(filepath)
#default
defaultTexture = "Default texture" # default Inherit texture. Relative file path?
defaultTextureSize = [16,16] # default based on Inherit texture # What does the "texture_size" even do? I don't even know
debug = False

def recalc(value):
    newValue = np.round(np.multiply(value,multiplier),round)
    return newValue

def worldGrid(offset): # offset worldGrid by (8,0,8) because it doesn't make sense for Blockbench for the world origin at the corner of the grid
    pivotOffset = [0,0,0]
    if offset == True:
        pivotOffset = np.multiply([8,0,8],multiplier)
    else:
        pass
    return pivotOffset

def load(filepath): # Load mimodel and Minecraft json
    try:
        with open(filepath, "r") as fileObject:
            data = json.load(fileObject)
            textureIndex = 0
            try: # Exception No "textures" found
                try:
                    texture = data["textures"][str(textureIndex)]
                except IndexError:
                    textureIndex+=1
                    texture = data["textures"][str(textureIndex)]
            except KeyError:
                texture = defaultTexture
            try: # Exception No "textures_size" found
                texture_size=data["texture_size"]
            except KeyError:
                texture_size= defaultTextureSize

            elements = data["elements"] # Extract "elements"
            return elements, texture, texture_size
    except FileNotFoundError:
        print('File not found. Please recheck your file or directory make sure it\'s in the right path.')

def blockbench(filepath,offset):
    elements, texture, texture_size, groups = load(filepath)
    model = file[1].replace(filetype[0],'')
    pivotOffset = worldGrid(offset)
    elementList =[]
    bbmodel_json = {
        "name": model + " converted by Blendbench - zNight Animatics",
        "texture_size": texture_size,
        "textures": {"0":texture}, 
        "elements": [],
        # "groups" : groups
    }
    
    for i,element in enumerate(elements):
        elementData = element
        elementName = elementData["name"]

        elementFrom = recalc(elementData["from"] - pivotOffset)
        elementTo = recalc(elementData["to"] - pivotOffset)
        
        elementRotate = elementData["rotation"]
        elementAngle = elementRotate["angle"]
        elementAxis = elementRotate["axis"]
        elementOrigin = recalc(elementRotate["origin"] - pivotOffset)
        
        elementOrigin = elementOrigin.tolist()
        
        elementFace = elementData["faces"]
        
        elementRotate = {}
        elementRotate["angle"] = elementAngle
        elementRotate["axis"] = elementAxis
        elementRotate["origin"] = elementOrigin

        elementFrom = elementFrom.tolist()
        elementTo = elementTo.tolist()
        

        elementList.append({
            "name": elementName,
            "from": elementFrom,
            "to" : elementTo,
            "rotation": elementRotate,
            "faces": elementFace
        })
        

    bbmodel_json["elements"] = elementList

    return bbmodel_json
