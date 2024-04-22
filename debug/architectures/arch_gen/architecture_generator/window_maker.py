def make_windows(module_info, target_modules):

    bit_count = 0
    for target_module in target_modules:
        print(f"\t{target_module} : {len(module_info[target_module])}")
        bit_count += len(module_info[target_module])
    
    # print(bit_count)