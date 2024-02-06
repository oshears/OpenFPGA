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
    def __init__(self, name="", type="", path="", size:int=1, values:[int]=None):
        self.name = name
        self.type = type
        self.path = path 

        if values:
            self.values = values   
        else:
            self.values = size * [0]

    def setValues(self,values:[int]):
        self.values = values

    def __str__(self) -> str:
        return f"{self.path} : {self.values.__str__()}"
    
class MuxTreeSize8Node(RoutingNode):
    def __init__(self, name="", type="", path="", size:int=1, values:[int]=None):
        super.__init__(name,type,path,8,values)

    def getInputChoice(self) -> int:
        if self.values[3]:
            if self.values[2]:
                if self.values[1]:
                    if self.values[0]:
                        return 0
                    else:
                        return 1
                else:
                    return 2
            else:
                if self.values[1]:
                    return 3
                else: 
                    return 4
        else:
            if self.values[2]:
                if self.values[1]:
                    return 5
                else:
                    return 6
            else:
                if self.values[1]:
                    return 7
                else:
                    return None

class Module:
    def __init__(self, name, type, numBits:int=0):
        self.name = name
        self.type = type
        self.bits = numBits=0
        self.nodes = []

    def addNode(self,node:RoutingNode):
        self.nodes.append(node)

    def __str__(self) -> str:
        nodeStrings = [f'\t({node.__str__()})\n' for node in self.nodes]
        nodeStrings = "".join(nodeStrings)
        return f"{self.name}:\n{nodeStrings}"
    

# node = RoutingNode(2)
# print(node)

### Tasks
### 1. Make graph connecting each node

if __name__ == "__main__":
    print(bitstreamFile)
    tree = ElementTree.parse(bitstreamFile)
    root = tree.getroot()



    total_bit_length = 0
    bit_dict = {}
    modules = {}
    for child in root:
        moduleName = child.attrib['name']
        modules[moduleName] = Module(child.attrib['name'],"")
        
    for primitive in root.findall(".//bitstream/.."): # iterate through all nodes with a bitstream child
        path = "/".join([f"{primitive[0][i].attrib['name']}" for i in range(1,len(primitive[0]))])
        topModuleName = primitive[0][1].attrib["name"]
        
        bits = [int(primitive[-1][i].attrib["value"]) for i in range(len(primitive[-1])-1,-1,-1)]
        
        node = RoutingNode("",primitive[0][-1].attrib["name"],path,len(bits),bits)

        modules[topModuleName].addNode(node)
        
    
    ## write modules and routing nodes out to file
    fh = open(f"{baseDir}/debug/bitstream_validator/out.txt","w+")
    # fh.write(modules["cbx_1__2_"].__str__())
    for moduleName in module_order:
        # print(module)
        modules[moduleName].nodes.reverse()
        fh.write(modules[moduleName].__str__())
    fh.close()
    