import random
import os
import shutil

def make_std_il_designs(design_dir, NUM_DESIGNS=20000, NUM_LUTS = 16):
    # design_dir = f"./debug/architectures/arch_gen/results/{outdir}"

    # shutil.rmtree(design_dir)
    # os.mkdir(design_dir)

    class Wire:
        def __init__(self,name,lut,idx,dir):
            self.name = name
            self.lut = lut
            self.idx = idx
            self.dir = dir

    for i in range(NUM_DESIGNS):

        index = i
        index_str = f"{(index + 1)}".zfill(5)
        
        os.mkdir(f"{design_dir}/{index_str}")
        fh = open(f"{design_dir}/{index_str}/design.il","w+")
        # fh = open(f"{design_dir}/{index_str}/design.v","w+")

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

def make_tiered_il_designs(design_dir, NUM_DESIGNS=20000, NUM_LUTS = 16):
    
    for i in range(NUM_DESIGNS):
        index = i
        index_str = f"{(index + 1)}".zfill(5)
        os.mkdir(f"{design_dir}/{index_str}")
        make_tiered_il_design(f"{design_dir}/{index_str}", NUM_LUTS)

def make_tiered_il_design(design_dir, NUM_LUTS):
        
        fh = open(f"{design_dir}/design.il","w+")

        NUM_LUT_INPUTS = 4
        NUM_INPUTS = 4



        # fh.write(f"# design #: {index_str}\n")
        fh.write(f"# num luts #: {NUM_LUTS}\n")
        fh.write(f"autoidx 140\n")
        fh.write(f"attribute \\top 1\n")
        fh.write(f"module \\fpga_design\n")

        luts_remaining = NUM_LUTS
        tier_outputs = [[f"fpga_in_{i}" for i in range(NUM_INPUTS)]]
        lut_count = 0
        while luts_remaining > 0:
            curr_tier = []
            luts_in_tier = random.randint(min(4,luts_remaining), luts_remaining)
            luts_remaining -= luts_in_tier
            for lut_idx in range(luts_in_tier):
                curr_tier.append(f"lut_out_{lut_count}")
                lut_count += 1
            tier_outputs.append(curr_tier)

        for lut_input_idx in range(NUM_INPUTS):
            fh.write(f"  wire input {lut_input_idx} \\fpga_in_{lut_input_idx}\n")
        
        lut_count = 0

        for lut_idx in range(NUM_LUTS - len(tier_outputs[-1])):
            fh.write(f"  wire \\lut_out_{lut_idx}\n")
            lut_count += 1

        for lut_idx in range(len(tier_outputs[-1])):
            fh.write(f"  wire output {NUM_INPUTS + lut_idx} \\lut_out_{lut_count}\n")
            lut_count += 1

        # prev_tier = list(range(4))
        # prev_tier_outputs = [f"fpga_in_{i}" for i in range(NUM_INPUTS)]
        # next_tier_outputs = []
        lut_count = 0

        for curr_tier_index in range(1,len(tier_outputs)):
            
            # OYS: Need at least 4 luts in the previous tier to provide at least 4 inputs to the next tier luts
            # luts_in_tier = random.randint(min(4,luts_remaining), luts_remaining)
            # luts_remaining -= luts_in_tier
            # print(luts_in_tier)
            luts_in_tier = len(tier_outputs[curr_tier_index])

            # randomize connections between LUTs with wires
            for lut_idx in range(luts_in_tier):

                ## randomly assign lut inputs
                # shuffled_input_indexes = list(range(len(prev_tier_outputs)))
                # random.shuffle(shuffled_input_indexes)
                prev_tier_inputs = tier_outputs[curr_tier_index - 1]
                random.shuffle(prev_tier_inputs)

                curr_lut_output = tier_outputs[curr_tier_index][lut_idx]
                # for lut_input_idx in range(NUM_LUT_INPUTS):

                ## instantiate LUT
                # fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${964 + lut_idx}\n")
                # fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${lut_idx}\n")
                fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${lut_count}\n")
                lut_string = ''.join(random.choice("01") for i in range(16))
                fh.write(f"    parameter \LUT 16'{lut_string}\n")
                fh.write(f"    parameter \WIDTH 4\n")
                fh.write(f"    connect \\A {{")

                for lut_input_idx in range(NUM_LUT_INPUTS):
                    fh.write(f" \\{prev_tier_inputs[lut_input_idx]}")
                    # \\fpga_in_{lut_input_idx[1]} \\fpga_in_{lut_input_idx[2]} \\fpga_in_{lut_input_idx[3]}}}")
                
                fh.write(f" }}\n")
                fh.write(f"    connect \Y \\{curr_lut_output}\n")
                fh.write(f"  end\n")

                # next_tier_outputs.append(f"fpga_out_{lut_idx}")

                lut_count += 1
            
            # prev_tier_outputs = next_tier_outputs

        fh.write(f"end\n")

        fh.close()

# make_tiered_il_design("debug/architectures/arch_gen/results/fpga_4x4_clb/designs/00001", 64)