from typing import List, Union
from . import *
# from __init__ import *

## Classes
class RoutingNode:
    def __init__(self, name="", type="", path="", numBits:int=1, values:List[int]=None):
        self.name = name
        self.type = type
        self.path = path 
        self.selectedInput = None
        self.muxOutput = None
        self.desc = ""
        self.sinks = None

        if values:
            self.values = values   
        else:
            self.values = numBits * [0]

    def setValues(self, values:List[int]):
        self.values = values

    def __str__(self) -> str:
        if self.sinks is None:
            return f"{self.path} : {self.values.__str__()} ({self.desc})"
        else:
            return f"{self.path} : {self.values.__str__()} ({self.desc}) ({','.join(self.sinks)})"
            
    
    def setSelectedInput(self, selectedInput):
        self.selectedInput = selectedInput
    
    def setMuxOutput(self, muxOutput):
        self.muxOutput = muxOutput
        
    def hasConfigBits(self):
        return 1 in self.values
    
    def isLut(self):
        return "lut4_DFF_mem" in self.type
    
    def isLutOutput(self):
        return "mem_ble4_out_0" in self.type
    
    def setMuxDescription(self, desc):
        self.desc = desc
    
    def setSink(self, sink):
        self.sinks = [sink]
    
    def addSink(self, sink):
        if self.sinks is None:
            self.sinks = [sink]
        else:
            self.sinks.append(sink)

class GPIO_PAD(RoutingNode):
    def __init__(self, name="", type="", path="", value:int=0):
        super(GPIO_PAD,self).__init__(name,type,path,1,[value])
        self.value = value

    def getSetting(self):
        return "in_pad" if self.value else "out_pad"

class IO:
    def __init__(self, name:str="", module:str="", direction:str="input"):
        self.name = name

        if direction != "input" and direction != "output" and direction != "inout":
            raise Exception()
        
        self.direction = direction
        self.nextIO:List[IO] = []
        self.prevIO:List[IO] = []
        self.moduleName = module
        self.nextioIsDirect = []
        self.previoIsDirect = []
        self.mux:RoutingNode = None
    
    def __str__(self) -> str:
        outputString = ""
        outputString += f"{self.moduleName}.{self.name} " 
        outputString += f"{self.direction} " 
        # outputString += f"{'DIRECT_WIRE' if self.connectsDirectlyToNext else ''} " 

        if len(self.nextIO) == 0:
            outputString += "(Next: None)"
        else:
            outputString += "(Next: "
            for ioIndex in range(len(self.nextIO)):
                # outputString += f"(Next: {f'{self.nextIO.moduleName}.{self.nextIO.name}' if self.nextIO else None})" 
                isDirectConnectionStr = "DIRECT_WIRE " if self.nextioIsDirect[ioIndex] else ""
                outputString += f"{isDirectConnectionStr}{f'{self.nextIO[ioIndex].moduleName}.{self.nextIO[ioIndex].name}'}, " 
            outputString += ")"

        return outputString
    
    def addNextIO(self, nextIO, connectsDirectlyToNext:bool=False):
        self.nextIO.append(nextIO)
        self.nextioIsDirect.append(connectsDirectlyToNext)
        self.nextIO[-1].addPrevIO(self, connectsDirectlyToNext)

        if self.direction == "inout":
            self.direction = "input"
    
    def addPrevIO(self, prevIO, connectsdirectlyToPrev:bool=False):
        self.prevIO.append(prevIO)
        self.previoIsDirect.append(connectsdirectlyToPrev)

        if self.direction == "inout":
            self.direction = "output"
    
    def hasNextIO(self):
        return len(self.nextIO) > 0
    
    def hasPrevIO(self):
        return len(self.prevIO) > 0

class Module:
    def __init__(self, name, type, numBits:int=0):
        self.name = name
        self.type = type
        self.numBits = numBits=0
        self.nodes = []
        self.io:Union[str, IO] = {}
        self.input2output_maps = {}

    def addNode(self, node:RoutingNode):
        self.nodes.append(node)
    
    def addIO(self, io:IO):
        self.io[io.name] = io
    
    def getIO(self, ioName:str) -> IO:
        for io in self.io.keys():
            if io == ioName:
                return self.io[io]
        raise Exception(f"IO {ioName} does not exist in module: {self.name}")

    def mapIO(self, inputName:str, outputName:str, directConnection=False):
        if inputName == outputName:
            raise Exception("Cannot map and IO back to itself!")
        inputIO = self.getIO(inputName)
        outputIO = self.getIO(outputName)
        inputIO.addNextIO(outputIO, directConnection)

    def __str__(self) -> str:
        nodeStrings = [f'\t({node.__str__()})\n' for node in self.nodes]
        nodeStrings = "".join(nodeStrings)
        return f"{self.name}:\n{nodeStrings}"

class CLB_IO(IO):
    def __init__(self, name:str="", module:str="",):
        super(CLB_IO,self).__init__(name, module,"input")
        self.internal = True

class CLBModule(Module):
    def __init__(self, name, type, numBits:int=0):
        super(CLBModule,self).__init__(name,type,numBits)

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
                if self.values[2]:
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