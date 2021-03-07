import json
import os

import numpy as np

blockbench = "sweetheart.json"
filepath = ".\\storage\\"
file = filepath + blockbench

os.system('cls')

def load(file): # Load mimodel and Minecraft json
    with open(file, "r") as fileObject:
        data = json.load(fileObject) 
        try: #Exception  No "elements" found
            elements = data["elements"] # Extract "elements"
            # print(elements)
            return elements
        except KeyError:
            parts = data["parts"] # Through "parts" extract "shapes"
            # print(parts[0]['shapes'])
            return parts[0]['shapes']

def convertBlock(filename):  
    # print('Blockbench to Modelbench')
    mimodel_json = {
        "name": filename,
        "texture": "Default texture.png",
        # default Inherit texture. how Modelbench get texture file? filepath? 
        "texture_size": [ 16, 16 ]
        # default based on Inherit texture
    }
    e = 0
    parts = []
    elements = load(file)
    for element in elements: # Extract "elements" list
        part = element
        if e == 0:
            fill = ""
        else:
            fill = " " + str(e)
        try: # Exception No "name" found. 
            partName = part["name"] + fill
        except KeyError:
            partName = "cube"+ fill
        e+=1

        shape = element
        shapeFrom = shape["from"]
        shape = element
        shapeTo = shape["to"]
        origin = []
        position = []
        rotation = []
        shape = []
        shape.append({ # Cluttered?
            "type": "block",
            "description": partName + " shape",
            "texture": "Default texture.png",
            "texture_size": [ 16, 16 ],
            # "color_blend": "#000000",
			# "color_mix": "#FFFFFF",
			# "color_mix_percent": 1,
			# "color_brightness": 0,
            "from": shapeFrom,
            "to": shapeTo,
            "uv": [ 0, 0 ], # TODO: new UV map based on calculation
            "position": origin, # offset shape using part "rotation"
            "rotation" : [0 , 0 , 0 ],
            "scale" : [ 1, 1, 1 ]
        })
        parts.append({
            "name": partName,
            # "color_blend": "#000000",
			# "color_mix": "#FFFFFF",
			# "color_mix_percent": 1,
			# "color_brightness": 0,
            "position": position,     # this gonna be *a lot* of PIVOT OFFSET
            "rotation": rotation,    # TODO:angle based on one axis 
                                        # "rotation": {
                                        #         "angle",
                                        #         "axis" }
                                        
            "scale": [ 1, 1, 1 ],
            "shapes": shape
        })
    mimodel_json["parts"] = parts


    with open(filepath+filename+".mimodel", "w") as f:
        json.dump(mimodel_json, f)
        # print('                             ')
        print(mimodel_json)

convertBlock(filename="sweetheart")





#TODO: Reorder UV layout based on .mimodel layout
def layoutUV(filename): 
    UV = None
def load_test(): #testing rewrite mimodel file. just for fun check
    with open("MI_model.mimodel", "r") as fileObject:
        data = json.load(fileObject)
    print(data)

    with open("rewrite.mimodel", "w") as f:
        json.dump(data, f)
# load_test()
