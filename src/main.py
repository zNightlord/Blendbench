import sys

from .json_convert import convert_blockbench as blockbench
from .json_convert import convert_modelbench as modelbench

filepath = ''
newFilepath = ''
offset = False

# convert Blockbench to Modelbench JSON
def convert_Blockbench(filepath,newFilepath):
    blockbench.export(filepath,newFilepath,offset)

# convert Modelbench to Blockbench JSON
def convert_Modelbench(filepath,newFilepath,offset):
    modelbench.export(filepath,newFilepath,offset)


