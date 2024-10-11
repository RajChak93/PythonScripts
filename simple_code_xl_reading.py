import pandas as pd


# Do matching
xl_sheet_name = 'significant'
xl_file_names = ['resources/GT_selected.xlsx', 'resources/NC_selected.xlsx', 'resources/NT_selected.xlsx']
column_names = ['TF1', 'TF2']
matching_keywords_list = ['TBX1','junB', 'NtJAZ1', 'Sox', 'c-jun', 'NtJAZ3', 'GTF2B', 'NF-κB', 'NtJAZ', 'TFAP2b', 'FosB','Foxj', 'DFosB', 'Oct-1', 'GATA', 'STATs', 'NRF1', 'Pr2', 'c-Fos', 'PGC1-α', 'CREB', 'zif268', 'PAP1', 'Arc', 'ERF', 'IX', 'SREBPs', 'YY1', 'NRSE', 'USF', 'NtERF221', 'Smad3', 'junD', 'HIVEP2', 'BRG1', 'Sp1', 'AP1', 'cAMP', 'NRF2', 'Tfb1', 'Egr3', 'Ik', 'NFκB', 'PCBP', 'Homer1', 'Pr1', 'c-FOS', 'PU1', 'NtMYC2b', 'Sp3', 'IκB-α', 'PPARs', 'NtERF32', 'E2F3a', 'GR', 'Fra1', 'EAR', 'MEF2', 'Tfam', 'Fra2', 'NAC1', 'PARP1', 'TT8', 'NtMYC2a', 'lsl1', 'Nr4a1', 'Ets-1', 'NFAT', 'Drp1','DFosB']

# Iterate over all values in a particular column of the 'significant' sheet of an XL file, and match keywords
for xlfile in xl_file_names:
    for colname in column_names:
#-------------function begins----------
        set_of_values = set()
        df = pd.read_excel(io=xlfile, sheet_name=xl_sheet_name)
        column_values_list = df[colname].values.tolist()
        for val in column_values_list:
            set_of_values.add(str(val))
#-----------------function ends--------
        for keyword in matching_keywords_list:
            if keyword in set_of_values:
                print(f'{keyword} is found in {xlfile}, column {colname}')
