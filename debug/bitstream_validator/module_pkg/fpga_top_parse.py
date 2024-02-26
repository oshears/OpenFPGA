# from __init__ import *
from . import *

from .module_classes import *


class Connection:
    def __init__(self, wireName, parentWireName=None):
        self.wireName = wireName
        self.parentWireName = parentWireName
        self.connections:[IO] = []
        self.modules:[str] = []

    def addConnection(self, moduleName, connection):
        if connection == None:
            raise Exception("Error: Attempted to add null connection")
        self.connections.append(connection)
        self.modules.append(moduleName)

    def makeLinks(self):
        # TODO: I need to fix this
        if len(self.connections) > 1:
            # if self.connections[0].nextIO == None and self.connections[1].nextIO != None:
            #     self.connections[0].setNextIO(self.connections[1])
            # elif self.connections[1].nextIO == None and self.connections[0].nextIO != None:
            #     self.connections[1].setNextIO(self.connections[0])

            # first find the driving io
            numDrivers = 0
            driver = None
            others = []
            for io in self.connections:
                if io.direction == "output":
                    driver = io
                    numDrivers += 1
                else:
                    others.append(io)

            # raise exception if no drivers found or multiple drivers found
            if numDrivers != 1:
                raise Exception()
            
            # now assign the other wires as the next of this driver
            for otherIO in others:
                driver.addNextIO(otherIO,True)

    
    def __str__(self):
        if len(self.connections) >= 2:
            # print(self.wireName)
            # print(self.connections)
            # print(self.modules)
            return f"{self.wireName} : ({self.modules[0]}.{self.connections[0].name}, {self.modules[1]}.{self.connections[1].name})"
        return self.wireName
        

## This method takes in a list of the modules parsed from the bitstream and maps the 
## connections between each of the modules in the fpga_top.v file
## the result is a modified modules dictionary with each of the IO being connected (after calling makeLinks())
def parseTop(modules, resultsPath):
    wires = {}

    top_fh = open(f"{resultsPath}/SRC/fpga_top.v")
    fpga_top_lines = top_fh.readlines()


    ## loop though each line of the fpga_top.v file
    for line in fpga_top_lines:
        # skip lines that have "tail"
        if "tail" not in line:
            # if a wire definition is found, then get its size and add it to the dict of wires  
            if x := re.match(r"wire\s+\[\d+:(\d+)\]\s+(\S+);", line):
                size = int(x.group(1))+1
                wireName = x.group(2)
                if size > 1:
                    for i in range(size):
                        # parentWireName = f"{x.group(2)}[0:{size - 1}]"
                        wireName = f"{x.group(2)}[{i}]"
                        parentWireName = x.group(2)
                        wires[wireName] = Connection(wireName,parentWireName)
                else:
                    wires[wireName] = Connection(wireName)
                
    ## get input mappings
    currModule = None
    currModuleType = None

    # for each line in fpga_top.v
    for line in fpga_top_lines:

        # ignore all of these connections since they aren't relevant to the bitstream
        parseLine = ("prog_clk" not in line) and ("ccff_head" not in line) and ("ccff_tail" not in line) and ("set" not in line) and ("reset" not in line) and ("clk" not in line) and ("gfpga_pad_GPIO_PAD" not in line)
        
        # if we have a valid line to parse
        if parseLine:

            # if the line is a module definition line
            if x := re.match(r"\s+(\S+) (\S+) \(", line):

                # save the module name and type
                currModuleType = x.group(1)
                currModule = x.group(2)
            
            # if the current line is a module port line
            elif x := re.match(r"\s+.(\S+)\((\S+)\),", line):

                # identify the current module port detected
                modulePort = x.group(1)
                
                # identify the name of the wire that the port connects to
                wireName = x.group(2)
                wireSize = 1

                # check if the wire is a multi-bit wire
                if y := re.match(r"(\S+)\[\d+:(\d+)\]", wireName):

                    # if it is multi-bit, then get the wire name and size
                    wireName = y.group(1)
                    wireSize = int(y.group(2)) + 1

                    # prepare to add sveral IO/wire associations to the wires dictionary
                    # connectionList = []

                    # for each wire in the multi-bit wire
                    for i in range(wireSize):

                        # get the IO for the current module
                        moduleIO = modules[currModule].getIO(f"{modulePort}[{i}]")

                        # ensure the IO was found
                        if moduleIO == None or currModule == None:
                            raise Exception()

                        
                        # assuming it was found correctly,
                        # add a connection between the IO for the current module and the corresponding wire
                        wires[f"{wireName}[{i}]"].addConnection(currModule,moduleIO)
                
                # if it's not a multi-bit wire...
                else:

                    # get the IO for the current module
                    moduleIO = modules[currModule].getIO(modulePort)

                    # ensure the IO was found
                    if moduleIO == None or currModule == None:
                        raise Exception()
                    
                    # assuming it was found correctly,
                    # add a connection between the IO for the current module and the corresponding wire
                    wires[wireName].addConnection(currModule,moduleIO)

    
    # for wireName, wire in wires.items():
    #     if len(wire.connections) > 1:
    #         # TODO: this might not be working in the best way, need to fix
    #         if wire.connections[0].nextIO == None and wire.connections[1].nextIO != None:
    #             wire.connections[0].setNextIO(wire.connections[1])
    #         elif wire.connections[1].nextIO == None and wire.connections[0].nextIO != None:
    #             wire.connections[1].setNextIO(wire.connections[0])

    for wireName, wire in wires.items():
        wire.makeLinks()


    return wires

# if __name__ == "__main__":
#     parseTop()
