import glob
from typing import List
import xml
import xml.etree
# import xml.etree.ElementTree
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
import time

def get_config_distributions(bit_reference:str, bitstreams_path:str, out_file_path:str = "config_distributions.csv"):
    '''
    Record the configuration bit distribtuions for each of the configuration / routing muxes 
    '''
    
    bitstreams = glob.glob(bitstreams_path + "/*.bit")
    
    # number of bits in bitstream
    BITSTREAM_LENGTH = 1702
    NUM_CONFIGS = 20000
    
    # setup config_tracker
    print("Setting up Configuration Distribution Dictionary")
    startTime = time.time()
    config_tracker = {}
    
    bit_index_config_elem_mapping = []
    modules = []

    with open(bit_reference) as bit_reference_csv_fh:
        bit_reference_reader = csv.DictReader(bit_reference_csv_fh)
        
        curr_config_elem = None
        num_bits_for_config_elem = 0
        bit_index = 0
        
        for row in bit_reference_reader:
            
            config_elem = row['path'].replace("/",".") #f"{row['module']}.{row['name']}"
            bit_index_config_elem_mapping.append(config_elem)
            
            if row['module'] not in modules:
                modules.append(row['module'])
            
            if curr_config_elem == None:
                curr_config_elem = config_elem # f"{row['module']}.{row['name']}"
                config_tracker[curr_config_elem] = {"configs" : [], 'name':row['name'], 'type':row['type'], 'module':row['module'], 'path':row['path'], 'description':row['description']}
                num_bits_for_config_elem = 1
            else:
                
                ## if current bit belongs to previous config element
                if curr_config_elem == config_elem: #f"{row['module']}.{row['name']}":
                    num_bits_for_config_elem += 1
                    
                else:
                    
                    # populate all possible configs for previous config element
                    for i in range(2**num_bits_for_config_elem):
                        config_string = bin(i)[2:].zfill(num_bits_for_config_elem)
                        config_tracker[curr_config_elem]['configs'].append({"bits":config_string, "count" : 0, "percentage":0})
                    
                    # setup new config element
                    curr_config_elem = config_elem # f"{row['module']}.{row['name']}"
                    config_tracker[curr_config_elem] = {"configs" : [], 'name':row['name'], 'type':row['type'], 'module':row['module'], 'path':row['path'], 'description':row['description']}
                    num_bits_for_config_elem = 1
                    
                    
                if bit_index == BITSTREAM_LENGTH - 1:
                    # populate all possible configs
                    for i in range(num_bits_for_config_elem**2):
                        config_string = bin(i)[2:].zfill(num_bits_for_config_elem)
                        config_tracker[curr_config_elem]['configs'].append({"bits:":config_string, "count" : 0, "percentage":0})
                    
            
            bit_index += 1
        
    
    print(f"Done setting up the dictionary in {time.time() - startTime}s")
    
    print("Parsing bitstream data")
    startTime = time.time()

    # parse configs from bitstreams
    total_bitstreams = len(bitstreams)
    bitstream_index = 0
    for bitstream in bitstreams:
        
        bitstream_index += 1
        if bitstream_index % (total_bitstreams // 10) == 0:
            print(f"\t{bitstream_index * 100 // total_bitstreams}%\t({bitstream_index} / {total_bitstreams})")
        
        HEADER_OFFSET = 5
        with open(bitstream, "r+") as bitstream_fh:
            bitstream_lines = bitstream_fh.readlines()
            
            curr_config_bits = ""
            prev_config_elem = None
            
            for bit_index in range(len(bitstream_lines) - HEADER_OFFSET):
                curr_config_elem = bit_index_config_elem_mapping[bit_index]
                
                if prev_config_elem == None:
                    prev_config_elem = curr_config_elem
                    curr_config_bits = bitstream_lines[HEADER_OFFSET + bit_index].strip()
                    
                else:
                    
                    if curr_config_elem == prev_config_elem:
                        curr_config_bits += bitstream_lines[HEADER_OFFSET + bit_index].strip()
                        
                    else:
                        config_tracker[prev_config_elem]['configs'][int(curr_config_bits,2)]["count"] += 1
                        
                        if config_tracker[prev_config_elem]['configs'][int(curr_config_bits,2)]["count"] > 20000:
                            raise Exception("too many configs!")
                        
                        prev_config_elem = curr_config_elem
                        curr_config_bits = bitstream_lines[HEADER_OFFSET + bit_index].strip()
                        
    # caculate distribution percentages
    for config_elem in config_tracker.keys():
        for config in config_tracker[config_elem]['configs']:
            config['percentage'] = (100 * config['count']) / NUM_CONFIGS       
            
    print(f"Done collecting bitstream data in: {time.time() - startTime}s")
    
    # https://docs.python.org/3/library/pickle.html
    # Export Dictionary to PKL file
    
    print("Writing JSON Files")   
    startTime = time.time()
    write_json_files(config_tracker, out_file_path)
    print(f"Done writing json files in: {time.time() - startTime}s")
    
    print("Writing Module JSON Files")   
    startTime = time.time()
    write_module_json_files(config_tracker, modules, out_file_path)
    print(f"Done writing module json files in: {time.time() - startTime}s")
    
    print("Writing Visualizations")
    startTime = time.time()
    write_visualizations(config_tracker, out_file_path)
    print(f"Done writing visualizations in: {time.time() - startTime}s")
        
    

def write_json_files(config_distributions:str, out_file_path:str):
    
    # write json
    total_config_elems = len(config_distributions.keys())
    current_config_elem_index = 0
    
    for config_element in config_distributions.keys():
        
        current_config_elem_index += 1
        if current_config_elem_index % (total_config_elems//10) == 0:
            print(f"\t{current_config_elem_index * 100 // total_config_elems}%\t({current_config_elem_index} / {total_config_elems})")
            
        # output_json_string = json.encoder.JSONEncoder().encode(config_distributions[config_element])
        with open(f"{out_file_path}/{config_element}.json","w+") as out_file:
            json.dump(config_distributions[config_element], out_file, ensure_ascii=False, indent=4)

def write_module_json_files(config_distributions:str, modules:List[str], out_file_path:str):
    # write json
    total_config_elems = len(modules)
    current_config_elem_index = 0
    
    for module in modules:
        
        current_config_elem_index += 1
        if current_config_elem_index % (total_config_elems//10) == 0:
            print(f"\t{current_config_elem_index * 100 / total_config_elems}%\t({current_config_elem_index} / {total_config_elems})")
        
        module_config_elements = {}
        with open(f"{out_file_path}/modules/{module}.json", "w+") as out_file:
            
            for config_element in config_distributions.keys():
                if module in config_element:
                    module_config_elements[config_element] = config_distributions[config_element]
                    # output_json_string = json.encoder.JSONEncoder().encode(config_distributions[config_element])
            
            json.dump(module_config_elements, out_file, ensure_ascii=False, indent=4)
    

def write_visualizations(config_distributions:str, out_file_path:str):
    
    total_config_elems = len(config_distributions.keys())
    current_config_elem_index = 0
    
    for config_element in config_distributions.keys():
        
        current_config_elem_index += 1
        if current_config_elem_index % (total_config_elems/20) == 0:
            print(f"\t{current_config_elem_index * 100 // total_config_elems}%\t({current_config_elem_index} / {total_config_elems})")
        
        configurations = []
        counts = []
        
        for config in config_distributions[config_element]['configs']:
            configurations.append(config['bits'])
            counts.append(config['count'])
        
        fig = plt.figure(figsize=(10,5))
        
        plt.bar(configurations,counts,width=0.4)
        
        plt.xlabel("Configuratons")
        plt.ylabel("Number of Times Configured")
        plt.title(f"Distribution of Configurations for {config_element}")
        plt.ylim((0,20000))
        plt.savefig(f"{out_file_path}/{config_element}.png")
        
        plt.close()