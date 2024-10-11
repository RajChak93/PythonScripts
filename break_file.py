FOLDER_PATH = 'resources/2024_feb_15/'


def chunk_list(list, size):
    return [list[i:i + size] for i in range(0, len(list), size)]


def break_file(input_filename, limit):
    input_filepath = FOLDER_PATH + input_filename
    with open(input_filepath, 'r') as file:
        list_of_chunks = chunk_list(file.readlines(), limit)
    i = 0
    for chunk in list_of_chunks:
        output_filename = str(i) + '_' + input_filename
        output_filepath = FOLDER_PATH + 'results/' + output_filename
        print(f'{output_filename} has {len(chunk)} rows')
        chunk_to_str = '\n'.join(chunk)
        # Write to output path
        with open(output_filepath, 'wt') as f:
            print(chunk_to_str, file=f)
        i = i + 1


# main call
break_file('GT_ZNF610_MA1713.csv_unique_elements_t_minus_c.txt', 5000)
