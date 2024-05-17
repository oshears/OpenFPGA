def make_readme(outdir, VERTICAL_CLB_COUNT, lut_count, module_layout_grid, module_info, module_config_order, windows):

    fh = open(f"{outdir}/README.md","w+")

    fh.write("## Overview:\n")
    fh.write(f"- Name: openfpga__arch_{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}__lut_{lut_count}__tiered_luts__20240423\n")
    fh.write("- Generation Date: 04/23/2024\n")
    fh.write(f"- Architecture: {VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}\n")
    fh.write(f"- LUT Count: {lut_count}\n")
    fh.write(f"- Number of Modules : {len(module_info)}\n")
    fh.write(f"- Number of Windows (Partitions): {len(windows)}\n")

    fh.write("## Description:\n")
    fh.write(f"- Data includes {lut_count} LUTs per bitstream organized into random, cascading tiers.\n")
    fh.write("- \n")

    fh.write("## Architecture Layout:\n")

    device_width = len(module_layout_grid)

    # print module names
    fh.write("### Module Names\n")
    fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |\n")
    fh.write("|---" * device_width + "|\n")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = module_layout_grid[x][y]
            fh.write(f"| {module_layout_grid[x][y]} ")
        fh.write("|\n")

    # print configuration order
    # fh.write("### Module Configuration Order\n")
    # fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |\n")
    # fh.write("|---" * device_width + "|\n")
    # for y in range(device_width-1,-1,-1):
    #     for x in range(device_width):
    #         module_name = module_layout_grid[x][y]
    #         config_index = module_config_order.index(module_name)
    #         fh.write(f"| {config_index} ")
    #     fh.write("|\n")

    # print bit counts
    # fh.write("### Module Configuration Bit Counts\n")
    # fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |\n")
    # fh.write("|---" * device_width + "|\n")
    # for y in range(device_width-1,-1,-1):
    #     for x in range(device_width):
    #         module_name = module_layout_grid[x][y]
    #         fh.write(f"| {len(module_info[module_name])} ")
    #     fh.write("|\n")

    # fh.write("## Windows:\n")

    # for window_idx in range(len(windows)):
    #     fh.write(f"### Window #{window_idx + 1}\n")
    #     #for module in windows[window_idx]:
    #     #    fh.write(f"- {module}\n")
    #     # print module names
    #     # fh.write("### Module Names\n")
    #     fh.write(" ".join(f"| {i}" for i in range(device_width)) + " |\n")
    #     fh.write("|---" * device_width + "|\n")
    #     for y in range(device_width-1,-1,-1):
    #         for x in range(device_width):
    #             module_name = module_layout_grid[x][y]
    #             if module_name in windows[window_idx]:
    #                 fh.write(f"| <mark>**{module_layout_grid[x][y]}** ")
    #             else:
    #                 fh.write(f"| {module_layout_grid[x][y]} ")
    #         fh.write("|\n")


    fh.close()