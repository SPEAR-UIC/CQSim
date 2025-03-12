import pandas as pd
import sys

swf_columns = [
    'id', 'submit', 'wait', 'run', 'used_proc', 'used_ave_cpu',
    'used_mem', 'req_proc', 'req_time', 'req_mem', 'status',
    'user_id', 'group_id', 'num_exe', 'num_queue',
    'num_part', 'num_pre', 'think_time'
]

def read_swf(trace_path):
    """
    Reads an SWF file into a dataframe

    Args:
        filename: The name of the file to read.

    Returns:
        A list of lists, where each inner list represents a processed line of input.
    """
    data = []

    with open(f'{trace_path}', 'r') as file:
        for line in file:
        
            # TODO: For now ignoring the header of the swf file
            if line[0] == ';':
                continue

            # Split the line into elements, convert non-empty elements to integers
            row = [int(x) for x in line.split() if x]
            data.append(row)
    df = pd.DataFrame(data, columns=swf_columns)
    return df

def check_column_sorted(df: pd.DataFrame, column_name: str, ascending: bool = True) -> bool:
  column_values = df[column_name].values.tolist()  # Get column values as a list
  return column_values == sorted(column_values, reverse=not ascending)

def check_column_nonzero(df: pd.DataFrame, column_name: str) -> bool:
  return (df[column_name] != 0).any()


if __name__ == "__main__":

    trace_path = sys.argv[1]

    swfdf = read_swf(trace_path)


    print("########TEST CASE########\n")
    print(f'Testing trace {trace_path}')

    print("Checking if submit times are sorted...")
    print(check_column_sorted(swfdf, "submit"))

    print("Checking if used_proc is non-zero...")
    print(check_column_nonzero(swfdf, "used_proc"))

    print("Checking if req_proc is non-zero...")
    print(check_column_nonzero(swfdf, "req_proc"))

    print("Checking if req_time is non-zero...")
    print(check_column_nonzero(swfdf, "req_time"))

    print("########TEST CASE########")




