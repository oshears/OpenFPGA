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

def make_tiered_il_designs(design_dir, device_width, NUM_DESIGNS=20000, NUM_LUTS = 16):
    
    for i in range(NUM_DESIGNS):
        index = i
        index_str = f"{(index + 1)}".zfill(5)
        os.mkdir(f"{design_dir}/{index_str}")
        make_tiered_il_design(f"{design_dir}/{index_str}", NUM_LUTS, device_width)

def make_tiered_il_design(design_dir, NUM_LUTS, device_width):
        
        fh = open(f"{design_dir}/design.il","w+")

        NUM_LUT_INPUTS = 4
        NUM_INPUTS = 4

        # TODO: need to cap the number of LUTs present at the output to avoid implementation issues
        luts_remaining = NUM_LUTS
        tier_outputs = [[f"fpga_in_{i}" for i in range(NUM_INPUTS)]]
        used_outputs = []
        all_tier_lut_inputs = [[]] # X: Tier, Y: LUT, Z: LUT input
        device_outputs = []
        lut_count = 0
        num_tiers = 0

        # number of gpio pads
        NUM_DEVICE_IO = (device_width * 4) * 8

        NUM_DEVICE_INPUTS = None
        NUM_DEVICE_OUTPUTS = None
        MIN_DEVICE_OUTPUTS = 4
        MAX_DEVICE_OUTPUTS = NUM_DEVICE_IO - 4

        # random.seed(0)
        
        # while there are still LUTs to be placed
        while luts_remaining > 0:

            curr_tier = []

            # pick a random number of LUTs for this tier
            if num_tiers == 0:
                
                # TODO: Make this variable, not just fixed at 4
                # OYS: Maybe this can be a function of the number of LUTs at the last level
                # NUM_DEVICE_INPUTS = NUM_DEVICE_IO - NUM_DEVICE_OUTPUTS
                NUM_DEVICE_INPUTS = 4

                NUM_DEVICE_OUTPUTS = random.randint(MIN_DEVICE_OUTPUTS, min(MAX_DEVICE_OUTPUTS,NUM_LUTS))
                
                luts_in_tier = NUM_DEVICE_OUTPUTS
                
            else:
                # luts_in_tier = random.randint(min(4,luts_remaining), luts_remaining)
                luts_in_next_tier = len(tier_outputs[-1 * num_tiers])
                # concept:
                # - constrain the maximum number of luts to put in this layer
                # - the lower of the number of luts remaining and the number of luts in next layer times 4
                # - two extremes:
                # -   1. every lut has a unique input (luts_in_next_tier * 4)
                # -   2. all luts share the same 4 unique inputs (4 luts in this tier)
                # this technique ensures that all of the previous inputs will sink into the next tier
                # min_num_luts_in_curr_tier = min(luts_remaining, luts_in_next_tier * 4)
                luts_in_tier = min(random.randint(4, luts_in_next_tier*4), luts_remaining)

            # reduce the number of luts remaining
            luts_remaining -= luts_in_tier

            next_tier_inputs = []

            first_tier_inputs = []

            # create an output for each LUT at this tier index in tier_outputs
            for lut_idx in range(luts_in_tier):
                lut_output_name = f"lut_out_{lut_count}"
                curr_tier.append(lut_output_name)
                # if luts_remaining <= 0:
                if num_tiers == 0:
                    device_outputs.append(lut_output_name)
                else:
                    next_tier_inputs.append(lut_output_name)
                
                if luts_remaining == 0:
                    device_inputs = [f"fpga_in_{idx}" for idx in range(NUM_DEVICE_INPUTS)]
                    random.shuffle(device_inputs)
                    for device_input in device_inputs:
                        first_tier_inputs.append(device_input)
                
                lut_count += 1
            # tier_outputs.append(curr_tier)
            tier_outputs.insert(1,curr_tier)
            
            random.shuffle(next_tier_inputs)
            if num_tiers > 0:
                all_tier_lut_inputs.insert(1,next_tier_inputs)

            if len(first_tier_inputs) > 0:
                all_tier_lut_inputs.insert(1,first_tier_inputs)

            # decide which inputs will go to which LUTs
            # tier_lut_inputs = []
            # for lut_idx in range(luts_in_tier):

            #     # get all outputs from the previous tier and shuffle their order
            #     prev_tier_outputs = tier_outputs[num_tiers]
            #     random.shuffle(prev_tier_outputs)

            #     # append the first NUM_LUT_INPUTS tier outputs as inputs to the current LUT
            #     curr_lut_inputs = []
            #     for lut_input_index in range(NUM_LUT_INPUTS):
            #         curr_lut_inputs.append(prev_tier_outputs[lut_input_index])
                
            #     # add the list of current_lut_inputs to the list of tier_lut_inputs
            #     tier_lut_inputs.append(curr_lut_inputs)

            # # add the list all of the LUT input lists to the list of all tier-lut inputs
            # all_tier_lut_inputs.append(tier_lut_inputs)

            # track LUTs that go to outpads

            # for each output from previous tier
            # if num_tiers > 0:
            #     for lut_output_wire in tier_outputs[num_tiers]:
            #         lut_output_has_sink = False

            #         # for each set of LUT inputs in the current tier
            #         for lut_inputs in tier_lut_inputs:
            #             # if the output sinks into one of the current lut_inputs at at the next tier
            #             if lut_output_wire in lut_inputs:
            #                 lut_output_has_sink = True
            #                 break

            #         if not lut_output_has_sink:
            #             device_outputs.append(lut_output_wire)
            
            
            
            num_tiers += 1
        
        fh.write(f"# num luts #: {NUM_LUTS}\n")
        fh.write(f"# LUT TIERS: " + "->".join([str(len(tier_outputs[i])) for i in range(len(tier_outputs))]) + "\n")
        fh.write(f"autoidx 140\n")
        fh.write(f"attribute \\top 1\n")
        fh.write(f"module \\fpga_design\n")

        for lut_input_idx in range(NUM_INPUTS):
            fh.write(f"  wire input {lut_input_idx} \\fpga_in_{lut_input_idx}\n")
        
        io_count = NUM_INPUTS

        for lut_idx in range(NUM_LUTS):
            if f"lut_out_{lut_idx}" in device_outputs:
                fh.write(f"  wire output {io_count} \\lut_out_{lut_idx}\n")
                io_count += 1
            else:
                fh.write(f"  wire \\lut_out_{lut_idx}\n")
                # fh.write(f"  attribute \keep 1\n")

        lut_count = 0

        for curr_tier_index in range(1,len(tier_outputs)):

            tier_input_counter = 0
            
            for lut_idx in range(len(tier_outputs[curr_tier_index])):

                curr_lut_output = tier_outputs[curr_tier_index][lut_idx]

                ## instantiate LUT
                # fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${964 + lut_idx}\n")
                # fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${lut_idx}\n")
                # fh.write(f"  attribute \keep 1\n")
                fh.write(f"  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif${lut_count}\n")
                lut_string = ''.join(random.choice("01") for i in range(16))
                
                # avoid having luts that are programmed as all 1's or all 0's
                if '1' not in lut_string:
                    lut_string = lut_string[:-1] + '1'
                elif '0' not in lut_string:
                    lut_string = lut_string[:-1] + '0'

                fh.write(f"    parameter \LUT 16'{lut_string}\n")
                fh.write(f"    parameter \WIDTH 4\n")
                fh.write(f"    connect \\A {{")
                
                # get the next 4 inputs and shuffle again
                lut_inputs = []
                for lut_input_idx in range(NUM_LUT_INPUTS):
                    lut_inputs.append(all_tier_lut_inputs[curr_tier_index][tier_input_counter])
                    tier_input_counter = (tier_input_counter + 1) % len(all_tier_lut_inputs[curr_tier_index])
                random.shuffle(lut_inputs)
                
                for lut_input_idx in range(NUM_LUT_INPUTS):
                    fh.write(f" \\{lut_inputs[lut_input_idx]}")
                
                fh.write(f" }}\n")
                fh.write(f"    connect \Y \\{curr_lut_output}\n")
                fh.write(f"  end\n")

                lut_count += 1
            
        fh.write(f"end\n")

        fh.close()

# make_tiered_il_design("debug/architectures/arch_gen/results/fpga_4x4_clb/designs/00001", 64)