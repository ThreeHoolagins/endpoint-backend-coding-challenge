import sys
from enum import Enum
import time

class commands(str, Enum):
    Create = "CREATE"
    Move = "MOVE"
    Delete = "DELETE"
    List = "LIST"
    Exit = "exit"

class virtualFileTree:
    ROOT_DIR_TAG = "><"
    
    # adding children so more complex trees can be created to start with
    def __init__(self, folderName, children):
        self.name = folderName
        # this is a list. This makes my life hard, but I'm too deep now to convert it to a dictionary
        self.children = children
        pass
    
    def addChild(self, child):
        self.children.append(child)
        # mantaining sorted order so we don't re-sort on print
        self.children.sort(key=lambda child : child.name)
        
    def hasChild(self, childName):
        return len([child for child in self.children if child.name == childName]) > 0
    
    def getChild(self, childName):
        for child in self.children:
            if child.name == childName:
                return child
    
    def removeChild(self, childName):
        self.children = [child for child in self.children if child.name != childName]
    
def isValidCommand(command):
    commandArgs = command.split(" ")
    if commandArgs[0] == commands.Create or commandArgs[0] == commands.Delete:
        return len(commandArgs) == 2
    elif commandArgs[0] == commands.Move:
        return len(commandArgs) == 3
    elif commandArgs[0] == commands.List:
        return len(commandArgs) == 1
    else:
        print("NO COMMAND: " + commandArgs[0])
        return False
    
def depthFirstPrint(fileTreeRoot, depth=0):
    if (fileTreeRoot.name != virtualFileTree.ROOT_DIR_TAG):
        print(" " * depth + fileTreeRoot.name)
    # print children in order
    if len(fileTreeRoot.children) > 0:
        for child in fileTreeRoot.children:
            if (fileTreeRoot.name != virtualFileTree.ROOT_DIR_TAG):
                depthFirstPrint(child, depth+2)
            else:
                depthFirstPrint(child)
    
def executeCommand(fileTree, command):
    print(command)
    commandArgs = command.split(" ")
    match (commandArgs[0]):
            case commands.Create:
                pathToCreate = commandArgs[1].split("/")
                ref = fileTree
                for index, pathSection in enumerate(pathToCreate):
                    if ref.hasChild(pathSection):
                        ref = ref.getChild(pathSection)
                    else:
                        if(index == len(pathToCreate) - 1):
                            ref.addChild(virtualFileTree(pathSection, []))
                        else:
                            print(f"Cannot create {commandArgs[1]} - {pathSection} does not exist")
                            break
            case commands.Move:
                pathToMoveFrom = commandArgs[1].split("/")
                pathToMoveTo = commandArgs[2].split("/")
                
                findRef = fileTree
                refToMove = fileTree
                for index, pathSection in enumerate(pathToMoveFrom):
                    if findRef.hasChild(pathSection):
                        if index == len(pathToMoveFrom) - 1:
                            temp = findRef.getChild(pathSection)
                            findRef.removeChild(pathSection)
                            findRef = temp
                        else:
                            findRef = findRef.getChild(pathSection)
                    else:
                        print(f"Cannot move {commandArgs[1]} - {pathSection} does not exist")
                        break
     
                for index, pathSection in enumerate(pathToMoveTo):
                    if refToMove.hasChild(pathSection):
                        if index == len(pathToMoveTo) - 1:
                            refToMove = refToMove.getChild(pathSection)
                            refToMove.addChild(findRef)
                        else:
                            refToMove = refToMove.getChild(pathSection)
                    else:
                        print(f"Cannot move to {commandArgs[2]} - {pathSection} does not exist")
                        break
            case commands.Delete:
                pathToCreate = commandArgs[1].split("/")
                ref = fileTree
                for index, pathSection in enumerate(pathToCreate):
                    if ref.hasChild(pathSection):
                        if(index == len(pathToCreate) - 1):
                            ref.removeChild(pathSection)
                        else:
                            ref = ref.getChild(pathSection)
                    else:
                        print(f"Cannot delete {commandArgs[1]} - {pathSection} does not exist")
                        break
            case commands.List:
                #this is a depth first search
                depthFirstPrint(fileTree)
            case _ :
                print(f"{command[0]} Invalid command, exiting...")
                exit(1)

# todo: fix bad name omegalol
def main():
    print("Running with stdin")
    #todo: print out how to exit
    lastInput = ""
    commandList = []
    while True:
        command = input()
        if command.split(" ")[0] == commands.Exit:
            break
        if isValidCommand(lastInput):
            commandList.append()
        else:
            print("Invalid Command. Try from list: (CREATE, MOVE, DELETE, LIST)")
            
        print("User entered: " + lastInput)
        
    fileTree = virtualFileTree(virtualFileTree.ROOT_DIR_TAG, [])
    for command in commandList:
        executeCommand(fileTree, command)
    # give output

#todo make better name
def mainWithFile(filePath):
    print(f"doing directorties with {filePath}")
    readFile = open(filePath, "r")
    commandList = []
    for line in readFile:
        line = line.strip()
        if isValidCommand(line):
            commandList.append(line)
        else:
            print("File not properly formatted. Please only include valid commands (CREATE, MOVE, DELETE, LIST) and do not have any spare lines")
            exit(1)
            
    fileTree = virtualFileTree(virtualFileTree.ROOT_DIR_TAG, [])
    for command in commandList:
        executeCommand(fileTree, command)



if __name__ == "__main__":
    match len(sys.argv):
        case 1:
            # run with stdin
            main()
        case 2:
            # run with  file
            mainWithFile(sys.argv[1])
        