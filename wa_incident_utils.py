def read_line_by_line(filename):
    """
    Read a file line-by-line and return as list
    ignore empty lines
    :return: set of values
    """
    ret_set = set()
    with open(filename, 'rt') as logfile:
        for line in logfile:
            sanitized_line = line.strip()
            if len(sanitized_line) >0:
                ret_set.add(sanitized_line)
    return ret_set

def pretty_print_set(myset):
    for element in myset:
        print(element)

COLS_IN_CORE_FILE = "resources/2024_04_07/cols_in_core.txt"
COLS_IN_BIZ_FILE = "resources/2024_04_07/cols_in_biz.txt"

set_core_cols = read_line_by_line(COLS_IN_CORE_FILE)
set_biz_cols = read_line_by_line(COLS_IN_BIZ_FILE)

print("-------------------CORE - BIZ ----------")
set_core_minus_biz = set_core_cols.difference(set_biz_cols)
pretty_print_set(set_core_minus_biz)


print("-------------------BIZ - CORE ----------")
set_biz_minus_core = set_biz_cols.difference(set_core_cols)
pretty_print_set(set_biz_minus_core)