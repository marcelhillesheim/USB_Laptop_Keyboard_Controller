"""
    Copyright 2019 Marcel Hillesheim
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

"""
author: Marcel Hillesheim

input:
textfile in same folder with the fpc pins pair of the key in the order of the array keys
output:
matrix column and row teensy pin order
AND
key matrix
AND
modifierkey matrix

Description:
https://www.instructables.com/id/How-to-Make-a-USB-Laptop-Keyboard-Controller/

little tool to help creating a matrix for a teensy usb-keyboard

its not pretty but functional :d
"""
seperator="-----------------------------------------------------"


from enum import Enum
import os

class Keytype(Enum):
    KEY=1
    MODIFIER=2
    FN=3
    # for all-one matrix
    ONE=4

class Key:
    isassigned=False
    def __init__(self,label,modifiervalue,pin1,pin2):
        self.label = label
        self.pin1 = pin1
        self.pin2 = pin2
        self.type = Keytype.KEY
        # generate keytype from label
        for keytype in Keytype:
            if(label.startswith(keytype.name)):
               self.type=keytype
        # check if user set the keytype
        for keytype in Keytype:
            if(modifiervalue==keytype.name):
                self.type=keytype
keys=[]
    
con_pin=[23, 0, 22, 1, 24, 2, 21, 3, 25, 4, 20, 5, 19, 6, 18, 7, 17, 8, 16, 9, 15, 10, 14, 11, 26, 12]
#resultlist for inputpins
inputpins=[]
#resultlist for outputpins
outputpins=[]


# fileinput
# go through list of filenames and check if file exists
filenamelist=["Keyboard_with_number_pad.txt","Keyboard_without_number_pad.txt"]
for filename in filenamelist:
    if os.path.exists(filename):
        with open(filename) as file:
            content = file.readlines()
        break
try:
    content = [x.strip() for x in content]
# if no file exists inform user and offer to enter their own filename
except:
    print("No file found. The name of the textfile should be one of these")
    print(filenamelist)
    with open(input("Or enter your own filename: ")) as file:
        content = file.readlines()
    content = [x.strip() for x in content]
# read in file and store values line by line into key objects
for line in content:
    line=line.split()
    # save key objects in array
    if len(line)>=3:
        keys.append(Key(line[0],line[1],int(line[-1]),int(line[-2])))
# initialize matrix creator by finding common pins of Shift key
temporary=[]
temporary.append(keys[0].pin1)
temporary.append(keys[1].pin1)
temporary.append(keys[0].pin2)
temporary.append(keys[1].pin2)
# determine if there is a common pin (count>1)
temporary=list(set([i for i in temporary if temporary.count(i)>1]))
if (temporary!=[]):
    outputpins.append(temporary.pop())

# if no common pin found ask user for initial input
if(outputpins==[]):
    outputpins.append(int(input("NO common pin found for shift. Please enter a outputpin: ")))
print("initial outputpin:"+str(outputpins[0]))
# iterate until no new outputpins or inputpins get found
found=True
while(found==True):
    found=False
    for key in keys:
        # if not already assigned
        if key.isassigned==False:
            # set partner pin to the opposite array e.g. pin1 outputpin -> pin2 inputpin
            if key.pin1 in outputpins:
                inputpins.append(key.pin2)
                key.isassigned=True
                found=True
            elif key.pin1 in inputpins:
                outputpins.append(key.pin2)
                key.isassigned=True
                found=True
            elif key.pin2 in outputpins:
                inputpins.append(key.pin1)
                key.isassigned=True
                found=True
            elif key.pin2 in inputpins:
                outputpins.append(key.pin1)
                key.isassigned=True
                found=True

inputpins=list(set(inputpins))
outputpins=list(set(outputpins))
inputpins.sort()
outputpins.sort()
# Output results
print(seperator+"\nResults:\n"+seperator)
# print FPC pins
print("FPC PINS:")
print("\n"+str(len(inputpins))+" inputpins:")
print(inputpins)
print("\n"+str(len(outputpins))+" outputins:")
print(outputpins)
print(seperator+"\nTEENSY PINS (these have to be copied to the arduino file):")
# translate FPC pins to TEENSY pins using the con_pin array
print("\n"+str(len(inputpins))+" inputpins:")
print(list(map(lambda x: con_pin[x-1], inputpins)))
print("\n"+str(len(outputpins))+" outputins:")
print(list(map(lambda x: con_pin[x-1], outputpins)))
# create the different matrices for every keytype
for keytype in Keytype:
    matrix=seperator+"\n"+keytype.name+"\n"+seperator+"\n{\n"
    # rows
    for outputpin in outputpins:
        keyrow=""
        # colums
        for inputpin in inputpins:
            # default keyvalue
            keylabel="0"
            if keytype==Keytype.ONE:
                keylabel="1"
            # search for key that matches with row and column pin
            for key in keys:
                if (((key.pin1==inputpin) |(key.pin2==inputpin))&((key.pin1==outputpin) | (key.pin2==outputpin))):
                    if key.type==keytype:
                        keylabel=key.label
            keyrow=keyrow+"'"+keylabel+"',"
        matrix=matrix+"{"+keyrow[:-1]+"},\n"
    matrix=matrix[:-1]+"\n}"
    print(matrix)
input(seperator+"\nFinished")

        
            
            

    
        

    
        
        



    
    
    

