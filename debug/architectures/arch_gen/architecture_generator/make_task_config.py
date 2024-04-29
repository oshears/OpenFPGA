# write task.conf

def write_task_config(outdir, design_dir, NUM_DESIGNS=20000, device_size="2x2", device_arch="k4_N4_40nm_cc_openfpga.xml", route_chan_width=40):
    # NUM_DESIGNS=20000

    fh = open(f"{outdir}/task.conf","w+")


    fh.write(f"[GENERAL]\n")
    fh.write(f"run_engine=openfpga_shell\n")
    fh.write(f"power_tech_file = ${{PATH:OPENFPGA_PATH}}/openfpga_flow/tech/PTM_45nm/45nm.xml\n")
    fh.write(f"power_analysis = true\n")
    fh.write(f"spice_output=false\n")
    fh.write(f"verilog_output=true\n")
    fh.write(f"timeout_each_job = 20*60\n")
    fh.write(f"fpga_flow=yosys_vpr\n")
    fh.write(f"\n")

    fh.write(f"[OpenFPGA_SHELL]\n")
    fh.write(f"openfpga_shell_template=${{PATH:OPENFPGA_PATH}}/openfpga_flow/openfpga_shell_scripts/write_full_testbench_example_script_1.openfpga\n")
    fh.write(f"openfpga_arch_file=${{PATH:OPENFPGA_PATH}}/openfpga_flow/openfpga_arch/{device_arch}\n")
    fh.write(f"openfpga_sim_setting_file=${{PATH:OPENFPGA_PATH}}/openfpga_flow/openfpga_simulation_settings/auto_sim_openfpga.xml\n")
    fh.write(f"openfpga_vpr_device_layout=--device {device_size} --route_chan_width {route_chan_width}\n")
    fh.write(f"openfpga_fast_configuration=\n")
    fh.write(f"\n")

    fh.write(f"[ARCHITECTURES]\n")
    fh.write(f"arch0=${{PATH:OPENFPGA_PATH}}/openfpga_flow/vpr_arch/k4_N4_tileable_40nm_new.xml\n")
    fh.write(f"\n")

    fh.write(f"[BENCHMARKS]\n")
    for i in range(NUM_DESIGNS):
        design_num = f"{(i+1)}".zfill(5)
        fh.write(f"bench{i}=${{PATH:OPENFPGA_PATH}}/{design_dir}/{design_num}/design.il\n")
    fh.write(f"\n")

    fh.write(f"[SYNTHESIS_PARAM]\n")
    fh.write(f"bench_read_verilog_options_common = -nolatches\n")
    fh.write(f"bench_yosys_common=${{PATH:OPENFPGA_PATH}}/openfpga_flow/misc/ys_tmpl_yosys_vpr_flow_2.ys\n")
    fh.write(f"\n")

    for i in range(NUM_DESIGNS):
        design_num = f"{(i+1)}".zfill(4)
        fh.write(f"bench{i}_top=fpga_design\n")
        fh.write(f"bench{i}_chan_width={route_chan_width}\n")
    fh.write(f"\n")

    fh.write(f"[SCRIPT_PARAM_MIN_ROUTE_CHAN_WIDTH]\n")
    fh.write(f"end_flow_with_test=\n")


    fh.close()