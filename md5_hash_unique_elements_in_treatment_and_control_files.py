import glob
import math
import hashlib
import pandas as pd
import pickle


def generate_dict_from_df(df):
    '''
    Given a dataframe with schema chrom, start, end
    Create a dict of md5_hash of tuple(chrom,start,end) -> str(chrom,start,end)
    :param df: dataframe
    :return: dict
    '''
    md5_dict = dict()
    # TODO make it more robust by doing schema adhere check
    for i in range(len(df)):
        # ignore empty rows, so checking if the second element (integer) is nan
        if math.isnan(df.iloc[i, 1]):
            # TODO assert here that rest of the cols are also empty
            continue
        chrom = df.iloc[i, 0]
        start = int(df.iloc[i, 1])
        end = int(df.iloc[i, 2])
        string_rep = str(chrom) + ',' + str(start) + ',' + str(end)
        # Step 1: Create the tuple object
        tuple_obj = (chrom, start, end)
        # Step 2 : serialize the tuple
        serialized_tuple = pickle.dumps(tuple_obj)
        # Step 3: Create md5 hash of the tuple object
        md5_hash = hashlib.md5(serialized_tuple)
        # Step 4: add to dict
        md5_dict[md5_hash] = string_rep
    return md5_dict


def read_two_dicts_from_xl_file(path_to_xl: str):
    """
    XL file has 6 cols - treatment,start,end, control,start,end
    We are reading first 3 cols (treatment) into a dict and the next 3 cols (control) in another dict
    The dict schema looks like md5_hash of tuple(chrom,start,end) -> str(chrom,start,end)
    :param path_to_xl: xl file path
    :return: 2 dicts- treatment and control
    """
    obj_set = set()
    df = pd.read_csv(path_to_xl)
    df_treatment = df.iloc[:, 0:3]
    # df_control = df.iloc[:, 4:7] Piu removed middle space
    df_control = df.iloc[:, 3:6]
    treatment_dict = generate_dict_from_df(df_treatment)
    control_dict = generate_dict_from_df(df_control)
    return treatment_dict, control_dict


def print_dict_to_file(filepath: str, key_set: set, md5_to_readable_dict: dict):
    '''
    Given a dict produced by earlier methods md5_hash -> chrom,start,end, and a set of allowed keys
    Write the valid values (chrom,start,end) to a file
    :param filepath: path to output file
    :param md5_to_readable_dict: dict of md5_hash -> chrom,start,end
    :param key_set: set of keys to be included in output
    :return: no return, with side effects (file write)
    '''
    output_str = ''
    # TODO make it single line using lambda functions (map/reduce)
    for md5_key in key_set:
        assert (md5_key in md5_to_readable_dict.keys())
        readable_str = md5_to_readable_dict[md5_key]
        output_str = output_str + str(readable_str) + '\n'
    with open(filepath, 'wt') as f:
        print(output_str, file=f)


# business logic
FOLDER_PATH = "resources/2024_Mar_28/"
# processing: 1) Open xlsx file using Numbers 2)export to CSV
filenames = ['ELK3_MA0759.csv', 'ETV4_MA0764.csv', 'ETV5_MA0765.csv', 'KLF15_MA1513.csv', 'MGA_MA0801.csv',
             'Nrf1_MA0506.csv', 'OTX2_MA0712.csv', 'ZBTB14_MA1650.csv', 'ZNF135_MA1587.csv', 'ZNF610_MA1713.csv']

for filename in filenames:
    xl_file_path = FOLDER_PATH + filename
    output_c_minus_t_path = FOLDER_PATH + 'results/' + filename + '_unique_elements_c_minus_t.txt'
    output_t_minus_c_path = FOLDER_PATH + 'results/' + filename + '_unique_elements_t_minus_c.txt'
    dict_t, dict_c = read_two_dicts_from_xl_file(xl_file_path)
    # Find difference of dicts based on keys
    unique_keys_c_minus_t = set(dict_c.keys()).difference(set(dict_t.keys()))
    unique_keys_t_minus_c = set(dict_t.keys()).difference(set(dict_c.keys()))
    print(f'''
    File {filename} : dict_c has {len(dict_c)} elements, set_t has {len(dict_t)} elements
    unique_elements_c_minus_t has {len(unique_keys_c_minus_t)} elements,
    unique_elements_t_minus_c has {len(unique_keys_t_minus_c)} elements
    ''')
    print_dict_to_file(output_c_minus_t_path, unique_keys_c_minus_t, dict_c)
    print_dict_to_file(output_t_minus_c_path, unique_keys_t_minus_c, dict_t)
