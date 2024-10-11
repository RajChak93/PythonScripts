import excel_reading_utils

# Folder names with 55 excel files
folder_names = ['resources/July21/GT/', 'resources/July21/NC/', 'resources/July21/NT/', 'resources/July21/GC/']
# these columns are to be extracted
column_to_be_read_list = ['site1_chrom', 'site1_name', 'site2_chrom', 'site2_name', 'gene_id', 'gene_type']


def check_55_files():
    """
    Assert that there are 55 files in total in all 4 folders
    :return: Prints output, non functional side effects layer
    """
    for folder_name in folder_names:
        cnt = len(excel_reading_utils.get_xl_file_list_from_folder(folder_name))
        print(f'{folder_name} has {cnt} excel files')


def validate_xl_folders():
    """
    Valdiates that each file has those columns that we intend to copy
    :return: Prints output, non functional side effects layer
    """
    for folder_name in folder_names:
        error_tuple_list = excel_reading_utils.validate_xl_folder(folder_name, column_to_be_read_list)
        print(f'{folder_name} output is {error_tuple_list}')


def test_consolidate_column_values():
    """
    Test function to test behavior of create_consolidated_column_values_set()
    :return: ONLY manual debugging
    """
    ans = excel_reading_utils.create_consolidated_column_values_set(folder_names[0], column_to_be_read_list[0])


def test_consolidated_df():
    """

    :return:
    """
    ans = excel_reading_utils.create_consolidated_df(folder_names[0], column_to_be_read_list)


def run_single_column():
    for folder_name in folder_names:
        for colname in column_to_be_read_list:
            consolidated_set_of_col_values = excel_reading_utils.create_consolidated_column_values_set(folder_name,
                                                                                                       colname)
            # write back to file names {colname}.txt in {folder_name}
            # NOTE : Assumes file already exists
            col_values_string = '\n'.join(consolidated_set_of_col_values)
            with open(folder_name + '/' + colname + '.txt', 'wt') as f:  # write after overwriting
                f.write(col_values_string)


def run():
    for folder_name in folder_names:
        for colname in column_to_be_read_list:
            consolidated_set_of_col_values = excel_reading_utils.create_consolidated_column_values_set(folder_name,
                                                                                                       colname)
            # write back to file names {colname}.txt in {folder_name}
            # NOTE : Assumes file already exists
            col_values_string = '\n'.join(consolidated_set_of_col_values)
            with open(folder_name + '/' + colname + '.txt', 'wt') as f:  # write after overwriting
                f.write(col_values_string)


if __name__ == '__main__':
    # check_55_files() -> PASSED
    # validate_xl_folders() -> passed
    # test_consolidate_column_values() -> passed
    test_consolidated_df()
