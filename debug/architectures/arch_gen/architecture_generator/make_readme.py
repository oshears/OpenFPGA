from windows_4x4 import *

def make_readme(outdir):

    fh = open(f"{outdir}/README.md","w+")

    fh.write("## Overview:\n")
    fh.write("Name: openfpga__arch_4x4__lut_60__tiered_luts__20240423\n")
    fh.write("Generation Date: 04/23/2024\n")
    fh.write("Architecture: 4x4\n")
    fh.write("LUT Count: 64 - 4 (60)\n")

    fh.write("## Description:\n")
    fh.write("- Data includes 60 LUTs per bitstream organized into random, cascading tiers.\n")
    fh.write("- ")

    fh.write("## Architecture Layout:\n")

    fh.write("## Windows:\n")

    for window in windows_4x4:
        for module in window:
            fh.write(f"- {module}\n")


    fh.close()