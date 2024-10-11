import pandas as pd


def transform_bed_to_set(path_to_bed: str) -> set:
    obj_set = set()
    df = pd.read_csv(path_to_bed, sep='\t', header=None)
    df_projection = df.iloc[:, 0:3]
    for i in range(len(df_projection)):
        string_rep = str(df.iloc[i, 0]) + ',' + str(df.iloc[i, 1]) + ',' + str(df.iloc[i, 2])
        obj_set.add(string_rep)
    return obj_set


set_gc = transform_bed_to_set('resources/2024_jan14/AhrArnt_MA0006.1_GC_all_bound.bed')
set_gt = transform_bed_to_set('resources/2024_jan14/AhrArnt_MA0006.1_GT_all_bound.bed')
unique_elements = set_gc.intersection(set_gt)
a = 7
