import pandas as pd

xl_sheet_name = 'Sheet1'
xl_file_name = 'resources/GT_divconv.xlsx'

# this list has been extracted from IPA_TF_OUD.xl
matching_keywords_list = ['ATN1', 'BHLHE41', 'CC2D1A', 'CC2D1B', 'CLOCK', 'CNBP', 'CREB1', 'CTCF', 'CTNNB1', 'DEAF1',
                          'DLX1', 'DLX2', 'EN1', 'EPAS1', 'FEV', 'GSX2', 'GTF2F2', 'HDAC4', 'HES5', 'HIC1', 'HTT',
                          'IRF8', 'KLF11', 'Klf16', 'LHX5', 'LMX1A', 'MAFA', 'MECP2', 'NEUROD2', 'NFE2L2', 'NKX3-1',
                          'PHOX2A', 'PIAS1', 'PITX3', 'PRDM8', 'PTF1A', 'RAD21', 'RCOR1', 'REST', 'SP1', 'SP3', 'STAT6',
                          'THRAP3', 'TLX1', 'TLX3', 'ZIC2']
# create set out of matching keywords
# matching_keywords_set = set(matching_keywords_list)
matching_keywords_set = {word.casefold() for word in matching_keywords_list}  # make it non case-sensitive

original_df = pd.read_excel(io=xl_file_name, sheet_name=xl_sheet_name)
column_names_of_original_df = original_df.columns.values.tolist()
print(column_names_of_original_df)
# Create a new result dataframe with the same schema as the source XL sheet but empty
result_df = pd.DataFrame(columns=column_names_of_original_df)

for index, row in original_df.iterrows():
    val_tf1 = str(row['TF1']).casefold()
    val_tf2 = str(row['TF2']).casefold()
    if val_tf1 in matching_keywords_set or val_tf2 in matching_keywords_set:
        # append series to result df
        new_row = row.to_frame().T  # remember we need to take transpose
        result_df = pd.concat([result_df, new_row], ignore_index=True)

# write result DF to excel sheet
output_xl_sheet = 'resources/result1_GT_divconv.xlsx'
result_df.to_excel(output_xl_sheet)
