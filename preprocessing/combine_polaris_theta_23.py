import pandas as pd
from test import read_swf

# Define column names for the SWF format
swf_columns_combined = [
    'id', 'submit', 'wait', 'run', 'used_proc', 'used_ave_cpu',
    'used_mem', 'req_proc', 'req_time', 'req_mem', 'status',
    'cluster_id', 'cluster_job_id', 'num_exe', 'is_gpu',
    'num_part', 'num_pre', 'think_time'
]

if __name__ == "__main__":

    import sys
    trace_path_1 = 'output/polaris_23.swf' # cluster id is 0
    trace_path_2 = 'output/theta_23.swf' # cluster id is 1
    trace_path_out = 'output/polaris_theta_23.swf'

    polaris_df= read_swf(trace_path_1)
    polaris_df.columns = swf_columns_combined
    polaris_df['cluster_id'] = 0
    polaris_df['cluster_job_id'] = polaris_df['id']


    theta_df = read_swf(trace_path_2)
    theta_df.columns = swf_columns_combined
    theta_df['cluster_id'] = 1
    theta_df['cluster_job_id'] = theta_df['id']

    df_polaris_theta = pd.concat([polaris_df, theta_df]).sort_values(by='submit')
    df_polaris_theta['id'] = range(1, len(df_polaris_theta) + 1)

    with open(trace_path_out, 'w') as f:
        # Get the maximum width of each column
        col_widths = [
            max(len(str(x)) for x in df_polaris_theta[col].tolist())
            for col in df_polaris_theta.columns
        ]

        # Calculate the total width needed for each row
        total_width = sum(col_widths) + (len(col_widths) - 1) * 3  # 3 spaces between columns

        # Print the data rows with padding for alignment
        for index, row in df_polaris_theta.iterrows():
            row_str = "   ".join([
                str(x).ljust(width)
                for x, width in zip(row, col_widths)
            ])
            f.write(row_str.ljust(total_width) + "\n")  # Pad the entire row for alignment