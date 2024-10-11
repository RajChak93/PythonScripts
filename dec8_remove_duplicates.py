import pandas as pd
from pandas import DataFrame
from typing import Callable

from excel_reading_utils import create_subset_df_from_keyset, \
    get_sanitized_column_values_set_mapped, remove_duplicates


def transcription_mapping(trans: str) -> str:
    """
    Mapping function that treats gene1-gene2 and gene2-gene1 the same way
    :param trans: transcription of the form gene1-gene2
    :return: Sorted(trans)
    """
    sorted_trans_list = sorted(trans.split('-'))
    assert (len(sorted_trans_list) == 2), f'transcription <{trans}> incorrect format'
    return '-'.join(sorted_trans_list)


def transcription_data_errors_validator(df: DataFrame, tag: str):
    """
    In the dataframe check what transcription have more than 2 dashes (-)
    """
    print(f'-----------{tag}-------------')
    column_values_list: list = df['transcription'].values.tolist()
    error_values_dict = {}
    for val in column_values_list:
        constituents = val.split('-')
        if len(constituents) != 2:
            if val in error_values_dict.keys():
                error_values_dict[val] = error_values_dict[val] + 1
            else:
                error_values_dict[val] = 1
    print(error_values_dict)


def runner(source_file: str, output_file: str, tag: str) -> None:
    """
    Main runner of business logic. Takes the source and output file locations. Does the following-
    1. Reads source file to dataframe
    2. Deduped source dataframe on key column (needs a mapping function as well to eliminate duplicates)
    3. Writes deduped df to output files
    4. Prints metrics for observability
    :param source_file
    :param output_file
    :param tag
    :return: void method
    """
    source_df: DataFrame = pd.read_excel(io=source_file)
    deduped_df: DataFrame = remove_duplicates(source_df, 'transcription', transcription_mapping)
    # write result DFs to excel sheet
    deduped_df.to_excel(output_file)
    print(f'rows in {tag} output DF = {len(deduped_df)}')
    return None


if __name__ == '__main__':
    # -------GC-GT---------
    runner('resources/2023_Dec8/GC_minus_GT.xlsx', 'resources/2023_Dec8/deduped_GC_minus_GT.xlsx', 'GC-GT')

    # -------GT-GC---------
    runner('resources/2023_Dec8/GT_minus_GC.xlsx', 'resources/2023_Dec8/deduped_GT_minus_GC.xlsx', 'GT-GC')

    # -------NC-NT---------
    runner('resources/2023_Dec8/NC_minus_NT.xlsx', 'resources/2023_Dec8/deduped_NC_minus_NT.xlsx', 'NC-NT')

    # -------NT-NC---------
    runner('resources/2023_Dec8/NT_minus_NC.xlsx', 'resources/2023_Dec8/deduped_NT_minus_NC.xlsx', 'NT-NC')

    # -------GT-NT---------
    runner('resources/2023_Dec8/GT_minus_NT.xlsx', 'resources/2023_Dec8/deduped_GT_minus_NT.xlsx', 'GT-NT')

    # -------NT-GT---------
    runner('resources/2023_Dec8/NT_minus_GT.xlsx', 'resources/2023_Dec8/deduped_NT_minus_GT.xlsx', 'NT-GT')

    # -------GC-NC---------
    runner('resources/2023_Dec8/GC_minus_NC.xlsx', 'resources/2023_Dec8/deduped_GC_minus_NC.xlsx', 'GC-NC')

    # -------NC-GC---------
    runner('resources/2023_Dec8/NC_minus_GC.xlsx', 'resources/2023_Dec8/deduped_NC_minus_GC.xlsx', 'NC-GC')
