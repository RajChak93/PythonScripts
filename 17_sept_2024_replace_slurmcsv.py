
source_file_dict = {'slurm':'slurm.txt','csv':'csvfile.txt'}


def read_data_from_file(file_type:str):
    source_file = f'resources/2023_09_17/{source_file_dict[file_type]}'
    data = ''
    with open(source_file,'rt') as f:
        data = f.read()
    return data

def write_to_file(file_type:str, file_number:str, source_data:str):
    data_written = source_data.replace('&NUMBER',file_number)
    output_filename = f'resources/2023_09_17/output/{file_number}.{file_type}'
    with open(output_filename,'wt') as f:
        print(data_written,file=f)


def main():
    slurm_data:str = read_data_from_file('slurm')
    csv_data: str = read_data_from_file('csv')
    for file_number in range(45,65):
        write_to_file('slurm',str(file_number),slurm_data)
        write_to_file('csv', str(file_number), csv_data)

if __name__=="__main__":
    main()