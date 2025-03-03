import sys
from enum import Enum

# Enum for reuse and extendability. Really just to prevent dev skill issues and make changes values easier, if need be.
class commands(str, Enum):
    Create = "CREATE"
    Move = "MOVE"
    Delete = "DELETE"
    List = "LIST"
    Exit = "exit"

# Using a tree structor for our,,, file tree.
class virtualFileTree:
    # This is a brute force solution, and in a real system we'd either want to keep track of a parent, and when an object has no parent it's the root,
    # or use reserved characters that only this can use. For this example, I used characters that are marked in windows as not acceptable for filenames.
    ROOT_DIR_TAG = "><"
    
    # adding children so more complex trees can be created to start with
    def __init__(self, folderName, children):
        self.name = folderName
        # Keeping children as a list. I thought about converting it to a dictionary to make insertion and retreval times
        # better, however the list operation becomes more complicated. Since this is a file system application, it is unlikely
        # that rapid performance for thousands of folders would be nessisary. This could be revised though.
        self.children = children
        pass
    
    # Add child is O(n), where N is the number of children of self. This is because we sort on insertion, instead of on print.
    # There is a design case for where we'd prefer inserion to be quicker than print.
    def addChild(self, child):
        self.children.append(child)
        # mantaining sorted order so we don't re-sort on print.
        self.children.sort(key=lambda child : child.name)
        
    # O(n), as we loop through the list. Using a dict or hashmap/set could make this O(1)
    def hasChild(self, childName):
        return len([child for child in self.children if child.name == childName]) > 0
    
    # O(n). We could make this faster, but we'd need a dict/hashmap/hashset
    def getChild(self, childName):
        for child in self.children:
            if child.name == childName:
                return child
    
    # O(n). We could make this faster, but we'd need a dict/hashmap/hashset
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
                #this is a depth first pre-order search, in print form.
                depthFirstPrint(fileTree)
            case _ :
                print(f"{command[0]} Invalid command, exiting...")
                exit(1)

def executeFileSystemCommandsFromUser():
    print("Running with stdin.\nCommands will all be executed after exit command has been given.")
    commandList = []
    while True:
        command = input()
        # This is here instead of in the isValidCommand, because of control flow.
        if command.split(" ")[0] == commands.Exit:
            break
        if isValidCommand(command):
            commandList.append(command)
        else:
            print("Invalid Command. Try from list: (CREATE, MOVE, DELETE, LIST, exit)")

    print("\nExecuting now...\n\n")
    fileTree = virtualFileTree(virtualFileTree.ROOT_DIR_TAG, [])
    for command in commandList:
        executeCommand(fileTree, command)

def executeFileSystemCommandListFromFile(filePath):
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
        # run with stdin
        case 1:
            executeFileSystemCommandsFromUser()
        case 2:
            executeFileSystemCommandListFromFile(sys.argv[1])