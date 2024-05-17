import re

def config_chain_extraction(top_level_file:str):

    print("Extracting the configuration chain...")

    fh = open(top_level_file,"r+")

    lines = fh.readlines()

    moduleOrder = []

    module_count = 0

    # TODO: This is temporary
    total_num_modules = 7393
    intervals = total_num_modules // 100

    lastConfigChainNet = "ccff_head"
    while lastConfigChainNet != "ccff_tail":
        
        currentModule = ""
        findTail = False
        for line in lines:
            
            if x := re.search(r"\t(\S+) (\S+) \(", line):
                currentModule = x.group(2)

            if f".ccff_head({lastConfigChainNet})" in line:
            # if x := re.search(r"\t\t.ccff_head\((\S+)\);", line):
                moduleOrder.append(currentModule)
                module_count += 1

                if module_count % intervals == 0:
                    print(f"Modules Found: {module_count} / {total_num_modules} ({100 * module_count / total_num_modules}%)")

                # print(f"Found Module #{module_count}: ")
                # print(currentModule)
                # print("\t Head: " + lastConfigChainNet)
                findTail = True

            if findTail:
                if x := re.search(r"\t\t.ccff_tail\((\S+)\)\);", line):
                    # print("\t Tail:" + lastConfigChainNet)
                    lastConfigChainNet = x.group(1)
                    break
    
    moduleOrder.reverse()

    return moduleOrder


# top_level = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/SRC/fpga_top.v"
# results = config_chain_extraction(top_level)
# print(results)