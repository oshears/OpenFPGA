from . import *
# from __init__ import *

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

class GPIO_PAD(RoutingNode):
    def __init__(self, name="", type="", path="", numBits:int=1, value:int=0):
        super(GPIO_PAD,self).__init__(name,type,path,numBits,[value])
        self.value = value

    def getSetting(self):
        return "out_pad" if self.value else "in_pad"

class IO:
    def __init__(self, name:str="", module:str="", direction:str="input"):
        self.name = name
        self.direction = direction
        self.nextIO = None
        self.moduleName = module
    
    def __str__(self) -> str:
        return f"{self.moduleName}.{self.name} {'output' if self.direction else 'input'} (Next: {f'{self.nextIO.moduleName}.{self.nextIO.name}' if self.nextIO else None})"
    
    def setNextIO(self,nextIO):
        self.nextIO = nextIO

class Module:
    def __init__(self, name, type, numBits:int=0):
        self.name = name
        self.type = type
        self.numBits = numBits=0
        self.nodes = []
        self.io:[str, IO] = {}
        self.input2output_maps = {}

    def addNode(self,node:RoutingNode):
        # self.nodes[node.path] = node
        self.nodes.append(node)
    
    def addIO(self, io:IO):
        self.io[io.name] = io
    
    def getIO(self, ioName:str) -> IO:
        for io in self.io.keys():
            if io == ioName:
                return self.io[io]

    def mapIO(self, inputName:str, outputName:str, node=None):
        # self.input2output_maps[inputName] = outputName
        inputIO = self.getIO(inputName)
        outputIO = self.getIO(outputName)
        inputIO.setNextIO(outputIO)

    def __str__(self) -> str:
        nodeStrings = [f'\t({node.__str__()})\n' for node in self.nodes]
        nodeStrings = "".join(nodeStrings)
        return f"{self.name}:\n{nodeStrings}"

class CLB_IO(IO):
    def __init__(self, driverName:str="", module:str="", ioName:str="",idx=-1, input_idx=-1):
        super(CLB_IO,self).__init__(driverName,module,"clb_io")
        self.idx = idx
        self.input_idx = input_idx
        self.driverName = driverName
        self.ioName = ioName

    def __str__(self) -> str:
        if self.idx > -1 and self.input_idx > -1:
            return f"{self.driverName} => {self.ioName} => FLE_{self.idx}.I_{self.input_idx}"
        else:
            return f"{self.name} 'wire' (Next: {self.nextIO.name if self.nextIO else None})"

class CLB:
    def __init__(self, idx=-1, input_idx=-1):
        self.idx = idx
        self.input_idx = input_idx

class CLBModule(Module):
    def __init__(self, name, type, numBits:int=0):
        super(CLBModule,self).__init__(name,type,numBits)

        self.internalIO = {}

    def mapIO(self, inputName:str, outputName:str, node):
        if x := re.match(r"mem_fle_(\d+)_in_(\d+)", node.name):
            # fle_num = int(x.group(1))
            # fle_input = int(x.group(2))
            fleInput = CLB_IO(inputName,self.name,outputName,int(x.group(1)),int(x.group(2)))
            fleInput.setNextIO( CLB(int(x.group(1)),int(x.group(2))) )
            self.addIO(fleInput)

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
            
class MuxTreeSize3Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize3Node,self).__init__(name,type,path,2,values)

    def getInputChoice(self) -> int:
            if self.values[0]:
                if self.values[1]:
                    return 0
                else:
                    return 1
            else:
                if self.values[1]:
                    return 2
                else:
                    return None

class MuxTreeSize4Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize4Node,self).__init__(name,type,path,3,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    return 0
                else:
                    return 1
            else:
                return 2
        else:
            if self.values[1]:
                return 3
            else:
                return None

class MuxTreeSize5Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize5Node,self).__init__(name,type,path,3,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    return 0
                else:
                    return 1
            else:
                if self.values[2]:
                    return 2
                else:
                    return 3
        else:
            if self.values[1]:
                return 4
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

class MuxTreeSize9Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize9Node,self).__init__(name,type,path,4,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 0
                    else:
                        return 1
                else:
                    if self.values[3]:
                        return 2
                    else:
                        return 3
            else:
                if self.values[2]:
                    return 4
                else: 
                    return 5
        else:
            if self.values[1]:
                if self.values[2]:
                    return 6
                else:
                    return 7
            else:
                if self.values[2]:
                    return 8
                else:
                    return None

class MuxTreeSize11Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize11Node,self).__init__(name,type,path,4,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 0
                    else:
                        return 1
                else:
                    if self.values[3]:
                        return 2
                    else:
                        return 3
            else:
                if self.values[2]:
                    if self.values[3]:
                        return 4
                    else:
                        return 5
                else:
                    if self.values[3]:
                        return 6
                    else:
                        return 7
        else:
            if self.values[1]:
                if self.values[2]:
                    return 8
                else:
                    return 9
            else:
                if self.values[2]:
                    return 10
                else: 
                    return None

class MuxTreeSize12Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize12Node,self).__init__(name,type,path,4,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 0
                    else:
                        return 1
                else:
                    if self.values[3]:
                        return 2
                    else:
                        return 3
            else:
                if self.values[2]:
                    if self.values[3]:
                        return 4
                    else:
                        return 5
                else:
                    if self.values[3]:
                        return 6
                    else:
                        return 7
        else:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 8
                    else:
                        return 9
                else:
                    return 10
            else:
                if self.values[2]:
                    return 11
                else: 
                    return None
                
class MuxTreeSize14Node(RoutingNode):
    def __init__(self, name="", type="", path="", values:[int]=None):
        super(MuxTreeSize14Node,self).__init__(name,type,path,4,values)

    def getInputChoice(self) -> int:
        if self.values[0]:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 0
                    else:
                        return 1
                else:
                    if self.values[3]:
                        return 2
                    else:
                        return 3
            else:
                if self.values[2]:
                    if self.values[3]:
                        return 4
                    else:
                        return 5
                else:
                    if self.values[3]:
                        return 6
                    else:
                        return 7
        else:
            if self.values[1]:
                if self.values[2]:
                    if self.values[3]:
                        return 8
                    else:
                        return 9
                else:
                    if self.values[3]:
                        return 10
                    else:
                        return 11
            else:
                if self.values[2]:
                    if self.values[3]:
                        return 12
                    else:
                        return 13
                else:
                    return None