import pandas as pd

import excel_reading_utils
def process_nt():
    folder_names = ['resources/2023_Oct29/nt']
    dfs_list = []
    numrows = 0
    xl_files = excel_reading_utils.get_xl_file_list_from_folder(folder_names[0])
    for xl_file in xl_files:
        df1 = pd.read_excel(io=xl_file)
        # dfx = df1["site1_name"]
        # dfxcnt = len(dfx)
        # dfy = df1["gene_name"]
        # dfycnt = len(dfy)
        dfz = df1[["site1_name", "gene_name"]]
        dfzcnt = len(dfz)
        numrows = numrows + dfzcnt
        dfs_list.append(dfz)
        print(xl_file)
    # ans = excel_reading_utils.create_consolidated_df(folder_names[0], column_to_be_read_list)
    ans = pd.concat(dfs_list)
    anscnt = len(ans)
    print(f'Hello {numrows} {anscnt}')
    # write result DFs to excel sheet
    ans.to_excel('resources/2023_Oct29/nt/NT_consolidated.xlsx')


def process_nc():
    folder_names = ['resources/2023_Oct29/nc']
    dfs_list = []
    numrows = 0
    xl_files = excel_reading_utils.get_xl_file_list_from_folder(folder_names[0])
    xl_files.sort()
    for xl_file in xl_files:
        df1 = pd.read_excel(io=xl_file)
        dfx = df1["site1_name"]
        dfxcnt = len(dfx)
        dfy = df1["gene_name"]
        dfycnt = len(dfy)
        dfz = df1[["site1_name", "gene_name"]]
        dfzcnt = len(dfz)
        numrows = numrows + dfzcnt
        dfs_list.append(dfz)
        print(xl_file)
    # ans = excel_reading_utils.create_consolidated_df(folder_names[0], column_to_be_read_list)
    ans = pd.concat(dfs_list)
    anscnt = len(ans)
    print(f'Hello {numrows} {anscnt}')
    # write result DFs to excel sheet
    ans.to_excel('resources/2023_Oct29/nc/NC_consolidated.xlsx')

def process_gt():
    folder_names = ['resources/2023_Oct29/gt']
    dfs_list = []
    numrows = 0
    xl_files = excel_reading_utils.get_xl_file_list_from_folder(folder_names[0])
    xl_files.sort()
    for xl_file in xl_files:
        df1 = pd.read_excel(io=xl_file)
        dfx = df1["site1_name"]
        dfxcnt = len(dfx)
        dfy = df1["gene_name"]
        dfycnt = len(dfy)
        dfz = df1[["site1_name", "gene_name"]]
        dfzcnt = len(dfz)
        numrows = numrows + dfzcnt
        dfs_list.append(dfz)
        print(xl_file)
    # ans = excel_reading_utils.create_consolidated_df(folder_names[0], column_to_be_read_list)
    ans = pd.concat(dfs_list)
    anscnt = len(ans)
    print(f'Hello {numrows} {anscnt}')
    # write result DFs to excel sheet
    ans.to_excel('resources/2023_Oct29/gt/GT_consolidated.xlsx')


def process_gc():
    folder_names = ['resources/2023_Oct29/gc']
    dfs_list = []
    numrows = 0
    xl_files = excel_reading_utils.get_xl_file_list_from_folder(folder_names[0])
    xl_files.sort()
    for xl_file in xl_files:
        df1 = pd.read_excel(io=xl_file)
        dfx = df1["site1_name"]
        dfxcnt = len(dfx)
        dfy = df1["gene_name"]
        dfycnt = len(dfy)
        dfz = df1[["site1_name", "gene_name"]]
        dfzcnt = len(dfz)
        numrows = numrows + dfzcnt
        dfs_list.append(dfz)
        print(xl_file)
    # ans = excel_reading_utils.create_consolidated_df(folder_names[0], column_to_be_read_list)
    ans = pd.concat(dfs_list)
    anscnt = len(ans)
    print(f'Hello {numrows} {anscnt}')
    # write result DFs to excel sheet
    ans.to_excel('resources/2023_Oct29/gc/GC_consolidated.xlsx')


