from excel_reading_utils import read_all_excel_sheets
from itertools import product
from itertools import combinations

def match(str1, str2):
    list1 = str1.split(".")
    list2 = str2.split(".")
    if len(list1) != 3:
        raise Exception(f"{str1} doesn't conform to format")
    if len(list2) != 3:
        raise Exception(f"{str2} doesn't conform to format")
    gene1 = list1[2]
    gene2 = list2[2]
    return gene1.lower() == gene2.lower()


dict_sheetname_to_valueset = read_all_excel_sheets('resources/oct12/Glia_control.xlsx', 'col')
sheet_name_pairs = [list(x) for x in combinations(dict_sheetname_to_valueset, 2)]


for sheet1, sheet2 in sheet_name_pairs:
    set1 = dict_sheetname_to_valueset[sheet1]
    set2 = dict_sheetname_to_valueset[sheet2]
    repeated_entries = {i for i, j in product(set1, set2) if i in set1 and match(i, j)}
    print(f'{sheet1},{sheet2} -> common entries = {len(repeated_entries)}')
print('done')

# {i for i,j in product(set_a, set_b) if i in set_b and match(i,j)}
