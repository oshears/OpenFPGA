import glob
import xml
import xml.etree
# import xml.etree.ElementTree
import csv
import json


def get_config_distributions(bit_reference:str, bitstreams_path:str, out_file_path:str = "config_distributions.csv"):
    '''
    Record the configuration bit distribtuions for each of the configuration / routing muxes 
    '''
    
    bitstreams = glob.glob(bitstreams_path + "/*.bit")
    
    # number of bits in bitstream
    BITSTREAM_LENGTH = 1702
    
    # setup config_tracker
    config_tracker = {}
    
    bit_index_config_elem_mapping = []

    with open(bit_reference) as bit_reference_csv_fh:
        bit_reference_reader = csv.DictReader(bit_reference_csv_fh)
        
        curr_config_elem = None
        num_bits_for_config_elem = 0
        bit_index = 0
        
        for row in bit_reference_reader:
            
            config_elem_name = f"{row['module']}.{row['name']}"
            bit_index_config_elem_mapping.append(config_elem_name)
            
            if curr_config_elem == None:
                curr_config_elem = f"{row['module']}.{row['name']}"
                config_tracker[curr_config_elem] = {"configs" : [], 'name':row['name'], 'type':row['type'], 'module':row['module'], 'path':row['path'], 'description':row['description']}
                num_bits_for_config_elem = 1
            else:
                
                ## if current bit belongs to previous config element
                if curr_config_elem == f"{row['module']}.{row['name']}":
                    num_bits_for_config_elem += 1
                    
                else:
                    
                    # populate all possible configs for previous config element
                    for i in range(2**num_bits_for_config_elem):
                        config_string = bin(i)[2:].zfill(num_bits_for_config_elem)
                        config_tracker[curr_config_elem]['configs'].append({"bits":config_string, "count" : 0, "percentage":0})
                    
                    # setup new config element
                    curr_config_elem = f"{row['module']}.{row['name']}"
                    config_tracker[curr_config_elem] = {"configs" : [], 'name':row['name'], 'type':row['type'], 'module':row['module'], 'path':row['path'], 'description':row['description']}
                    num_bits_for_config_elem = 1
                    
                    
                if bit_index == BITSTREAM_LENGTH - 1:
                    # populate all possible configs
                    for i in range(num_bits_for_config_elem**2):
                        config_string = bin(i)[2:].zfill(num_bits_for_config_elem)
                        config_tracker[curr_config_elem]['configs'].append({"bits:":config_string, "count" : 0, "percentage":0})
                    
            
            bit_index += 1
        
        
                

    # parse configs from bitstreams
    for bitstream in bitstreams:
        
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
                        
                        prev_config_elem = curr_config_elem
                        curr_config_bits = bitstream_lines[HEADER_OFFSET + bit_index].strip()
                        
                        
        
    # write json
    for config_element in config_tracker.keys():
        output_json_string = json.encoder.JSONEncoder().encode(config_tracker[config_element])
        out_file_name = config_element.replace('/',".")
        with open(f"{out_file_path}/{out_file_name}.json", "w+") as out_file:
            out_file.write(output_json_string)
        
        
    