from . import *
# from module_classes import *
# import module_pkg.module_classes.Module
from .module_classes import *

from xml.etree import ElementTree

def getModules(baseDir, bitstreamFile, module_order) -> dict[str, Module]:
    '''
    get modules and their bit configurations from the xml bitstream file
    '''
    
    tree = ElementTree.parse(bitstreamFile)
    root = tree.getroot()

    modules = {}

    # loop through each child module and create a class for it
    for child in root:
        moduleName = child.attrib['name']

        if "clb" in moduleName: 
            modules[moduleName] = CLBModule(child.attrib['name'],"")
        else:
            modules[moduleName] = Module(child.attrib['name'],"")

    # iterate through all nodes with a bitstream child
    for configNode in root.findall(".//bitstream/.."): 
        path = "/".join([f"{configNode[0][i].attrib['name']}" for i in range(1,len(configNode[0]))])
        topModuleName = configNode[0][1].attrib["name"]
        
        bits = [int(configNode[-1][i].attrib["value"]) for i in range(len(configNode[-1])-1,-1,-1)]
        
        node = None

        # if "lut4_DFF_mem" in path:
            
        # else:
        node = RoutingNode(configNode[0][-1].attrib["name"],configNode[0][-1].attrib["name"],path,len(bits),bits)

        # Configure Descriptions of LUT and FF config bits       
        if 'grid_clb' in topModuleName:     
            # lut init data
            if 'lut4_DFF_mem' in node.path:
                node.setMuxDescription("lut init data")
            # lut ff config
            elif 'mem_ble4_out_0' in node.path:
                node.setMuxDescription("lut ff config")
            else:
                node.setMuxDescription("lut input config")
        elif 'gpio' in topModuleName:
            node.setMuxDescription("gpio config")
        # sb
        elif 'sb_' in topModuleName:
            node.setMuxDescription("sb routing mux")
        # cb
        elif 'cbx' in topModuleName or 'cby' in topModuleName:
            node.setMuxDescription("cb routing mux")
            # if 'outpad' in node.muxOutput.name:
            #     node.setMuxDescription("cb outpad config")
            # else:
            #     node.setMuxDescription("cb clb input config")

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