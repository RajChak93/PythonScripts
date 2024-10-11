import glob
import pandas as pd
import argparse


def transform_bed_to_set(path_to_bed: str) -> set:
    obj_set = set()
    df = pd.read_csv(path_to_bed, sep='\t', header=None)
    df_projection = df.iloc[:, 0:3]
    for i in range(len(df_projection)):
        string_rep = str(df.iloc[i, 0]) + ',' + str(df.iloc[i, 1]) + ',' + str(df.iloc[i, 2])
        obj_set.add(string_rep)
    return obj_set


def get_bed_filenames_under_folder(folder_path):
    """
    Returns the name of the gc and get bed files under folder structure
    """
    paths_matching_gc = glob.glob(str(folder_path) + '/*_GC_all_bound.bed')
    if len(paths_matching_gc) != 1:
        raise FileNotFoundError(f'folder_path={folder_path}, gc paths matching = {paths_matching_gc}')
    paths_matching_gt = glob.glob(str(folder_path) + '/*_GT_all_bound.bed')
    if len(paths_matching_gt) != 1:
        raise FileNotFoundError(f'folder_path={folder_path}, gt paths matching = {paths_matching_gt}')
    return paths_matching_gc[0], paths_matching_gt[0]


def print_set_to_file(filepath: str, objset: set):
    output_str = ''
    for element in objset:
        output_str = output_str + str(element) + '\n'
    with open(filepath, 'wt') as f:
        print(output_str, file=f)


def does_output_file_exist(filepath):
    """
    Returns true if output file already exists
    """
    paths_matching = glob.glob(str(filepath))
    if len(paths_matching) > 0:
        return True
    else:
        return False


# Parse cmd line argument
parser = argparse.ArgumentParser(description='Root folder path that has the gc/gt files under /bed/')
# Note path should not end with /, eg
# "python3 unique_elements_in_bed_files.py -f /Users/ssen/PycharmProjects/PythonLearning/resources/2024_jan14"
parser.add_argument('-f', '--folder_path', dest='folder_path', action='store', required=True)
args = parser.parse_args()

# business logic
FOLDER_PATH = args.folder_path
# output_txt_path = FOLDER_PATH + '/unique_elements.txt'
output_gc_minus_gt_path = FOLDER_PATH + '/unique_elements_gc_minus_gt.txt'
output_gt_minus_gc_path = FOLDER_PATH + '/unique_elements_gt_minus_gc.txt'
if does_output_file_exist(output_gc_minus_gt_path) and does_output_file_exist(output_gt_minus_gc_path):
    print('Files already created, exiting!')
    exit()
gc_file_path, gt_file_path = get_bed_filenames_under_folder(FOLDER_PATH)
set_gc = transform_bed_to_set(gc_file_path)
set_gt = transform_bed_to_set(gt_file_path)
# unique_elements = set_gc.intersection(set_gt)
unique_elements_gc_minus_gt = set_gc.difference(set_gt)
unique_elements_gt_minus_gc = set_gt.difference(set_gc)
print(
    f'Folder {FOLDER_PATH} : set_gc has {len(set_gc)} elements, set_gt has {len(set_gt)} elements, unique_elements_gc_minus_gt has {len(unique_elements_gc_minus_gt)} elements, unique_elements_gt_minus_gc has {len(unique_elements_gt_minus_gc)} elements')

# print to file
print_set_to_file(output_gc_minus_gt_path, unique_elements_gc_minus_gt)
print_set_to_file(output_gt_minus_gc_path, unique_elements_gt_minus_gc)
