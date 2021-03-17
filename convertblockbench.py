import json
import os

import numpy as np
from PIL import Image

# user adjustable variables
# file
filepath = "D:\SourceCode\Python\Mine imator\Blendbench\converted\OuterTaleGasterBlaster_convert.mimodel"
newFilepath = "D:\SourceCode\Python\Mine imator\Blendbench\converted"

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
file = os.path.split(filepath)

def recalc(value):
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
        if filetype[0] in file[1]:
            textureIndex = 0 
            try: # Exception No "textures" found
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
            
            groups = data["groups"]
            elements = data["elements"] # xtract "elements"
            return elements, texture, texture_size,groups
        else:
            texture = data["texture"]
            texture_size = data["texture_size"]
            parts = data["parts"] # Through "parts" extract "shapes"
            return parts,texture,texture_size
    except FileNotFoundError:
        print('File not found.')

def axisPart(axis,angle): #axis Rotation
    if axis == "x":
        rotation = [angle,0,0]
    elif axis == "y":
        rotation = [0,angle,0]
    else:
        rotation = [0,0,angle]
    return rotation
    
def convertModel(filepath,offset):
    parts, texture, texture_size,  = load(filepath)
    model = file[1].replace(filetype[0],'')
    elementList =[]

    bbmodel_json = {
        "name": model + " converted by Blendbench - zNight Animatics",
        "texture_size": texture_size,
        "textures": texture, 
        "elements": [],
    }
    
    def UVFaceLayout(face,elementFrom,elementTo,elementUV):
        x = elementFrom
        y = elementTo
        xPos = elementUV[0]
        yPos = elementUV[1] 
        if face == 'north':
            return x+y
        elif face == "east":
            return x+y
        elif face == "south":
            return x+y
        elif face == "west": 
            return x+y  
        elif face == "up":
            return x+y
        else:
            return x+y
        
    parentParts = parts[0]
    parts = parentParts["parts"]
    for i,part in enumerate(parts):
        elementName = part["name"]
        elementOrigin = part["position"]
        try:
            elementRotate = part["rotate"]
        except KeyError:
            elementRotate = [ 0, 0, 0 ]
        shapes = part["shapes"]
        for e,shape in enumerate(shapes):
            elementFrom = shape["from"]
            elementTo = shape["to"]
            elementUV = shape["uv"]
            elementPosition = shape["position"]

        northUV = UVFaceLayout("north",elementFrom,elementTo,elementUV)
        eastUV = UVFaceLayout("east",elementFrom,elementTo,elementUV)
        southUV = UVFaceLayout("south",elementFrom,elementTo,elementUV)
        westUV = UVFaceLayout("west",elementFrom,elementTo,elementUV)
        upUV = UVFaceLayout("up",elementFrom,elementTo,elementUV)
        downUV = UVFaceLayout("down",elementFrom,elementTo,elementUV)

        faces = {
            "north": {"uv" : northUV, "texture": "#0"}
        }   
        

        elementList.append({
            "name": elementName,
            "from": elementFrom,
            "to" : elementTo,
            "rotation": elementRotate,
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


def exportBB(filepath,newFilepath,offset):
    path = os.path.split(filepath)[0]+"\\"
    file = os.path.split(filepath)[1].replace(filetype[0],'')
    bbmodel_json = convertModel(filepath,offset)
    if path == newFilepath:
        file = file+"_converted"+filetype[0]
    else:
        file = file+filetype[0]
    newFilepath = newFilepath+"\\"+file
    with open(newFilepath, "w") as f:
        json.dump(bbmodel_json, f)

def convert(filepath,newFilepath,offset):
    exportBB(filepath,newFilepath,offset)

def convertDebug(filepath,offset,debug):
    mimodel_json = convertModel(filepath,offset)
    if debug:
        print(mimodel_json)

if __name__ == "__main__":
    # clear screen
    os.system('cls')
    convert(filepath,newFilepath,offset)
