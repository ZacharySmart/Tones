import math
import random
import time
import copy
import re

frets = 24
strings = 6
from graphics import*


multimode=0
windows=[]
currentWinObjects=[]
activeScales=0
myImage=None
currentScale=None
lastWinName="generic"

winx=0
winy=0

win = GraphWin("neut",0,0)

rendered=0

def fretBoardRender(winName):
    
    global winx,winy,win,fretWidth,fretHeight,currentWinObjects, lastWinName
    global activeScales, myImage
    myImage = Image(Point(400,300), "fretboard.png")
    winy=myImage.getHeight()
    winx=myImage.getWidth()

    win = GraphWin(winName,winx,winy)
    lastWinName=winName
    currentScales=0

    myImage = Image(Point(winx/2,winy/2), "fretboard.png")
    myImage.draw(win)

    fretWidth=winx/frets
    fretHeight=winy/(strings-1)

    z=0
    while z<strings:
        iterString=Line(Point(0,winy-(fretHeight*z)),(Point(winx,winy-(fretHeight*z))))
        iterString.setWidth(4)
        iterString.draw(win)
        currentWinObjects.append(iterString.clone())
        z+=1
    """draw strings"""
    z=0
    while z<frets:
        iterString=Line(Point((z+1)*fretWidth,0),(Point((z+1)*fretWidth,winy)))
        iterString.setWidth(2)
        iterString.setFill("brown")
        iterString.draw(win)
        currentWinObjects.append(iterString.clone())
        z+=1

    """draw frets"""

    c=1
    while c<=frets:
        if ((c%12==3) or (c%12==5) or (c%12==9) or (c%12==7)):
            cir=Circle(Point((winx/frets)*c-.5*(winx/frets),(winy/2)),7)
            cir.draw(win)
            currentWinObjects.append(cir.clone())
        if (c%12==0):
            cir=Circle(Point((winx/frets)*c-.5*(winx/frets),(winy-(fretHeight)*1.5)),7)
            cir.draw(win)
            currentWinObjects.append(cir.clone())
            cir=Circle(Point((winx/frets)*c-.5*(winx/frets),(winy-(fretHeight)*3.5)),7)
            cir.draw(win)
            currentWinObjects.append(cir.clone())
        c+=1

    """draw fretboard dots"""
    global rendered
    rendered=1

def refresh(winName):
    global win, myImage, windows,currentWinObjects,lastWinName
    if multimode:
        durr= GraphWin(lastWinName,winx,winy)
        for i in currentWinObjects:
            try:
                i.draw(durr)
            except:
                continue
        windows.append(durr)
    else:
        for i in windows:
            i.close()
        currentWinObjects=[]
    win.close()
    fretBoardRender(winName)

x = int(0)

modeLib = [
    "ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian",
    "locrian"
]

scaleLib={"ionian": [2,2,1,2,2,2,1],
          "dorian": [2,1,2,2,2,1,2],
          "phrygian":[1,2,2,2,1,2,2],
          "lydian": [2,2,2,1,2,2,1],
          "mixolydian": [2,2,1,2,2,1,2],
          "minor": [2,1,2,2,1,2,2],
          "locrian":[1,2,2,1,2,2,2],
          "harmonic_minor": [2,1,2,2,1,3,1],
          "locrian_natural 6": [1,2,2,1,3,1,2],
          "ionian_diminished": [2,1,3,1,2,1,2],
          "phrygian_dominant": [1,3,1,2,1,2,2],
          "aeolian_harmonic": [3,1,2,1,2,2,1],
          "ultralocrian":[1,2,1,2,2,1,3],
          "melodic_minor":[2,1,2,2,2,2,1],
          "lydian_dominant":[2,2,2,1,2,1,2],
          "mixolydian_b6":[2,2,1,2,1,2,2],
          "minor_pentatonic":[3,2,2,3,2],
          "blues_scale":[3,2,1,1,3,2],
          "major_pentatonic":[2,2,3,2,3],
          "minor_triad":[3,4,5]
          }

toneLib = [
    "En0", "Fn0", "F#0", "Gn0", "G#0", "An0", "A#0", "Bn0", "Cn0", "C#0", "Dn0","D#0",
    "En1", "Fn1", "F#1", "Gn1", "G#1", "An1", "A#1", "Bn1", "Cn1", "C#1", "Dn1", "D#1",
    "En2", "Fn2", "F#2", "Gn2", "G#2", "An2", "A#2", "Bn2", "Cn2", "C#2", "Dn2", "D#2",
    "En3", "Fn3", "F#3", "Gn3", "G#3", "An3", "A#3", "Bn3", "Cn3", "C#3", "Dn3", "D#3",
    "En4", "Fn4", "F#4", "Gn4", "G#4", "An4", "A#4", "Bn4", "Cn4", "C#4", "Dn4", "D#4",
    "En5", "Fn5", "F#5", "Gn5", "G#5", "An5", "A#5", "Bn5", "Cn5", "C#5", "Dn5", "D#5",
    "En6", "Fn6", "F#6", "Gn6", "G#6", "An6", "A#6", "Bn6", "Cn6", "C#6", "Dn6", "D#6",
    "En7", "Fn7", "F#7", "Gn7", "G#7", "An7", "A#7", "Bn7", "Cn7", "C#7", "Dn7", "D#7",
    "En8", "Fn8", "F#8", "Gn8", "G#8", "An8", "A#8", "Bn8", "Cn8", "C#8", "Dn8", "D#8",
    "En9", "Fn9", "F#9", "Gn9", "G#9", "An9", "A#9", "Bn9", "Cn9", "C#9", "Dn9", "D#9"
]
"""a generic library of tones, from lowest E to highest D#"""

curToneLib=[]

"""a list of current tones for rendering, in Int"""

tuneLib = {"standard": [24, 29, 34, 39, 43, 48],
           "standard8":[24, 29, 34, 39, 43, 48,53,58],
"drop_d": [22, 29, 34, 39, 43, 48],"all_fifths": [24,31,38,45,52,59]
           }

fretArray = [[None] * frets] * strings

currentRoot="F#"

def validColor(hex):
    return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex)

def randomColor():
    while True:
        random_number = random.randint(0,(8388607))
        hex_number = str(hex(random_number))
        hex_number ='#'+ hex_number[2:]
        if validColor(hex_number):
            return hex_number
        else:
            continue



def convert(lst):
    return (lst.split())

def populateFrets(tuning):
    i = 0
    while i < strings:
        stringArray=[None]*frets
        v = 0
        while v < frets:
            baseNoteNum = tuneLib[tuning][i]
            stringArray[v] = (toneLib[baseNoteNum + v + 1])
            v += 1
        fretArray[i]=stringArray
        i += 1


def drawNote(stringNum,note,color,size):
    if note in (fretArray[stringNum]):
        cir=Circle(Point((((winx/frets)*fretArray[stringNum].index(note))+(winx/frets)/2),(winy-((winy/(strings-1))*(stringNum)))),size-(activeScales*2))
        cir.setFill(color)
        cir.draw(win)
        currentWinObjects.append(cir.clone())
    elif toneLib.index(note)==((toneLib.index(fretArray[stringNum][0]))-1):
        cir=Circle(Point(0,(winy-((winy/(strings-1))*(stringNum)))),size-(activeScales*2))
        cir.setFill(color)
        cir.draw(win)
        currentWinObjects.append(cir.clone())
def notesToLib(note):
    for i in toneLib:
        if note in i:
            curToneLib.append(toneLib.index(i))
"""appends every octave of a given note to the current tones collection"""
def scaleDef(key,scale):
    global currentRoot, currentScale
    global curToneLib
    curToneLib=[]
    floatNote="neut"
    notesToLib(key)
    noteIndex=toneLib.index(key+"0")
    for i in scaleLib[scale]:
            noteIndex+=i
            floatNote=toneLib[noteIndex]
            notesToLib(floatNote[:-1])
    currentRoot=key
    currentScale=scale



def wholeFretboard():
    global activeScales
    colOne="red"
    colTwo="black"
    if activeScales>0:
        while True:
            colOne=randomColor()
            colTwo=randomColor()
            if validColor(colOne) and validColor(colTwo):
                break
            else:
                continue
    s=0
    while s<strings:
        for i in curToneLib:
            if (currentRoot in toneLib[i]):
                drawNote(s,toneLib[i],colOne,10)
            else:
                drawNote(s,toneLib[i],colTwo,10)
        s+=1
    activeScales+=1

def removeDuplicates(listofElements):

    # Create an empty list to store unique elements
    uniqueList = []

    # Iterate over the original list and for each element
    # add it to uniqueList, if its not already there.
    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)

    # Return the list of unique elements
    return uniqueList

def organize(aList):
    aList.sort()
    newArr=aList
    newArr=removeDuplicates(newArr)
    aList=newArr
    return (aList)

def notesPerString(root,nps):
    global activeScales
    colOne="red"
    colTwo="black"
    if activeScales>0:
        colOne=randomColor()
        colTwo=randomColor()

    newList=organize(curToneLib)
    rootStart=0
    s=0
    if nps<3:
        rootStart-=1
    while s<strings:
        n=0
        while n<nps and ((len(newList))>0):
            if (toneLib[newList[0]] in fretArray[s]):
                if (root in toneLib[newList[0]]):
                    drawNote(s,toneLib[newList.pop(0)],colOne,10)
                    rootStart+=1
                else:
                    if rootStart:
                        drawNote(s,toneLib[newList.pop(0)],colTwo,10)
                    else:
                        newList.pop(0)
                if rootStart:
                    n+=1
            elif (toneLib[newList[0]+1]==fretArray[s][0]):
                if (root in toneLib[newList[0]]):
                    drawNote(s,toneLib[newList.pop(0)],colOne,10)
                    rootStart+=1
                else:
                    if rootStart:
                        drawNote(s,toneLib[newList.pop(0)],colTwo,10)
                    else:
                        newList.pop(0)
                if rootStart:
                    n+=1
            else:
                newList.pop(0)
                continue
        s+=1

    activeScales+=1

populateFrets("standard")



while (True):
    y = (input("Input>"))
    if y == ('q'):
        print("Quitting...")
        break
    y=convert(y)
    if "n" in y:
        activeScales=0
    if (y[0]=="nps"):
        y.pop(0)
        try:
            str(y[0])
        except:
            try:
                int(y[0])
            except:
                print ("proper input please")
                continue
            else:
                if "n" in y or not rendered:
                    refresh(currentRoot+" "+currentScale+" "+(y[0]))
                notesPerString(currentRoot,int(y[0]))
                continue
        else:
            if "n" in y or not rendered:
                refresh((y[0])+" "+currentScale+" "+(y[1]))
            notesPerString((y[0]),int(y[1]))
            continue
    if (y[0]=="scaleDef"):
        try:
            scaleDef(y[1],y[2])
        except:
            print ("please input a valid scale (check spelling)")
    if (y[0]=="wholeFretboard"):
        if "n" in y or not rendered:
            refresh(currentRoot+" "+currentScale+" "+(y[0]))
        wholeFretboard()
    if (y[0]=="tuning"):
        try:
            populateFrets(y[1])
        except:
            print ("please input valid tuning(check spelling)")
    if y[0]=="multimode":
        if not multimode:
            print ("multi mode on>")
            multimode=1
        else:
            print ("multi mode off>")
            multimode=0
    if y[0]=="help" or y[0]=="h":
        print ("commands: \n note-per-string mode: nps note number/string \n enable multiple windows: multimode \n set scale: scaleDef root scalename \n change tuning: tuning tune_name \n quit: q \n >add 'n' to the end of your command to display in a new window (closes old windows when multimode is off)")


