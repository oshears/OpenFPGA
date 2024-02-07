from module_pkg.module_classes import *
from module_pkg.fpga_top_parse import *
from module_pkg.module_graph import *

if __name__ == "__main__":
    modules:dict[str, Module] = getModules()
    parseModules()
    mapMuxes(modules)
    displayRoutes(modules)
    parseTop(modules)
