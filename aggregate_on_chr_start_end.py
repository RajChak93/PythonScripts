from typing import List
from typing import Dict


def parse_file_to_table(path: str) -> List[List[str]]:
    ret_list = []
    with open(path, 'rt') as f:
        for line in f:
            subparts = line.strip().split('\t')
            assert (len(subparts) == 4)
            ret_list.append(subparts)
    return ret_list


def create_groupby(table: List[List[str]]) -> Dict[str, str]:
    groupby_dict = {}
    for row in table:
        assert (len(row) == 4)
        transcription, chr, start, end = row
        key = chr + ',' + start + ',' + end
        if key in groupby_dict:
            groupby_dict[key] = groupby_dict[key] + ',' + transcription
        else:
            groupby_dict[key] = transcription
    return groupby_dict


# Runner
INPUT_FILE = 'resources/2024_05_25/agg_file.txt'
OUTPUT_FILE = 'resources/2024_05_25/results/tab_sep_result.txt'
group_by_dict = create_groupby(parse_file_to_table(INPUT_FILE))
with open(OUTPUT_FILE, 'wt') as f:
    for key, transcriptions in sorted(group_by_dict.items()):
        chr, start, end = key.split(',')
        print(f'{chr}\t{start}\t{end}\t{transcriptions}', file=f)
