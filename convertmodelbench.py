import json
import os

import numpy as np
from PIL import Image

# user adjustable variables
# file
filepath = "D:\SourceCode\Python\Mine imator\storage\OuterTaleSans\OuterTaleSans\OuterTaleGasterBlaster_convert.json"
newFilepath = "D:\SourceCode\Python\Mine imator\Blendbench\converted"

# setting
offset = True
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

def worldGrid(offset): # offset worldGrid by (8,0,8) because it doesn't make sense for Blockbench for the world origin at the corner of the grid
    pivotOffset = [0,0,0]
    if offset == True:
        pivotOffset = np.multiply([8,0,8],multiplier)
    else:
        pass
    return pivotOffset

def UVLayout(value,*args):
    value = np.round(value*UVmultiplier*args[0],decimals=0).tolist()*a
    return value

def axisPart(axis,angle): #axis Rotation
    if axis == "x":
        rotation = [angle,0,0]
    elif axis == "y":
        rotation = [0,angle,0]
    else:
        rotation = [0,0,angle]
    return rotation

def convertBlock(filepath,offset): 
    elements, texture, texture_size = load(filepath)
    model = file[1].replace(filetype[0],'')
    pivotOffset = worldGrid(offset)
    if texture == "Default texture":
        texture = "Default texture.png"
    else:
        texture = texture.split('/')[1]+".png"

    imageTex = np.array(Image.open(file[0]+ "\\" + texture))
    imageSize = imageTex.shape # Image Size
    imageX = imageSize[0]
    imageY = imageSize[1]
    
    mimodel_json = {
        "name": model + " converted by Blendbench - zNight Animatics",
        "texture": texture,
        "texture_size": texture_size

    }
    num_cube = 0 # numbers of cube parts
    num_parts = 0 # numbers of parts
    total_parts = 0 # total
    
    parts = []
    for i,element in enumerate(elements): # Extract "elements" list
        part = element
        try: # Exception No "name" found. 
            partName = part["name"]
            if num_parts == 0: 
                partName = partName
            else:
                partName = partName + " " + str(num_parts)
            num_parts+=1
            total_parts+=1
        except KeyError:
            if num_cube == 0:
                partName = "cube"
            else:
                partName = "cube" + " " + str(num_cube)
            num_cube+=1
            total_parts+=1
        else:
            pass
        
        shape = element
        shapeFrom = np.array(shape["from"])
        shapeTo = np.array(shape["to"]) 

        origin = np.array(shape["rotation"]["origin"])
        origin = origin.tolist() # part position base on element origin
        position = np.multiply(origin,-1) # shape position flip base on origin
        
        angle = shape["rotation"]["angle"]
        axis = shape["rotation"]["axis"]
        rotation = axisPart(axis,angle)
        
        face = shape["faces"]
        faceU = face["up"]["uv"][0]
        faceE = face["east"]["uv"][1]
        
        h = 0
        w = 0
        h = imageY*0.0035
        w = imageX*0.0035

        texturePos=[UVLayout(faceU,h)-10,UVLayout(faceE,w)*1.05-8]

        if texture_size[0] == 32:
            textureScale = 2
        elif texture_size[0] == 64:
            textureScale = 3
        elif texture_size[0] == 128:
            textureScale = 4
        else:
            textureScale = 1 # textureScale = 1 #default

        uv = texturePos
        #convert np list
        shapeFrom = shapeFrom.tolist()
        shapeTo = shapeTo.tolist()
        position = position.tolist()

        shape = []
        shape.append({ 
            "type": "block",
            "description": partName + " shape",
            "texture": texture,
            "texture_size": texture_size,
            "texture_scale": textureScale, 
            # "color_blend": "#000000",
			# "color_mix": "#FFFFFF",
			# "color_mix_percent": 1,
			# "color_brightness": 0,
            "from": shapeFrom,
            "to": shapeTo,
            "uv": uv, # TODO: new UV map based on calculation
            "position": position, 
            "rotation" : [0 , 0 , 0 ],
            "scale" : [ 1, 1, 1 ]
        })
        parts.append({
            "name": partName,
            # "color_blend": "#000000",
			# "color_mix": "#FFFFFF",
			# "color_mix_percent": 1,
			# "color_brightness": 0,
            "position": np.subtract(origin,pivotOffset).tolist(),     
            "rotation": rotation, 
            "scale": [ 1, 1, 1 ],
            "shapes": shape
        })
    parentPart = []
    parentPart.append({
        "name": model,
        # "color_blend": "#000000",
        # "color_mix": "#FFFFFF",
        # "color_mix_percent": 1,
        # "color_brightness": 0,
        "position": [ 0, 0, 0 ],     
        "rotation": [ 0, 0, 0 ], 
        "scale": [ 1, 1, 1 ],
        "parts": parts
    })

    mimodel_json["parts"] = parentPart
    return mimodel_json

def exportMI(filepath,newFilepath,offset):
    path = os.path.split(filepath)[0]+"\\"
    file = os.path.split(filepath)[1].replace(filetype[0],'')
    mimodel_json = convertBlock(filepath,offset)
    if path == newFilepath:
        file = file+"_converted"+filetype[1]
    else:
        file = file+filetype[1]
    newFilepath = newFilepath+"\\"+file
    with open(newFilepath, "w") as f:
        json.dump(mimodel_json, f)
    
def convertDebug(filepath,offset,debug):
    mimodel_json = convertBlock(filepath,offset)
    if debug:
        print(mimodel_json)

def convert(filepath,newFilepath,offset,debug):
    exportMI(filepath,newFilepath,offset)
    convertDebug(filepath,offset,debug)
    
if __name__ == "__main__":
    # clear screen
    os.system('cls')
    convert(filepath,newFilepath,offset,debug)
