def make_readme(outdir, device_width, lut_count, module_layout_grid, module_info, windows):

    fh = open(f"{outdir}/README.md","w+")

    fh.write("## Overview:\n")
    fh.write(f"Name: openfpga__arch_{device_width}x{device_width}__lut_{lut_count}__tiered_luts__20240423\n")
    fh.write("Generation Date: 04/23/2024\n")
    fh.write(f"Architecture: {device_width}x{device_width}\n")
    fh.write(f"LUT Count: {lut_count}\n")

    fh.write("## Description:\n")
    fh.write(f"- Data includes {lut_count} LUTs per bitstream organized into random, cascading tiers.\n")
    fh.write("- ")

    fh.write("## Architecture Layout:\n")

    # print module names
    fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = module_layout_grid[x][y]
            fh.write(f"| {module_layout_grid[x][y]} ")
        fh.write("|\n")

    # print configuration order
    fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = module_layout_grid[x][y]
            config_index = module_layout_grid.index(module_name)
            fh.write(f"| {config_index} ")
        fh.write("|\n")

    # print bit counts
    fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = module_layout_grid[x][y]
            fh.write(f"| {len(module_info[module_name])} ")
        fh.write("|\n")

    fh.write("## Windows:\n")

    for window in windows:
        for module in window:
            fh.write(f"- {module}\n")


    fh.close()