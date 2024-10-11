from typing import Callable

import pandas as pd
import glob
import pandas
from pandas import DataFrame

# Global var - do we need case sensitive comparisons ?
case_sensitive = True


def validate_xl_file_columns(xl_file_path, expected_col_list):
    """
    Validate that the XL file has the required columns
    :param xl_file_path: path to excel file
    :param expected_col_list: the mandatory list of columns in the XL file
    :return: list of missing columns
    """
    df = pd.read_excel(io=xl_file_path)
    missing_expected_cols = []
    column_names_of_df = df.columns.values.tolist()
    for col in expected_col_list:
        if col not in column_names_of_df:
            missing_expected_cols.append(col)
    return missing_expected_cols


def validate_xl_folder(xl_folder_path, expected_col_list):
    """
    Validate that every file in the XL folder path has valid column list
    :param xl_folder_path:
    :param expected_col_list:
    :return: a list of tuples where first name is filename and second name is list of missing columns
    """
    xlfiles = get_xl_file_list_from_folder(xl_folder_path)
    output_tuple_list = []
    for xlfile in xlfiles:
        missing_expected_cols = validate_xl_file_columns(xlfile, expected_col_list)
        if len(missing_expected_cols) != 0:
            output_tuple_list.append((xlfile, missing_expected_cols))


def get_xl_file_list_from_folder(xl_folder_path):
    """
    Returns list of xl file paths under a folder
    """
    return glob.glob(str(xl_folder_path) + '/*.xlsx')


def read_column_from_xl_sheet(xl_file_name, xl_sheet_name, column_name):
    """ Read an excel sheet into a dataframe with column as input => set"""
    if xl_sheet_name == None:
        df = pd.read_excel(io=xl_file_name)
    else:
        df = pd.read_excel(io=xl_file_name, sheet_name=xl_sheet_name)

    column_names_of_df = df.columns.values.tolist()
    if column_name not in column_names_of_df:
        raise KeyError(f'column {column_name} not found in list of column names {column_names_of_df}')
    column_values_list = df[column_name].values.tolist()
    # Return set since we don't want duplicates
    clean_set = set()
    for val in column_values_list:
        if pd.notnull(val):
            valstr = str(val) if case_sensitive else str(val).casefold()
            clean_set.add(valstr)
    return clean_set


def read_columns_from_xl_sheet(xl_file_name, xl_sheet_name, column_names_list):
    """

    :param xl_file_name:
    :param xl_sheet_name:
    :param column_names_list:
    :return: dataframe object with only the expected columns
    """
    if xl_sheet_name == None:
        df = pd.read_excel(io=xl_file_name, names=column_names_list)
    else:
        df = pd.read_excel(io=xl_file_name, sheet_name=xl_sheet_name, names=column_names_list)
    return df


def transform(str1):
    list1 = str1.split(".")
    if len(list1) != 3:
        raise Exception(f"{str1} doesn't conform to format")
    return list1[2]


def read_all_excel_sheets(xl_file_name, col_name):
    """
    Reads XL file with multiple sheets and returns a dict of sheet name to set
    :param xl_file_name:
    :return:
    """
    dict = pd.read_excel(io=xl_file_name, sheet_name=None)
    dict_sheetname_to_set = {}
    for sheet_name in dict:
        df = dict[sheet_name]
        value_set = set(df[col_name].values.tolist())
        dict_sheetname_to_set[sheet_name] = value_set
    return dict_sheetname_to_set


def read_all_excel_sheets_data_into_set(xl_file_name, col_name):
    """
    Reads XL file with multiple sheets and returns a set of all transformed values
    :param xl_file_name:
    :return:
    """
    dict = pd.read_excel(io=xl_file_name, sheet_name=None)
    final_set = set()
    set_not_init = True
    for sheet_name in dict:
        df = dict[sheet_name]
        listvals = map(transform, df[col_name].values.tolist())
        value_set = set(listvals)
        if set_not_init is True:
            final_set = value_set.copy()
            set_not_init = False
        else:
            final_set = final_set.intersection(value_set)

    return final_set


def validate_df_schema(df, expected_cols_list):
    """
    validate that DF has expected columns
    :param df:
    :param expected_cols_list:
    :return:
    """
    col_list = df.columns.values.tolist()
    diffset = set(col_list).difference(set(expected_cols_list))
    if len(diffset) > 0:
        raise KeyError(f'columns {diffset} not found in list of column names of df')


def concat_dfs(dfs_list, expected_cols_list):
    """

    :param dfs_list:
    :return:
    """
    result_df = pd.DataFrame(columns=expected_cols_list)
    for inputdf in dfs_list:
        validate_df_schema(inputdf, expected_cols_list)
    return pd.concat(dfs_list)


def create_consolidated_df(folder_path, expected_col_names):
    """
    Read the column values from all XL files of the folder
    and concat them into a single df
    :param folder_path:
    :return: concatenated set of all col values
    """
    xl_files = get_xl_file_list_from_folder(folder_path)
    dflist = []
    for xl_file in xl_files:
        currentdf = read_columns_from_xl_sheet(xl_file, None, expected_col_names)
        dflist.append(currentdf)

    # concat
    final_df = concat_dfs(dflist, expected_col_names)
    return final_df


def create_consolidated_column_values_set(folder_path, col_name):
    """
    Read the column values from all XL files of the folder
    and concat them into a single set
    :param folder_path:
    :return: concatenated set of all col values
    """
    xl_files = get_xl_file_list_from_folder(folder_path)
    final_values = set()
    for xl_file in xl_files:
        curr_col_value_set = read_column_from_xl_sheet(xl_file, None, col_name)
        final_values = final_values | curr_col_value_set
    return final_values


def create_subset_df_from_keyset(column_name: str, keyset: set, source_df: DataFrame) -> DataFrame:
    """
    Given a value of keys of a particular column, select only those rows from source df
    :param column_name
    :param keyset: list of values of the column_name that need to be matched against
    :param source_df:
    :return:
    """
    # Create a new result dataframe empty
    result_df: DataFrame = pd.DataFrame()
    for index, row in source_df.iterrows():
        row_val = str(row[column_name]).casefold()
        if row_val in keyset:
            # append series to result df
            new_row = row.to_frame().T  # remember we need to take transpose
            result_df = pd.concat([result_df, new_row], ignore_index=True)
    return result_df


# TODO Rewrite this to have an optional map/equality function param
def get_sanitized_column_values_set(df: DataFrame, column_name: str) -> set:
    """
    Given a column name and a dataframe, return the set of unique column values that are not null
    :param df: dataframe
    :param column_name: name of the column
    :return: set of column values
    """
    column_values_list: list = df[column_name].values.tolist()
    # Return set since we don't want duplicates
    clean_set = set()
    for val in column_values_list:
        if pd.notnull(val):
            clean_set.add(str(val).casefold())
    return clean_set


def get_sanitized_column_values_set_mapped(df: DataFrame, column_name: str, map_func: Callable[[str], str]) -> set:
    """
    Given a column name, map func and a dataframe, return the set of unique column values
    that are not null
    :param df: dataframe
    :param column_name: name of the column
    :param map_func: column values are mapped before inserting them into set. A callable that takes a str
    as input and returns a str as output
    :return: set of column values
    """
    column_values_list: list = df[column_name].values.tolist()
    # Return set since we don't want duplicates
    clean_set = set()
    for val in column_values_list:
        if pd.notnull(val):
            clean_set.add(map_func(str(val).casefold()))
    return clean_set


def remove_duplicates(source_df: DataFrame, key_column: str, value_map_fn: Callable[[str], str]) -> DataFrame:
    """
    Given a dataframe and a key column (which should not have duplicates), dedup the dataframe.
    Also provided is a value_map_fn that is run on values before
    :param source_df: source dataframe with duplicate values in key_column
    :param key_column: name of the column that has duplicated
    :param value_map_fn: mapping function on the values before doing equality comparison. A callable that takes a str
    as input and returns a str as output
    :return: output dataframe with deduped values in key column
    """
    unique_key_set: set = get_sanitized_column_values_set_mapped(source_df, key_column, value_map_fn)
    deduped_df: DataFrame = create_subset_df_from_keyset(key_column, unique_key_set, source_df)
    return deduped_df
