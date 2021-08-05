import json
import math
import os

import numpy as np
from PIL import Image

#setting
offset = False
a = 1.05
round = 0
multiplier = 3.75
UVmultiplier = 20
## default 
defaultTexture = "Default texture" # default Inherit texture. Relative file path?
defaultTextureSize = [16,16] # default based on Inherit texture # What does the "texture_size" even do? I don't even know
debug = False
#file variables
filetype = [".json",".mimodel"]


def recalculate(value):
    newValue = np.round(np.multiply(value,multiplier),round)
    return newValue

def worldGrid(offset): # offset worldGrid by (8,0,8) because it doesn't make sense for Blockbench for the world origin at the corner of the grid
    pivotOffset = [0,0,0]
    if offset == True:
        pivotOffset = [8,0,8] 
    else:
        pass
    return pivotOffset

def load(filepath): # Load mimodel and Minecraft json
    try:
        with open(filepath, "r") as fileObject:
            data = json.load(fileObject)
            texture = data["texture"]
            texture_size = data["texture_size"]
            parts = data["parts"] # Through "parts" extract "shapes"
            return parts,texture,texture_size
    except FileNotFoundError:
        print('File not found.')

def round_rotation(angle, eps = 1e-4):
    if angle > 0:
        if abs(angle - math.pi/4) < eps:
            return math.pi/4
        if abs(angle - math.pi/8) < eps:
            return math.pi/8
        if abs(angle) < eps:
            return 0.0
    if angle < 0:
        if abs(angle + math.pi/4) < eps:
            return -math.pi/4
        if abs(angle + math.pi/8) < eps:
            return -math.pi/8
        if abs(angle) < eps:
            return 0.0
    
    return angle

def axisElement(elementRotate): #axis Rotation restricted
    angleRotate = elementRotate[0]
    axisRotate = 0
    for axis,angle in enumerate(elementRotate):
        if angle > angleRotate:
            angle == angleRotate
            axisRotate = axis

    if axisRotate == "1":
        elementAxis = "y"
        elementAngle = elementRotate[1]
    elif axisRotate == "2":
        elementAxis = "z"
        elementAngle = elementRotate[2]
    else:
        elementAxis = "x"
        elementAngle = elementRotate[0]

    elementAngle = round_rotation(elementAngle)
    return elementAngle,elementAxis 
    
def convert(filepath,offset=False):
    parts, texture, texture_size  = load(filepath)
    model = os.path.split(filepath)[1].replace(filetype[0],'')
    elementList = []

    pivotOffset = worldGrid(offset)
    bbmodel_json = {
        "name": model + " converted by Blendbench - zNight Animatics",
        "texture_size": texture_size,
        "textures": texture, 
        "elements": [],
    }
    
    # def UVFaceLayout(face,elementFrom,elementTo,elementUV):
    #     x = elementFrom
    #     y = elementTo
    #     xPos = elementUV[0]
    #     yPos = elementUV[1] 
    #     if face == 'north':
    #         return x+y
    #     elif face == "east":
    #         return x+y
    #     elif face == "south":
    #         return x+y
    #     elif face == "west": 
    #         return x+y  
    #     elif face == "up":
    #         return x+y
    #     else:
    #         return x+y
    
    parentParts = parts[0]
    parts = parentParts["parts"]
    for i,part in enumerate(parts):
        elementName = part["name"]
        elementOrigin = part["position"]
        try:
            elementRotate = part["rotation"]
        except KeyError:
            elementRotate = [ 0, 0, 0 ]
        shapes = part["shapes"]
        for e,shape in enumerate(shapes):
            elementFrom = shape["from"]
            elementTo = shape["to"]
            elementUV = shape["uv"]
        print(elementRotate)
        elementOrigin = np.subtract(np.multiply(elementOrigin,-1),pivotOffset).tolist()
        elementAngle, elementAxis = axisElement(elementRotate)

        elementRotation = {"angle": elementAngle ,"axis": elementAxis, "origin": elementOrigin}

        x = elementUV[0] 
        y = elementUV[1]
        x_size = elementTo[0]
        y_size = elementTo[1]
        z_size = elementTo[2]

        faces = {
            "up": {"uv":[ x, y, x_size, z_size ], "texture": "#0"},
            "down": {"uv":[ x + z_size + x_size , y, x_size , z_size ], "texture": "#0"},
            "east": {"uv": [ x, y + z_size, z_size, y_size], "texture": "#0"},
            "north": {"uv": [ x + z_size , y + z_size, z_size, y_size], "texture": "#0"},
            "west": {"uv": [ x + z_size + x_size , y + z_size, z_size, y_size], "texture": "#0"},
            "south": {"uv": [ x + z_size + x_size , y + z_size, x_size, y_size], "texture": "#0"}
        }   

        elementList.append({
            "name": elementName,
            "from": elementFrom,
            "to" : elementTo,
            "rotation": elementRotation,
            "faces": faces
        })
        
    #     elementRotate = elementData["rotation"]
    #     elementAngle = elementRotate["angle"]
    #     elementAxis = elementRotate["axis"]
    #     elementOrigin = recalc(elementRotate["origin"])

    #     elementOrigin = elementOrigin.tolist()

    #     elementFace = elementData["faces"]

    #     elementRotate = {}
    #     elementRotate["angle"] = elementAngle
    #     elementRotate["axis"] = elementAxis
    #     elementRotate["origin"] = elementOrigin

    # elementFrom = elementFrom.tolist()
    # elementTo = elementTo.tolist()
    
    
        

				# {face: 'north', fIndex: 10,	from: [size[2], size[2]],			 	size: [size[0],  size[1]]},
				# {face: 'east', fIndex: 0,	from: [0, size[2]],				   		size: [size[2],  size[1]]},
				# {face: 'south', fIndex: 8,	from: [size[2]*2 + size[0], size[2]], 	size: [size[0],  size[1]]},
				# {face: 'west', fIndex: 2,	from: [size[2] + size[0], size[2]],   	size: [size[2],  size[1]]},
				# {face: 'up', fIndex: 4,		from: [size[2]+size[0], size[2]],	 	size: [-size[0], -size[2]]},
				# {face: 'down', fIndex: 6,	from: [size[2]+size[0]*2, 0],		 	size: [-size[0], size[2]]}
    
    
    

    bbmodel_json["elements"] = elementList
    print(bbmodel_json)

    return bbmodel_json

def export(filepath,newFilepath,offset):
    path = os.path.split(filepath)[0]+"\\"
    file = os.path.split(filepath)[1].replace(filetype[1],'')
    bbmodel_json = convert(filepath,offset)
    if path == newFilepath:
        file = file+"_converted"+filetype[0]
    else:
        file = file+filetype[0]
    newFilepath = newFilepath+"\\"+file
    with open(newFilepath, "w") as f:
        json.dump(bbmodel_json, f)

def convertDebug(filepath,offset,debug):
    mimodel_json = convert(filepath,offset)
    if debug:
        print(mimodel_json)


