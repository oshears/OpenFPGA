import random
import os
import shutil

def generate_il_designs():
    design_dir = "./results/random_designs"

    shutil.rmtree(design_dir)
    os.mkdir(design_dir)

    class Wire:
        def __init__(self,name,lut,idx,dir):
            self.name = name
            self.lut = lut
            self.idx = idx
            self.dir = dir

    for i in range(20000):

        index = i
        index_str = f"{(index + 1)}".zfill(5)
        
        os.mkdir(f"{design_dir}/{index_str}")
        # fh = open(f"{design_dir}/{index_str}/design.il","w+")
        fh = open(f"{design_dir}/{index_str}/design.v","w+")

        NUM_LUTS = 16
        NUM_LUT_INPUTS = 4
        NUM_INPUTS = 4

        wires = []
    

        fh.write(f"# design #: {index_str}\n")
        fh.write(f"# num luts #: {NUM_LUTS}\n")
        fh.write(f"autoidx 140\n")
        fh.write(f"attribute \\top 1\n")
        fh.write(f"module \\fpga_design\n")
        # for lut_input_idx in range(NUM_INPUTS):
        #     fh.write(f"fpga_in_{lut_input_idx}, ")
        # for lut_idx in range(NUM_LUTS):
        #     if lut_idx < NUM_LUTS - 1:
        #         fh.write(f"fpga_out_{lut_idx}, ")
        for lut_input_idx in range(NUM_INPUTS):
            fh.write(f"  wire input {lut_input_idx} \\fpga_in_{lut_input_idx}\n")
        
        for lut_idx in range(NUM_LUTS):
            fh.write(f"  wire output {NUM_INPUTS + lut_idx + 1} \\fpga_out_{lut_idx}\n")

                
        # randomize connections between LUTs with wires
        for lut_idx in range(NUM_LUTS):

            ## randomly assign lut inputs
            shuffled_input_indexes = list(range(NUM_INPUTS))
            random.shuffle(shuffled_input_indexes)
            # for lut_input_idx in range(NUM_LUT_INPUTS):

            ## instantiate LUT
            # fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${964 + lut_idx}\n")
            # fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${lut_idx}\n")
            fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${lut_idx}\n")
            lut_string = ''.join(random.choice("01") for i in range(16))
            fh.write(f"    parameter \LUT 16'{lut_string}\n")
            fh.write(f"    parameter \WIDTH 4\n")
            fh.write(f"    connect \\A {{")
            for lut_input_idx in range(NUM_LUT_INPUTS):
                fh.write(f" \\fpga_in_{shuffled_input_indexes[lut_input_idx]}")
                # \\fpga_in_{lut_input_idx[1]} \\fpga_in_{lut_input_idx[2]} \\fpga_in_{lut_input_idx[3]}}}")
            fh.write(f" }}\n")
            fh.write(f"    connect \Y \\fpga_out_{lut_idx}\n")
            fh.write(f"  end\n")

        fh.write(f"end\n")

        fh.close()