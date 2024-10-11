
INPUT_FILE = 'resources/2024_Mar_11/views.txt'

with open(INPUT_FILE, 'rt') as f:
    for line in f:
        # process line
        view = line.strip()
        print(f'alter view {view} set change_tracking= false;')
        print(f'alter view {view} set change_tracking= true;')