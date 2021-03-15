import json
import os

import numpy as np
from PIL import Image

# config settings
filetype = [".json",".mimodel"]
fileload = "OuterTaleGasterBlaster_convert.mimodel" 
filepath = ".\\storage\\OuterTaleSans\\OuterTaleSans\\"
file = filepath + fileload 
filename = fileload + "convert_2"


# texture="texture"
## Default 
defaultTexture = "Default texture" # default Inherit texture. Relative file path?
defaultTextureSize = [16,16] # default based on Inherit texture # What does the "texture_size" even do? I don't even know
offset = False

a = 1.05
round = 0
multiplier = 3.75
UVmultiplier = 20
def recalc(value):
    newValue = np.round(np.multiply(value,multiplier),round)
    return newValue

# clear screen
os.system('cls')

def worldGrid(offset): # offset worldGrid by (8,0,8) because it doesn't make sense for Blockbench for the world origin at the corner of the grid
    pivotOffset = [0,0,0]
    if offset == True:
        pivotOffset = [8,0,8] 
    else:
        pass
    return pivotOffset
pivotOffset = worldGrid(offset)

def load(file): # Load mimodel and Minecraft json
    with open(file, "r") as fileObject:
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
        try:
            groups = data["groups"]
        except KeyError:
            groups = []
        try: # Exception  No "elements" found
            elements = data["elements"] # Extract "elements"

            return elements, texture, texture_size ,groups
        except KeyError:
            texture = data["texture"]
            texture_size = data["texture_size"]
            parts = data["parts"] # Through "parts" extract "shapes"

            return parts,texture,texture_size

def print_json(): # For Preview before and after
    data=load(file)
    print(data)
    print("\n")

def axisPart(axis,angle): #axis Rotation
    if axis == "x":
        rotation = [angle,0,0]
    elif axis == "y":
        rotation = [0,angle,0]
    else:
        rotation = [0,0,angle]
    return rotation

def convertBlock(filename): 
    elements, texture, texture_size, groups = load(file)
    if texture == "Default texture":
        texture = "Default texture.png"
    else:
        texture = texture.split('/')[1]+".png"
    # imageTex = np.array(Image.open(filepath + texture))

    # ImageSize = imageTex.shape # Image Size
    # print(str(ImageSize[0]) + " x " + str(ImageSize[1]))
    mimodel_json = {
        "credit": "Using zNight Animatics's Blendbench conversion made by Trung Phạm",
        "name": filename,
        "texture": texture,
        "texture_size": texture_size
    }
    num_cube = 0 # numbers of cube parts
    num_parts = 0 # numbers of parts
    total_parts = 0 # total
    parts = []
    for element in elements: # Extract "elements" list
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
        shapeFrom = np.array(shape["from"]) - pivotOffset 
        shapeTo = np.array(shape["to"]) - pivotOffset

        origin = np.array(shape["rotation"]["origin"])
        origin = origin.tolist() # part position base on element origin
        position = np.multiply(origin,-1) # shape position flip base on origin
        
        angle = shape["rotation"]["angle"]
        axis = shape["rotation"]["axis"]
        rotation = axisPart(axis,angle)
        
        face = shape["faces"]
        faceU = face["up"]["uv"][0]
        faceE = face["east"]["uv"][1]

        texturePos=[np.round(faceU*UVmultiplier,decimals=0).tolist()*a,np.round(faceE*UVmultiplier,decimals=0).tolist()*a]

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
            "position": origin ,     
            "rotation": rotation, 
            "scale": [ 1, 1, 1 ],
            "shapes": shape
        })
    mimodel_json["parts"] = parts
    return mimodel_json

def convertModel(filename): #rewrite json or convert mimodel
    def blockbench():
        elements, texture, texture_size, groups = load(file)
        elementList =[]
        bbmodel_json = {
            "name": filename,
            "texture_size": texture_size,
            "textures": {"0":texture}, 
            "elements": [],
            # "groups" : groups
        }
        
        for element in elements:
            elementData = element
            elementName = elementData["name"]

            elementFrom = recalc(elementData["from"])
            elementTo = recalc(elementData["to"])
            
            elementRotate = elementData["rotation"]
            elementAngle = elementRotate["angle"]
            elementAxis = elementRotate["axis"]
            elementOrigin = recalc(elementRotate["origin"])
            
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

    def modelbench():
        parts, texture, texture_size = load(file)

        elementList =[]
        bbmodel_json = {
            "name": filename,
            "texture_size": texture_size,
            "textures": texture.split('/')[1]+".png", 
            "elements": [],
        }
        
        for part in parts:
            partData = part

            elementName = partData["name"]

            shapes = partData["shapes"]
            for shape in shapes:
                shapeData = shape
                elementFrom = shape["from"]
                elementTo = shape["to"]
            # elementRotate = elementData["rotation"]
            # elementAngle = elementRotate["angle"]
            # elementAxis = elementRotate["axis"]
            # elementOrigin = recalc(elementRotate["origin"])
            
            # elementOrigin = elementOrigin.tolist()
            
            # elementFace = elementData["faces"]
            
            # elementRotate = {}
            # elementRotate["angle"] = elementAngle
            # elementRotate["axis"] = elementAxis
            # elementRotate["origin"] = elementOrigin

            # elementFrom = elementFrom.tolist()
            # elementTo = elementTo.tolist()
            

            # elementList.append({
            #     "name": elementName,
            #     "from": elementFrom,
            #     "to" : elementTo,
            #     "rotation": elementRotate,
            #     "faces": elementFace
            # })
            

        bbmodel_json["elements"] = elementList

        return bbmodel_json

    if '.json' in filename:
        blockbench()
        filename = filename.replace('.json','')
    else:
        # modelbench()
        print('Unfinish')
        filename = filename.replace('.modelbench','')
    
def exportMI(filepath,filename):
    mimodel_json = convertBlock(filename)
    filepath = filepath+filename.replace('.json','')+filetype[1]
    with open(filepath, "w") as f:
        json.dump(mimodel_json, f)
        print(mimodel_json)
        # print("\n")
        # print(total_parts)

def exportBB(filepath,filename):
    bbmodel_json = convertModel(filename)
    if '.json' in filename:
        filepath = filepath+filename.replace('.json','')+filetype[0]
    else:
        filepath = filepath+filename.replace('.mimodel','')+filetype[0]
    with open(filepath, "w") as f:
        json.dump(bbmodel_json, f)
        print(bbmodel_json)

# print_json()

# exportMI(filepath,filename)
exportBB(filepath,filename)

#TODO: Reorder UV layout based on .mimodel layout

if __name__ == "__main__":
    exportMI(filepath,filename)
