from xml.etree import ElementTree
import csv

baseDir = "/home/oshears/Documents/openfpga/OpenFPGA"

resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/run014/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"

bitstreamFile = f"{resultsPath}/fabric_independent_bitstream.xml"


moduleFile = f"{resultsPath}/SRC/routing/sb_0__2_.v"
moduleName = "sb_0__2_"
moduleType = "sb_0__2_"

csvBitstream = f"{baseDir}/debug/bitstream_validator/sample_bitstream.csv"


module_order = [
    "grid_io_bottom_1__0_",
    "grid_io_bottom_2__0_",
    "grid_io_right_3__1_",
    "grid_io_right_3__2_",
    "sb_2__2_",
    "cbx_2__2_",
    "grid_io_top_2__3_",
    "sb_1__2_",
    "cbx_1__2_",
    "grid_io_top_1__3_",
    "sb_0__2_",
    "sb_0__1_",
    "cby_0__2_",
    "grid_io_left_0__2_",
    "sb_0__0_",
    "cby_0__1_",
    "grid_io_left_0__1_",
    "sb_1__0_",
    "cbx_1__0_",
    "cby_1__1_",
    "grid_clb_1__1_",
    "sb_2__0_",
    "cbx_2__0_",
    "cby_2__1_",
    "grid_clb_2__1_",
    "sb_2__1_",
    "cbx_2__1_",
    "cby_2__2_",
    "grid_clb_2__2_",
    "sb_1__1_",
    "cbx_1__1_",
    "cby_1__2_",
    "grid_clb_1__2_"
]
module_order.reverse()


## Classes
class RoutingNode:
    def __init__(self, name="", type="", path="", numBits:int=1, values:[int]=None):
        self.name = name
        self.type = type
        self.path = path 

        if values:
            self.values = values   
        else:
            self.values = numBits * [0]

    def setValues(self,values:[int]):
        self.values = values

    def __str__(self) -> str:
        return f"{self.path} : {self.values.__str__()}"
    
class IO:
    def __init__(self, name:str="", direction:str="input"):
        self.name = name
        self.direction = direction
        self.nextIO = None
    
    def __str__(self) -> str:
        return f"{self.name} {'output' if self.direction else 'input'} (Next: {self.nextIO.name if self.nextIO else None})"
    
    def setNextIO(self,nextIO):
        self.nextIO = nextIO

class LUTNode(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize2Node,self).__init__(name,"lut4_DFF_mem",path,16,values)

class LUTFFNode(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize2Node,self).__init__(name,"mem_ble4_out_0",path,2,values)

class MuxTreeSize2Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize2Node,self).__init__(name,type,path,2,values)

    def getInputChoice(self) -> int:
            if self.values[0]:
                if self.values[1]:
                    return 0
                else:
                    return 1
            else:
                return None
                
class MuxTreeSize8Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize8Node,self).__init__(name,type,path,4,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 0
                    else:
                        return 1
                else:
                    return 2
            else:
                if self.values[3]:
                    return 3
                else: 
                    return 4
        else:
            if self.values[1]:
                if self.values[2]:
                    return 5
                else:
                    return 6
            else:
                if self.values[2]:
                    return 7
                else:
                    return None

class Module:
    def __init__(self, name, type, numBits:int=0):
        self.name = name
        self.type = type
        self.numBits = numBits=0
        self.nodes = []
        self.io = {}
        self.input2output_maps = {}

    def addNode(self,node:RoutingNode):
        # self.nodes[node.path] = node
        self.nodes.append(node)
    
    def addIO(self, io:IO):
        self.io[io.name] = io
    
    def getIO(self, ioName:str):
        for io in self.io.keys():
            if io == ioName:
                return self.io[io]

    def mapIO(self, inputName:str, outputName:str):
        # self.input2output_maps[inputName] = outputName
        inputIO = self.getIO(inputName)
        outputIO = self.getIO(outputName)
        inputIO.setNextIO(outputIO)

    def __str__(self) -> str:
        nodeStrings = [f'\t({node.__str__()})\n' for node in self.nodes]
        nodeStrings = "".join(nodeStrings)
        return f"{self.name}:\n{nodeStrings}"
    


### Tasks
    
### 1. Make graph connecting each node
    
### get modules and their bit configurations
def getModules() -> dict[str, Module]:
    print(bitstreamFile)
    tree = ElementTree.parse(bitstreamFile)
    root = tree.getroot()

    modules = {}
    for child in root:
        moduleName = child.attrib['name']
        modules[moduleName] = Module(child.attrib['name'],"")
        
    for primitive in root.findall(".//bitstream/.."): # iterate through all nodes with a bitstream child
        path = "/".join([f"{primitive[0][i].attrib['name']}" for i in range(1,len(primitive[0]))])
        topModuleName = primitive[0][1].attrib["name"]
        
        bits = [int(primitive[-1][i].attrib["value"]) for i in range(len(primitive[-1])-1,-1,-1)]
        
        node = RoutingNode(primitive[0][-1].attrib["name"],primitive[0][-1].attrib["name"],path,len(bits),bits)

        modules[topModuleName].addNode(node)
        
    
    ## write modules and routing nodes out to file
    fh = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/bit_configs/fullConfig.bit","w+")
    # fh.write(modules["cbx_1__2_"].__str__())
    for moduleName in module_order:
        # print(module)
        modules[moduleName].nodes.reverse()
        fh.write(modules[moduleName].__str__())
        fh_module = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/bit_configs/{moduleName}.bit","w+")
        fh_module.write(modules[moduleName].__str__())
        fh_module.close()
    fh.close()

    return modules


### get muxes and io, and map them to the modules
def mapMuxes(modules:dict[str,Module]):

    # moduleName = "sb_0__0_"
    moduleName = "cbx_1__2_"

    # ioCsvFile
    with open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{moduleName}.io","r+") as ioCsvFile:
        reader = csv.reader(ioCsvFile)
        next(reader)
        for io in reader:
            if int(io[1]) == 1:
                newIO = IO(io[0],io[2])
                modules[moduleName].addIO(newIO)
            else:
                for i in range(int(io[1])):
                    newIO = IO(io[0] + f"[{i}]",io[2])
                    modules[moduleName].addIO(newIO)
            

    with open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{moduleName}.mux","r+") as muxCsvFile:
        reader = csv.reader(muxCsvFile)
        next(reader)
        newNodes = []
        for muxLine in reader:

            if "wire" in muxLine[1]:
                modules[moduleName].mapIO(muxLine[2],muxLine[-1])

            else:
                for node in modules[moduleName].nodes:
                    
                    muxMemName = "mem" + muxLine[0][3:]

                    if node.name == muxMemName:

                        if "size2" in muxLine[1]:

                            newNode:MuxTreeSize2Node = MuxTreeSize2Node(node.name,muxLine[1],node.path,node.values)
                            newNodes.append(newNode)

                            muxChoice = newNode.getInputChoice()
                            if muxChoice != None:
                                print(f"{muxLine[2+muxChoice]}")
                                print(f"{muxLine[-1]}")
                                modules[moduleName].mapIO(muxLine[2+muxChoice],muxLine[-1])
                            else:
                                if ("".join(map(str,node.values)) != "00"):
                                    print("Routing node was not defaulted but still returned CONST1")
                                    print(f"\tValues: {node.values}")

                        if "size8" in muxLine[1]:

                            newNode:MuxTreeSize2Node = MuxTreeSize8Node(node.name,muxLine[1],node.path,node.values)
                            newNodes.append(newNode)

                            muxChoice = newNode.getInputChoice()
                            if muxChoice != None:
                                print(f"{muxLine[2+muxChoice]}")
                                print(f"{muxLine[-1]}")
                                modules[moduleName].mapIO(muxLine[2+muxChoice],muxLine[-1])
                            else:
                                if ("".join(map(str,node.values)) != "0000"):
                                    print("Routing node was not defaulted but still returned CONST1")
                                    print(f"\tValues: {node.values}")

                            # else:
                            #     print("NO MATCH")


        modules[moduleName].nodes = newNodes

    
    for io in modules[moduleName].io.values():
        print(io)


if __name__ == "__main__":
    modules = getModules()
    mapMuxes(modules)
