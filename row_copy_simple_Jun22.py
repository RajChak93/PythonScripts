import pandas as pd

#xl_sheet_name = 'Sheet1'
xl_file_name = 'resources/June22_piu/NT_selected_filtered.xlsx'

# this list has been extracted from IPA_TF_OUD.xl
matching_keywords_list = ['AP1', 'ACTN4', 'Arc', 'ARID1A', 'ARID2', 'ARNT', 'ARRB1', 'ASH2L', 'ATF4', 'ATN1', 'BCL10',
                          'BCL11A', 'BCL11B', 'BCL3', 'BCL6B', 'BHLHE41', 'BMAL1', 'BRCA1', 'BRG1', 'BTG2', 'c-Fos',
                          'c-jun', 'cAMP', 'CC2D1A', 'CC2D1B', 'CCNT1', 'CDKN2A', 'CDKN2C', 'CEBPA', 'CEBPB', 'CEBPD',
                          'CITED2', 'CLOCK', 'CNBP', 'CREB', 'CREB1', 'CREBBP', 'CTCF', 'CTNNB1', 'CUX1', 'DACH1',
                          'DBP', 'DEAF1', 'DEK', 'DFosB', 'DLX1', 'DLX2', 'Drp1', 'DUX4', 'E2F3a', 'EAR', 'ECSIT',
                          'EGR2', 'Egr3', 'ELF4', 'ELF5', 'ELK1', 'EN1', 'EP300', 'EPAS1', 'ERF', 'ESX1', 'Ets-1',
                          'ETS1', 'ETV3', 'ETV6', 'EZH2', 'FEV', 'FOS', 'FosB', 'FOSL1', 'FOXA1', 'FOXA2', 'Foxj',
                          'FOXM1', 'FOXO1', 'FOXO3', 'Fra1', 'Fra2', 'GABPA', 'GATA', 'GATA2', 'GFI1', 'GPS2', 'GR',
                          'GSX2', 'GTF2B', 'GTF2F2', 'GTF3A', 'HDAC1', 'HDAC11', 'HDAC3', 'HDAC4', 'HES5', 'HIC1',
                          'HIF1A', 'HIVEP1', 'HIVEP2', 'HMGA1', 'HMGB1', 'HMGB2', 'HNF4A', 'Homer1', 'HOXA5', 'HOXB4',
                          'HOXB9', 'HSF2', 'HTT', 'IFI16', 'Ik', 'IKZF1', 'IKZF3', 'ILF3', 'ING4', 'IRF1', 'IRF2BP1',
                          'IRF3', 'IRF4', 'IRF5', 'IRF8', 'IRF9', 'IX', 'JARID2', 'JUN', 'junB', 'junD', 'KAT2B',
                          'KAT5', 'KDM3A', 'KLF11', 'KLF13', 'Klf16', 'KLF5', 'KLF6', 'KLF9', 'KMT2C', 'LEF1', 'LHX5',
                          'LITAF', 'LMX1A', 'lsl1', 'MAF', 'MAFA', 'MAFB', 'MAFF', 'MAML1', 'MBD2', 'MECP2', 'MED6',
                          'MEF2', 'MIB2', 'MTA1', 'MYOCD', 'MZF1', 'NAC1', 'NCOA3', 'NCOA4', 'NCOR1', 'NCOR2',
                          'NEUROD2', 'NEUROG1', 'NF_B', 'NF-_B', 'NFAT', 'NFAT5', 'NFATC2', 'NFE2L2', 'NFIX', 'NFKB1',
                          'NFKBIA', 'NFKBIZ', 'NKRF', 'NKX3-1', 'NONO', 'NOTCH1', 'NPAS2', 'NPM1', 'Nr4a1', 'NRF1',
                          'NRF2', 'NRSE', 'NtJAZ1', 'Oct', 'ONECUT2', 'PAP1', 'PARP1', 'PAX3', 'PBX2', 'PCBP', 'PDYN',
                          'PGC1-_', 'PHB1', 'PHB2', 'PHOX2A', 'PIAS1', 'PITX3', 'PKNOX2', 'PML', 'POU2F1', 'POU5F1',
                          'PPARs', 'PPRC1', 'Pr1', 'Pr2', 'PRDM1', 'PRDM8', 'PRRX1', 'PSMD10', 'PTF1A', 'PU1', 'PYCARD',
                          'RAD21', 'RB1', 'RCOR1', 'REL', 'RELA', 'RELB', 'REST', 'SALL4', 'Scn4b', 'SFR1', 'SIN3A',
                          'SIX2', 'SIX4', 'Smad3', 'SMAD6', 'SMARCA4', 'SMARCE1', 'Sox', 'SOX9', 'Sp1', 'Sp3', 'SP4',
                          'SPI1', 'SQSTM1', 'SREBF2', 'SREBP', 'SRY', 'STAT', 'STAT1', 'STAT2', 'STAT3', 'STAT6',
                          'SUPT5H', 'TARDBP', 'Tfam', 'TFAP2b', 'TFAP2C', 'Tfb1', 'TFEB', 'THRAP3', 'TLX1', 'TLX3',
                          'TNF', 'TP53', 'TP63', 'TP73', 'TRIM28', 'TRIM32', 'TRIM66', 'TSC22D1', 'TSC22D3', 'TT8',
                          'TWIST1', 'TWIST2', 'USF', 'VDR', 'WBP2', 'WT1', 'WWTR1', 'XBP1', 'YAP1', 'YBX1', 'YY1',
                          'ZBTB16', 'ZGPAT', 'ZIC2', 'zif268', 'ZNF32', 'ZNF350', 'ZNF366']
# create set out of matching keywords
# matching_keywords_set = set(matching_keywords_list)
matching_keywords_set = {word.casefold() for word in matching_keywords_list}  # make it non case-sensitive

original_df = pd.read_excel(io=xl_file_name)
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
output_xl_sheet = 'resources/June22_piu/result1_NT_selected_filtered.xlsx'
result_df.to_excel(output_xl_sheet)
