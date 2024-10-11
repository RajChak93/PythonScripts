import numpy as np
INPUT_FILE = 'resources/2024_Feb_26/bptp_coregroup_50_runtimes.txt'


# Map of gene_target -> [tf,chr,start,end]1, [tf,chr,start,end]2 ... (list)
gene_target_to_list_rest_map = {}

# Iterate over the lines of the file
def validate(line_to_arr):
    assert len(line_to_arr) == 2

buildid_timemins_mapping = {}


def extract_mins(time_str):
    components = time_str.split(" ")
    assert len(components) == 4
    hour = int(components[0])
    min = int(components[2])
    return hour*60+min


with open(INPUT_FILE, 'rt') as f:
    for line in f:
        # process line
        line = line.strip()
        line_to_arr = line.split('\t')
        validate(line_to_arr)
        build_id, time_str = line_to_arr
        time_in_mins = extract_mins(time_str)
        buildid_timemins_mapping[build_id] = time_in_mins

# Compute percentiles
all_runtimes = buildid_timemins_mapping.values()
rerun_runtimes = [runtime for runtime in all_runtimes if runtime>180]
pass_runtimes = [runtime for runtime in all_runtimes if runtime<180]
fail_runtimes = [runtime for runtime in all_runtimes if runtime>=240]

pass_percentage = len(pass_runtimes)/len(all_runtimes) *100
rerun_percentage = len(rerun_runtimes)/len(all_runtimes) *100
fail_percentage = len(fail_runtimes)/len(all_runtimes) *100

pass_p50 = np.percentile(np.array(pass_runtimes),50)
pass_p95 = np.percentile(np.array(pass_runtimes),95)
rerun_p50 = np.percentile(np.array(rerun_runtimes),50)
rerun_p95 = np.percentile(np.array(rerun_runtimes),95)

print(f'Total sample size = {len(all_runtimes)}')
print(f'Pass % {pass_percentage}, rerun % {rerun_percentage}, fail % {fail_percentage}')
print(f'Pass p50 {pass_p50}, pass p95 {pass_p95}')
print(f'Rerun p50 {rerun_p50}, rerun p95 {rerun_p95}')