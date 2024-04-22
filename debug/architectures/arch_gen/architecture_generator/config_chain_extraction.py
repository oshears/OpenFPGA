import re

def config_chain_extraction(top_level_file:str):

    fh = open(top_level_file,"r+")

    lines = fh.readlines()

    moduleOrder = []

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
                print(currentModule)
                print("\t Head: " + lastConfigChainNet)
                findTail = True

            if findTail:
                if x := re.search(r"\t\t.ccff_tail\((\S+)\)\);", line):
                    print("\t Tail:" + lastConfigChainNet)
                    lastConfigChainNet = x.group(1)
                    break
    
    return moduleOrder


# top_level = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/SRC/fpga_top.v"
# results = config_chain_extraction(top_level)
# print(results)