from . import *
# from module_classes import *
# import module_pkg.module_classes.Module
from .module_classes import *


def follow_route_for(modules:Union[str, Module]):

    fh = open("./debug/bitstream_validator/results/follow.route","w")

    currModule:Module = modules["sb_2__0_"]
    startIo:IO = currModule.getIO("left_bottom_grid_top_width_0_height_0_subtile_6__pin_inpad_0_")
    
    follow_io_route(startIo, fh)

    fh.close()

    return

def follow_io_route(currIo:IO, fh, level=1):

    connectedIo = currIo.nextIO

    fh.write(level*"\t" + f"{currIo}\n")

    for io in connectedIo:
        follow_io_route(io,fh,level+1)