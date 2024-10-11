INPUT_FILE = 'resources/2024_Mar_11/unionall.txt'
OUTPUT_FILE = 'resources/2024_Mar_11/viewdefs.txt'


def print_to_file(arr):
    with open(OUTPUT_FILE, 'wt') as output:
        for output_str in arr:
            output_str = output_str + ';\n\n'
            print(output_str, file=output)

with open(INPUT_FILE, 'rt') as f:
    for line in f:
        # process line
        line = line.strip()
        if line == '':
            continue
        arr = line.split('union all')
        print_to_file(arr)
