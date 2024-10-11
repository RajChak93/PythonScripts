import excel_reading_utils

# Do matching
xl_sheet_name = 'significant'
xl_file_names = ['resources/GT_selected.xlsx', 'resources/NC_selected.xlsx', 'resources/NT_selected.xlsx']
column_names = ['TF1', 'TF2']
# Piu needs to fill this
matching_keywords_list = ['junB', 'NtJAZ1', 'Sox', 'c-jun', 'NtJAZ3', 'GTF2B', 'NF-κB', 'NtJAZ', 'TFAP2b', 'FosB','Foxj', 'DFosB', 'Oct-1', 'GATA', 'STATs', 'NRF1', 'Pr2', 'c-Fos', 'PGC1-α', 'CREB', 'zif268', 'PAP1', 'Arc', 'ERF IX', 'SREBPs', 'YY1', 'NRSE', 'USF', 'NtERF221', 'Smad3', 'junD', 'HIVEP2', 'BRG1', 'Sp1', 'AP1', 'cAMP', 'NRF2', 'Tfb1', 'Egr3', 'Ik', 'NFκB', 'PCBP', 'Homer1', 'Pr1', 'c-FOS', 'PU1', 'NtMYC2b', 'Sp3', 'IκB-α', 'PPARs', 'NtERF32', 'E2F3a', 'GR', 'Fra1', 'EAR', 'MEF2', 'Tfam', 'Fra2', 'NAC1', 'PARP1', 'TT8', 'NtMYC2a', 'lsl1', 'Nr4a1', 'Ets-1', 'NFAT', 'Drp1','DFosB']

# Iterate over all values in a particular column of the 'significant' sheet of an XL file, and match keywords
for xlfile in xl_file_names:
    for colname in column_names:
        set_of_values = excel_reading_utils.read_column_from_xl_sheet(xlfile, xl_sheet_name, colname)
        for keyword in matching_keywords_list:
            keyword = str(keyword) if excel_reading_utils.case_sensitive else str(keyword).casefold()
            if keyword in set_of_values:
                print(f'{keyword} is found in {xlfile}, column {colname}')
