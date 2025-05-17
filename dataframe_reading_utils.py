import pandas as pd

def get_sanitized_column_values_set(df, column_name):
    column_values_list = df[column_name].values.tolist()
    # Return set since we don't want duplicates
    clean_set = set()
    for val in column_values_list:
        if pd.notnull(val):
            clean_set.add(str(val).casefold())
    return clean_set

def create_subset_df_from_keyset(column_name, keyset, source_df):
    """
    Given a value of keys of a particular column, select only those rows from source df
    :param column_name
    :param keyset: list of values of the column_name that need to be matched against
    :param source_df:
    :return:
    """
    # Create a new result dataframe empty
    result_df = pd.DataFrame()
    for index, row in source_df.iterrows():
        row_val = str(row[column_name]).casefold()
        if row_val in keyset:
            # append series to result df
            new_row = row.to_frame().T  # remember we need to take transpose
            result_df = pd.concat([result_df, new_row], ignore_index=True)
    return result_df

def run(control_xlsheet_path, treatment_xlsheet_path):
    """
    Main runner of the business logic. Does the following-
    1. Read control and treatment in dataframes
    2. For given key column name, find the column value in control & treatment
    3. Find diff of key column values control - treatment, create a dataframe of the subset
    4. Find diff of key column values treatment - control, create a dataframe of the subset
    :return: tuple containing 2 dataframes c-t and t-c
    """
    df_control = pd.read_excel(io=control_xlsheet_path)
    df_treatment = pd.read_excel(io=treatment_xlsheet_path)
    # compute difference between gc and gt for a particular column
    column_name = 'TF_pairs'
    control_keycolumn_values_set = get_sanitized_column_values_set(df_control, column_name)
    treatment_keycolumn_values_set = get_sanitized_column_values_set(df_treatment, column_name)
    key_columnvals_c_minus_t = control_keycolumn_values_set.difference(treatment_keycolumn_values_set)
    key_columnvals_t_minus_c = treatment_keycolumn_values_set.difference(control_keycolumn_values_set)
    df_c_minus_t = create_subset_df_from_keyset(column_name,key_columnvals_c_minus_t,df_control)
    df_t_minus_c = create_subset_df_from_keyset(column_name, key_columnvals_t_minus_c, df_treatment)
    return (df_c_minus_t, df_t_minus_c)

if __name__ == '__main__':
    # -------GC,GT---------
    df_gc_minus_gt,df_gt_minus_gc = run('resources/Aug8/GC_selected_new.xlsx','resources/Aug8/GT_selected_new.xlsx')
    # write result DFs to excel sheet
    df_gc_minus_gt.to_excel('resources/Aug8/GC_minus_GT.xlsx')
    df_gt_minus_gc.to_excel('resources/Aug8/GT_minus_GC.xlsx')
    #-------NC,NT---------
    df_nc_minus_nt, df_nt_minus_nc = run('resources/Aug8/NC_selected_new.xlsx', 'resources/Aug8/NT_selected_new.xlsx')
    # write result DFs to excel sheet
    df_nc_minus_nt.to_excel('resources/Aug8/NC_minus_NT.xlsx')
    df_nt_minus_nc.to_excel('resources/Aug8/NT_minus_NC.xlsx')
