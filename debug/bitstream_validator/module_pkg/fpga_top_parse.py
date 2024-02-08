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
        if len(self.connections) > 1:
            if self.connections[0].nextIO == None and self.connections[1].nextIO != None:
                self.connections[0].setNextIO(self.connections[1])
            elif self.connections[1].nextIO == None and self.connections[0].nextIO != None:
                self.connections[1].setNextIO(self.connections[0])

    
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
def parseTop(modules):
    wires = {}

    top_fh = open(f"{resultsPath}/SRC/fpga_top.v")
    # for line
    fpga_top_lines = top_fh.readlines()


    ## get wires
    for line in fpga_top_lines:
        if "tail" not in line:
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
                
                # if size > 0:
                #     wires.append(f"{wireName}[0:{size}]")
                # else:
                #     wires.append(wireName)
    
    ## get input mappings
    currModule = None
    currModuleType = None
    for line in fpga_top_lines:
        parseLine = ("prog_clk" not in line) and ("ccff_head" not in line) and ("ccff_tail" not in line) and ("set" not in line) and ("reset" not in line) and ("clk" not in line) and ("gfpga_pad_GPIO_PAD" not in line)
        if parseLine:
            if x := re.match(r"\s+(\S+) (\S+) \(", line):
                currModuleType = x.group(1)
                currModule = x.group(2)
            elif x := re.match(r"\s+.(\S+)\((\S+)\),", line):
                # TODO: Make the grid_io connections between FPGA inputs and outputs
                # TODO: Make the clb connections
                if "grid_io" not in currModule and "clb" not in currModule: # DEBUG: Remove Later
                    modulePort = x.group(1)
                    
                    wireName = x.group(2)
                    wireSize = 1
                    if y := re.match(r"(\S+)\[\d+:(\d+)\]", wireName):
                        wireName = y.group(1)
                        wireSize = int(y.group(2)) + 1

                        connectionList = []
                        for i in range(wireSize):
                            moduleIO = modules[currModule].getIO(f"{modulePort}[{i}]")
                            if moduleIO == None or currModule == None:
                                raise Exception()
                            connectionList.append(moduleIO)
                            wires[f"{wireName}[{i}]"].addConnection(currModule,moduleIO)

                    else:
                        moduleIO = modules[currModule].getIO(modulePort)
                        if moduleIO == None or currModule == None:
                            raise Exception()
                        wires[wireName].addConnection(currModule,moduleIO)

    for wire in wires.values():
        wire.makeLinks()
        print(wire)

    return wires

# if __name__ == "__main__":
#     parseTop()
