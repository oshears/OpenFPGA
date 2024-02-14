from . import *
# from module_classes import *
# import module_pkg.module_classes.Module
from .module_classes import *

### get modules and their bit configurations from the xml bitstream file
def getModules() -> dict[str, Module]:
    print(bitstreamFile)
    tree = ElementTree.parse(bitstreamFile)
    root = tree.getroot()

    modules = {}
    for child in root:
        moduleName = child.attrib['name']

        if "clb" in moduleName: 
            modules[moduleName] = CLBModule(child.attrib['name'],"")
        else:
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