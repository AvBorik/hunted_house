# Date: 31 August 2015
# Modified by Tony Kuo, David McCurdy

# NOTE: 
# This game was created based on the book: Write Your Own Adventure Programs
# Written by Jenny Tyler, Les Howarth
# Published by Usborne computer books, 1983
# https://books.google.co.nz/books?id=f6BoAAAACAAJ

# Description: Code used for ISCG 5420 Assignment 2015 S2.
# Version no: 20150831

########################################################
#Modificated and edited by BORIS AVDEEV Date 17.10.2015#
########################################################

import random
import sys

#############################################################################################################
# GAME DATA                                                                                                 #
#############################################################################################################

# SOME CONSTANTS
HERO_INVENTORY_POS = 99

DirectionsList = ['SE', 'WE',  'WE',  'SWE', 'WE',   'WE',  'SWE',  'WS', #0-7
                   'NS', 'SE',  'WE',  'NW',  'SE',   'W',   'NE',   'NSW', #8-15
                   'NS', 'NS',  'SE',  'WE',  'NW', 'SE',  'WS', 'NS', #16-23
                   'N',  'NS',  'NSE',  'WE',  'WE',   'NSW', 'NS',   'NS', # 24 - 31
                   'S',  'NSE', 'NSW', 'S',   'NS', 'N',   'N',    'NS', #32 - 39
                   'NE', 'NSW',  'NE',  'W',   'NSE',  'WE',  'W',    'NS', #40 - 47
                   'SE', 'NSW', 'E',   'WE',  'NW',   'SE',   'SWE',   'NW', #48 - 55
                   'NE', 'NWE', 'WE',  'WE',  'WE',   'NWE', 'NWE',  'W'] #56 - 63



# '\' below is a continuation character, it tells Python that the current statement continues to the next line.
LocationsList = \
[ 'DARK CORNER',                  'OVERGROWN GARDEN',       'BY LARGE WOODPILE',         'YARD BY RUBBISH',
  'WEEDPATCH',                    'FOREST',                 'THICK FOREST',              'BLASTED TREE',
  'CORNER OF HOUSE',              'ENTRANCE TO KITCHEN',    'KITCHEN & GRIMY COOKER',    'SCULLERY DOOR',
  'ROOM WITH INCHES OF DUST',     'REAR TURRET ROOM',       'CLEARING BY HOUSE',         'PATH',
  'SIDE OF HOUSE',                'BACK OF HALLWAY',        'DARK ALCOVE',               'SHALL DARK ROOM',
  'BOTTOM OF SPIRAL STAIRCASE',   'WIDE PASSAGE',           'SLIPPERY STEPS',            'CLIFFTOP',
  'NEAR CRUMBLING WALL',          'GLOOMY PASSAGE',         'POOL OF LIGHT',             'IMPRESSIVE VAULTED HALLWAY',
  'HALL BY THICK WOODEN DOOR',    'TROPHY ROOM',            'CELLAR WITH BARRED WINDOW', 'CLIFF PATH',
  'CUPBOARD WITH HANGING COAT',   'FRONT HALL',             'SITTING ROOM',              'SECRET ROOM',
  'STEEP MARBLE STAIRS',          'DINING ROOM',            'DEEP CELLAR WITH COFFIN',   'CLIFF PATH',
  'CLOSET',                       'FRONT LOBBY',            'LIBRARY OF EVIL BOOKS',   'STUDY WITH DESK & HOLE IN WALL',
  'WEIRD COBWEBBY ROOM',          'VERY COLD CHAMBER',      'SPOOKY ROOM',               'CLIFF PATH BY MARSH',
  'RUBBLE-STREWN VERANDAH',       'FRONT PORCH',            'FRONT TOWER',               'SLOPING CORRIDOR',
  'UPPER GALLERY',                'MARSH BY WALL',          'MARSH',                     'SOGGY PATH',
  'BY TWISTED RAILING',           'PATH THROUGH IRON GATE', 'BY RAILINGS',               'BENEATH FRONT TOWER',
  'DEBRIS FROM CRUMBLING FACADE', 'LARGE FALLEN BRICKWORK', 'ROTTING STONE ARCH',        'CRUMBLING CLIFFTOP']

VerbList = ['HELP', 'CARRYING?', 'GO',    'N',       'S',       'W',     'E',   'U',      'D',
            'GET',  'TAKE',      'OPEN',  'EXAMINE', 'READ',    'SAY',
            'DIG',  'SWING',     'CLIMB', 'LIGHT',   'UNLIGHT', 'SPRAY', 'USE', 'UNLOCK', 'DROP', 'SCORE']


ItemList = ['SECRETNOTES', 'PAINTING', 'RING', 'MAGIC SPELLS', 'GOBLET', 'SCROLL', 'COINS', 'STATUE',  'CANDLESTICK', 'MATCHES',
            'VACUUM',   'BATTERIES', 'SHOVEL', 'AXE',    'ROPE',   'BOAT',  'AEROSOL','BONES', 'SALT','GAS', 'CANDLE','KEY', 'HAMMER']

PositionOfItems = [12, 46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 19, 10, 62, 100, 100, 100]

VisitedLocations =[0]

# This variable represents player's current location. Initial location is 0
currentLocation = 0
ExitGameLoop = 0
sm = 0
lastmis = 0
#############################################################################################################
# HELPER FUNCTIONS                                                                                          #
#############################################################################################################


def isMultiwordStatement(value):
    return value.find(" ") != -1

def isItemAvailableAtLocation(ItemID,location):
    return PositionOfItems[ItemID] == location

def isItemInInventory(itemName):
    ItemID = GetItemID(itemName)
    return PositionOfItems[ItemID] == HERO_INVENTORY_POS
def isItemHidden(itemName):
    # 100 is the location for hidden items. 
    ItemID = GetItemID(itemName)
    return PositionOfItems[ItemID] == 100

def GetItemID(item):
    for ItemID in range(0, len(ItemList), 1):
        if item == ItemList[ItemID]:
            return ItemID
    return -1




#############################################################################################
# GAME LOGIC                                                                                #
#############################################################################################
def SaveGame():
    global PositionOfItems, VisitedLocations, currentLocation

    SG=open("C:\Saves.txt", "w")
    PlayerLocation = str(currentLocation)
    SG.write(PlayerLocation)
    SG.write("\n")
    #
    for item in PositionOfItems:
        item = str(item)
        SG.write(item)
        SG.write("\n")
    #
    for location in LocationsList:
        loc = str(location)
        SG.write(location)
        SG.write("\n")
    #
    for loc in VisitedLocations:
        loc = str(loc)
        SG.write(loc)
        SG.write("\n")
    SG.close()

def LoadGame():
    global PositionOfItems, VisitedLocations, currentLocation, LocationList
    LG=open ("C:\Saves.txt", "r")
    currentLocation = LG.readline()
    currentLocation = int(currentLocation)
    PositionOfItems=[]
    for number in range (0,23):
        sposition = LG.readline()
        if sposition == '':
            PositionOfItems = PositonOfItems
        else:
            sposition = int(sposition)
            PositionOfItems.append(sposition)
    LocationList=[]
    for coordinate in range(0,64):
        coord = LG.readline()
        coord = str(coord).strip()
        LocationsList.append(coord)
    VisitedLocations=[]
    for number in range(0,80):
        VL = LG.readline()
        if VL == '':
            VisitedLocations = VisitedLocations
        else:
            VL =int(VL)
            VisitedLocations.append(VL)
    LG.close()
       
def GetVerbFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return sentence
    locationOfSpace=sentence.find(" ")
    return sentence[:locationOfSpace]

def GetNounFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return ""
    locationOfSpace=sentence.find(" ") + 1
    return sentence[locationOfSpace:]

def isMovementAvailable(directioncharacter):
    """
    isMovementAvailable checks whether it is possible to move in a direction in the current location


    directioncharacter - intended direction to move toward at the currentLocation
    returns True or False - based on whether the directioncharacter can be found in the String from DirectionsList[currentLocation]

    Example: 
    if directioncharacter is 'N' and DirectionsList[currentLocation] is 'NSW', this function returns True
    """
    
    dirString = DirectionsList[currentLocation]
    result = dirString.find(directioncharacter)
    if result >= 0:
        return True
    else:
        return False
    

def GetMovementDirection(statement):
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)
    if len(verb)==1:
        return verb
    if verb == 'GO':
        return noun[:1]
    return ''

def GetScore():
    score = 0
    for name in ItemList:
        if isItemInInventory(name):
            score +=1
    return score
    
#############################################################################################
# END GAME LOGIC                                                                            #
#############################################################################################

#############################################################################################
# BEGIN PRESENTATION LOGIC                                                                  #
#############################################################################################
def StartMenu():
    print("\t\t     WELCOME TO HUNTED HOUSE ver 2.0\n\t\t\t    AVAILABLE OPTIONS:")
    sm = str.upper(input("\t\t\t\tNEW GAME(NG)\n\t\t\t\tCONTINUE(CE)\n\t\t\t\t  QUIT(QT)\nYOU HAVE CHOSEN:"))
    if sm == "NEW GAME" or sm == "NG":
           Game()
    elif sm == "CONTINUE" or sm == "CE":
           LoadGame()
           Game()
    elif sm == "QUIT" or sm == "QT":
          print("YOU HAD QUIT FROM THE GAME")
          global ExitGameLoop
          ExitGameLoop==1
    else:
        print("INCORRECT OPTION,PLEASE CHECK SPLELING AND TYPE AGAIN")
        StartMenu()

def DisplayCongratulation():
    print("""
 __     __                    _       
 \ \   / /                   (_)      
  \ \_/ /__  _   _  __      ___ _ __  
   \   / _ \| | | | \ \ /\ / / | '_ \ 
    | | (_) | |_| |  \ V  V /| | | | |
    |_|\___/ \__,_|   \_/\_/ |_|_| |_|
                                      
 """)


    
def DisplayInventory():
    strItems=""
    for i in range(len(PositionOfItems)):
        if PositionOfItems[i] == HERO_INVENTORY_POS:
            strItems = strItems + " "+ ItemList[i]
    
    if len(strItems) == 0:
        strItems = "NOTHING"
    print("YOU ARE CARRYING:" + strItems)
    

def DisplayMap():

    """
     Each row of the map is consisted of 3 lines
     The first line - contains exit to North
     The second line - contains exits to West and East plus room no.
     The third line - contains exit to South
     
    """
    Line1 = ""
    Line2 = ""
    Line3 = ""
    # Use a FOR loop to draw every room
    for Index in range (0, 64, 1):
        if Index in VisitedLocations:
            # assign the exits at location 'Index' to currentValues
            # e.g. "NSW" if there are exits to North, South, and West
            currentValues=DirectionsList[Index]

            # if there is exit to the north draw a gap between the blocks
            if "N" in currentValues:
                Line1 += "█  █"
            # otherwise, draw a wall
            else:
                Line1 += "████"
                
            if "W" in currentValues:
                Line2 += (" ") + PrintableInts(Index)
            else:
                Line2 += ("█") + PrintableInts(Index)
            
                
            if "E" in currentValues:
                Line2 += " "
            else:
                Line2 += "█"

            if "S" in currentValues:
                Line3 += "█  █"
            else:
                Line3 += "████"
        else:
            Line1 += "    "
            Line2 += "    "
            Line3 += "    "
        # Draw the first row of rooms if 8 rooms have been processed.     
        if (Index + 1) % 8 == 0:
            print (Line1)
            print (Line2)
            print (Line3)
            # Emptying the lines for the next row of 8 rooms.
            Line1 = ""
            Line2 = ""
            Line3 = "" 
                                
###
def ExamineCoat():
    if currentLocation == 32 and isItemHidden("Key"):
        PositionOfItems[GetItemID("KEY")] = 32
        print ("YOU EXAMINE THE COAT AND FIND A KEY IN THE POCKET")
    elif currentLocation == 32 and not isItemHidden("Key"):
        print ("IT\'S A DIRTY OLD COAT")
    else:
        print ("WHAT COAT?")

def ExamineDrawer():
    if currentLocation == 43 and isItemInInventory("KEY") :
        print ("YOU UNLOCK THE DRAWER AND FIND IT IS EMPTY")
    elif currentLocation == 43 and not isItemInInventory("KEY") :
        print ("UNFORTUNATELY THE DRAWER IS LOCKED")
    else:
        print ("WHAT DRAWER?")

    
def ExamineRubbish():
    if currentLocation == 3:
        print ("THE RUBBISH IS FILTHY")
    else:
        print ("WHAT RUBBISH?")

def ExamineWall():
    if currentLocation == 43:
        LocationsList[currentLocation] = "STUDY WITH DESK"
        DirectionsList[currentLocation]="NW"
        print ("YOU LOOK AT THE WALL AND DISCOVER IT IS FALSE!\nYOU DISCOVER A NEW EXIT")
    else:
        print ("NO INTERESTING WALLS HERE")
def ExamineDoor():
    if currentLocation == 28 and  isItemInInventory("KEY"):
        DirectionsList[currentLocation]="SEW"
        print ("YOU UNLOCK THE DOOR AND DISCOVER A NEW LOCATION!")
    elif currentLocation == 28 and  not isItemInInventory("KEY"):
        print ("UNFORTUNATELY THE DOOR IS LOCKED")
    else:
        print ("NO INTERESTING DOOR HERE")
    
def ExamineBooks():
    if currentLocation == 42 and isItemHidden("CANDLE"):
        print ("YOU LOOK AT THE BOOKS AND FOUND A CANDLE IN BETWEEN BOOKS!")
        PositionOfItems[GetItemID("CANDLE")] = 42
    elif currentLocattion == 42 and not isItemHidden("CANDLE"):
        print ("THE BOOKS LOOK EVIL")
    else:
        print ("NO BOOKS HERE")

def ExamineSecretNotes():
    if currentLocation == 29 and isItemInInventory("SECRETNOTES"):
        PositionOfItems[GetItemID("HAMMER")] = 29
        print ("PLAYER:YEAH, NOTES WERE RIGHT!!!")
        print ("AFTER EXAMINE SECRETNOTES, YOU ARE FIND A HAMMER...MMM I SAW CRUMBLING WALL (24) ")
    elif isItemInInventory('SECRETNOTES') and not currentLocation == 29:
        print("I NEED TROPHY ROOM(29)")
    else:
        print("I DO NOT HAVE ANY NOTES")
        
#def ExamineSecretNotes():
   # if currentLocation == 12

def DoExamine(noun) :
    if noun == "COAT":
        ExamineCoat()
    elif noun == "DRAWER":
        ExamineDrawer( )
    elif noun == "RUBBISH":
        ExamineRubbish()
    elif noun == "WALL":
        ExamineWall()
    elif noun == "DOOR":
        ExamineDoor()
    elif noun == "BOOKS":
        ExamineBooks()
    elif noun == "SECRETNOTES":
        ExamineSecretNotes()

    else:
        print ("WHAT "+noun+"?")
    
def PrintableInts(Index):
    if currentLocation == Index:
     return("**")
    elif (Index <10):
        return (" ") + str(Index)
    return str(Index)
#############################################################################################
# END PRESENTATION LOGIC                                                                    #
#############################################################################################


def ListItemsAtPosition():
    strItems=""
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == currentLocation:
            strItems = strItems + " "+ ItemList[i]
    return strItems

def ItemsAvailableAtPosition():
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == currentLocation:
            return True
    return False


def Go(statement, nowLocation):
    directioncharacter = ''

    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)

    directioncharacter = verb
    if verb == 'GO':
        directioncharacter = noun[:1]
    
    if isMovementAvailable(directioncharacter):
        if directioncharacter == 'N':
            nowLocation -= 8
        elif directioncharacter == 'S':
            nowLocation += 8
        elif directioncharacter == 'W':
            nowLocation -= 1
        elif directioncharacter == 'E':
            nowLocation += 1
    return nowLocation

def GetItem(noun):
    ItemID = GetItemID(noun)
    if isItemAvailableAtLocation(ItemID,currentLocation):
        PositionOfItems[ItemID]=HERO_INVENTORY_POS
        print("YOU ARE NOW CARRYING A",noun, file=sys.stderr)
        if noun == "SECRETNOTES":
          print("SECRET NOTES: HEY EVERYONE. DO NOT TOUCH MY SECRET TOOL IN TROPHY ROOM(29)")
        elif noun == "BONES":
            print("-PLAYER THINKING: MAY BE IT IS GHOST'S BONES,I SHOULD BURN IT WITH SALT AND GAS LIKE IN SUPERNATURAL. VERGROWN GARDEN (1) MIGHT BE BETTER PLACE ")
    else:
          print("SORRY YOU CANNOT TAKE A ", noun)
    
        
def DropItem(noun):
    ItemID = GetItemID(noun)
    if isItemAvailableAtLocation(ItemID, HERO_INVENTORY_POS):
        PositionOfItems[ItemID] = currentLocation
        print("YOU HAVE DROPPED THE ", noun)
    else:
        print("YOU CANNOT DROP THAT WHICH YOU DO NOT POSSESS")

###
def OpenDoor():
    if currentLocation == 28 and isItemInInventory("KEY"):
        DirectionsList[currentLocation]="SEW"
        print("THE DOOR IS NOW OPEN! REVEALLING A NEW EXIT!")
    else:
        print("THE DOOR IS LOCKED")
def DoBreak():
    if currentLocation == 24 and isItemInInventory('HAMMER'):
        DirectionsList[currentLocation]="NS"
        print("WITH HAMMER YOU BROKE WALL AND MAKE NEW EXIT TO CUPBOARD WITH HANGING COAT (32)")
    elif currentLocation == 32 and isItemInInventory('HAMMER'):
            DirectionsList[currentLocation]="NS"
    elif currentLocation == 24 and not isItemInInventory('HAMMER'):
        print("-I NEED SOMETHING TO BREAK IT")
    else:
        print("-NOTHING TO BREAK!!!LETS GO TO NEAR CRUMBLING WALL (24)  ")
def DoBurn():
    if currentLocation == 1 and isItemInInventory('BONES') and isItemInInventory('SALT') and isItemInInventory('GAS'):
       global ExitGameLoop
       ExitGameLoop = 2
       print("CONGRATULATION, THE GHOST WAS GONE AND YOU CAN GO OUT")
    else:
        print("I NEES SOMETHING MORE")
    
        
def ProcessStatement(statement):
    global currentLocation
    '''
      A statement can be either a verb or a verb + a noun
      If a statement is consisted of 1 verb and 1 noun, (separated by a space), it can looks like 'examine desk', 'get axe' ..etc
    '''
    
    verb=GetVerbFromSentence(statement)
    noun=GetNounFromSentence(statement)    

    if verb== "HELP" or verb == "HP":
        print("""HELP(HP)\t- Display all possible actions you can carry out in this game\nSCORE(SE)\t- Display your current score
INVENTORY(IY)\t- Display your inventory\nGET(GT) \t- To get items in locations\nOPEN DOOR(OD)\t- To open doors\nDROP(DP)\t- To drop items from inventory
EXAMINE(EE)\t- To examine items\nSHOW MAP(SM)\t- To show map\nN,S,W,E \t- directions\nQUIT(QT)\t- To exit from game\nBREAK(BK)\t- To break something\nBURN(BN)\t- To burn something 
""")

    elif verb == "SCORE" or verb == "SE":
        print("YOUR CURRENT SCORE IS:", GetScore())

    elif verb == "INVENTORY" or verb == "IY":
        DisplayInventory()

    elif verb == "GET" or verb == "GT" :
        GetItem(noun)

    elif verb == "OPEN" and noun == "DOOR":
        OpenDoor()

    elif verb == "OD":
        OpenDoor()
        
    elif verb == "DROP" or verb == "DP":
        DropItem(noun)

    elif verb == "EXAMINE" or verb == "EE":
        DoExamine(noun)

    elif verb == "SHOW" and noun == "MAP":
        DisplayMap()

    elif verb == "SM":
        DisplayMap()

    elif verb == 'N' or verb == 'S' or verb == 'E' or verb == 'W' or verb == 'U' or verb == 'D' or verb == 'GO':  
        newLocationID = Go(statement,currentLocation)
        if currentLocation != newLocationID:
            print("YOU MOVED FROM " + LocationsList[currentLocation] + " TO " + LocationsList[newLocationID], file=sys.stderr)
        else:
            print("YOU ARE UNABLE TO MOVE IN THAT DIRECTION")
        currentLocation = newLocationID
    elif verb == "TELEPORT" or verb == "TT":
        noun = int(GetNounFromSentence(statement))
        if noun >= 0 and noun <=63:
            currentLocation = noun
            print ("YOU ARE ENABLE TELEPORT CHEAT TO MOVE IN", LocationsList[currentLocation])

        else:
            print("ERROR: WRONG LOCATION ID, PLEASE CHECK NEDDED LOCATION ID")

    elif verb == "QUIT" or verb == "QT":
         global ExitGameLoop
         ExitGameLoop = 1

    elif verb == "GIVEME" or verb == "GE":
        print("YOU ARE ENABLE GIVEME CHEAT, AVAILABLE ITEMS TO GET", ItemList)
        cheatItem = input ("WHICH ITEM DO YOU WANT TO GET?")
        cheatItem = cheatItem.upper()
        if cheatItem in ItemList:
            ItemID = GetItemID(cheatItem)
            PositionOfItems[ItemID] = HERO_INVENTORY_POS
            print(cheatItem, "IN YOUR BAG")
            if cheatItem =="SECRETNOTES":
                print("SECRET NOTES: HEY EVERYONE. DO NOT TOUCH MY SECRET TOOL IN TROPHY ROOM(29)")
            elif cheatItem == "BONES":
               print("-PLAYER THINKING: MAY BE IT IS GHOST'S BONES,I SHOULD BURN IT WITH SALT AND GAS LIKE IN SUPERNATURAL.VERGROWN GARDEN (1) -MIGHT BE BETTER.")
            elif cheatItem == "HAMMER":
               print ("YOU ARE FIND A HAMMER...MMM I SAW CRUMBLING WALL (24) ")
        else:
            print("INVALID ITEM, PLEASE CHECK SPELLING")

    elif verb == "BREAK" or verb == "BK":
        DoBreak()

    elif verb == "BURN" or verb == "BN":
        DoBurn()
          
    
# Existing missions:
# Go to location 32 and 'examine coat' to find a key
# Go to location 28 and 'open door' with the key in inventory.

# Go to location 43 and 'examine wall' to find a new exit into a secret room.

def Game():
    global ExitGameLoop
    # Win condition: pick up more than 5 items and go back to location 0
    while not ExitGameLoop >= 1 or(GetScore() >= 5 and currentLocation == 0):
    
        print("========Haunted House=========")
        print("YOU ARE LOCATED IN A ", LocationsList[currentLocation],"("+str(currentLocation)+")")
        if ItemsAvailableAtPosition():
            print("YOU CAN SEE THE FOLLOWING ITEMS AT THIS LOCATION: ", ListItemsAtPosition())
        print("VISIBLE EXITS: ", DirectionsList[currentLocation])
        DisplayMap()
        statement = str.upper (input("WHAT DO YOU WANT TO DO NEXT?"))
        ProcessStatement(statement)
        if not (currentLocation in VisitedLocations):
            VisitedLocations.append(currentLocation)
    if ExitGameLoop == 1:
          SaveGame()
          print ("YOU HAD QUIT FROM THE GAME")
          if ExitGameLoop == 2:
            DisplayCongratulation()
     
    else:
        DisplayCongratulation()

# Program starts here!
StartMenu()

