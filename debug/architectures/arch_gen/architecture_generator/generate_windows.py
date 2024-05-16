def generate_windows(device_width = 42, window_dim=(2,2)):
    windows = []

    horizontal_window_count = (device_width - 2) // 2

    window_count = 0

    for window_x in range(horizontal_window_count):
        for window_y in range(horizontal_window_count):
            print(f"Window #{window_count}")
            window = []

            # clbs
            for clb_x in range(2):
                for clb_y in range(2):
                    x_loc = 2 + window_x * 2 + clb_x 
                    y_loc = 2 + window_y * 2 + clb_y
                    clb = f"grid_clb_{x_loc}__{y_loc}_"
                    window.append(clb)
                    # print(f"\t{clb}")

            # switchboxes
            for sb_x in range(3):
                for sb_y in range(3):
                    x_loc = 1 + window_x * 2 + sb_x 
                    y_loc = 1 + window_y * 2 + sb_y
                    sb = f"sb_{x_loc}__{y_loc}_"
                    window.append(sb)
                    # print(f"\t{sb}")
            
            # cby connection blocks
            for cby_x in range(3):
                for cby_y in range(2):
                    x_loc = 1 + window_x * 2 + cby_x 
                    y_loc = 2 + window_y * 2 + cby_y
                    cby = f"cby_{x_loc}__{y_loc}_"
                    window.append(cby)
                    # print(f"\t{cby}")
            
            # cbx connection blocks
            for cbx_x in range(2):
                for cbx_y in range(3):
                    x_loc = 2 + window_x * 2 + cbx_x 
                    y_loc = 1 + window_y * 2 + cbx_y
                    cbx = f"cbx_{x_loc}__{y_loc}_"
                    window.append(cbx)
                    # print(f"\t{cbx}")

            windows.append(window)

            window_count += 1

    return windows