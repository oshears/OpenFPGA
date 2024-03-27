from module_pkg.module_classes import *

from typing import List, Union


def displayRoutes(modules:Union[str, Module]):
    fh = open(f"./debug/bitstream_validator/results/outRoutes.txt","w+")
    for modName, mod in modules.items():
        fh.write(f"{modName}\n")
        for io in mod.io.values():
            if io.nextIO != None:
                fh.write(f"\t{io}\n")
    fh.close()