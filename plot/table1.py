# Table 1: Average Wait Times Binned by Job Size - Homogeneous
# Job Size, Job Count (%), AWT Random, AWT SGST, %Improvement
import pandas as pd
import plotly.graph_objects as go
from plot_utils import read_rst, read_ult
from dash import Dash, dcc, html
from dash import Dash, html, dcc, Input, Output, callback
from plotly.subplots import make_subplots
import plotly.io as pio
import os


output = 'reproduced/experiments'

###################################################################
# Wait Time vs Node Count (Binned)
###################################################################
exp1c1 ='../data/Results/exp_theta_two_parts/optimal_turnaround_1/cluster_1/Results/theta_2022.rst',
exp1c2 = '../data/Results/exp_theta_two_parts/optimal_turnaround_1/cluster_2/Results/theta_2022.rst',
exp2c1 = '../data/Results/exp_theta_two_parts/probable_user_1_0.5/cluster_1/Results/theta_2022.rst',
exp2c2 = '../data/Results/exp_theta_two_parts/probable_user_1_0.5/cluster_2/Results/theta_2022.rst',
exp_1_name = "SGS-T",
exp_2_name = "Random",
fig_name = f'{output}/homo_avg_wait_vs_node.png',
csv_name = f'{output}/homo_avg_wait_vs_node.csv'

# Read result files 
c1 = read_rst(exp1c1)
c2 = read_rst(exp1c2)
c3 = read_rst(exp2c1)
c4 = read_rst(exp2c2)

exp1_net = pd.concat([c1, c2], axis=0)
exp2_net = pd.concat([c3, c4], axis=0)

# Remove first 1000 and last 1000 jobs
# Cluster warmup period
exp1_net = exp1_net.sort_values(by='id')
exp2_net = exp2_net.sort_values(by='id')
exp1_net = exp1_net.iloc[1000:-1000]
exp2_net = exp2_net.iloc[1000:-1000]

exp1_net['wait_m'] = exp1_net['wait']/60
exp2_net['wait_m'] = exp2_net['wait']/60

# Assign each row a bin label for the column 'proc_binned'
bins = [0, 128, 256, 512, 1024, float('inf')]
labels = ['0-128', '128-256','256-512','512-1024', '1024-2180']
for _df, name in zip([exp1_net, exp2_net], [exp_1_name, exp_2_name]):
    _df['proc_binned'] = pd.cut(_df['proc1'], bins=bins, labels=labels, right=True)

# Plot for each bin
showlegend = True
bin_index = 0  # To keep track of bin index

total_jobs = len(exp1_net)  # Calculate total jobs for percentage calculation

# Plot the overall value
exp1_cpy = exp1_net.copy()
exp2_cpy = exp2_net.copy()

# For the overall case
exp1_cpy['proc_binned'] = 'Overall'
exp2_cpy['proc_binned'] = 'Overall'

mean_exp1_overall = exp1_cpy['wait_m'].mean()
mean_exp2_overall = exp2_cpy['wait_m'].mean()

y_range_overall = [
    min(exp1_cpy['wait_m'].min(),
        exp2_cpy['wait_m'].min()),
    max(exp1_cpy['wait_m'].max(),
        exp2_cpy['wait_m'].max())
]
y_offset_overall = (y_range_overall[1] - y_range_overall[0]) * 0.5  # 5% of the y-range

data = {'Node Counts': labels}
avg_wait_exp1 = []
avg_wait_exp2 = []

for label in labels:
    avg_wait_exp1.append(exp1_net['wait_m'][exp1_net['proc_binned'] == label].mean())
    avg_wait_exp2.append(exp2_net['wait_m'][exp2_net['proc_binned'] == label].mean())

# Add the average wait times to the dictionary
data[exp_2_name] = avg_wait_exp2
data[exp_1_name] = avg_wait_exp1

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Add the overall average wait times
df = pd.concat([df, pd.DataFrame({'Node Counts': ['Overall'], 
                            exp_2_name: [mean_exp2_overall],
                            exp_1_name: [mean_exp1_overall]})])

# Save the DataFrame to a CSV file
df.to_csv(csv_name, index=False)

# Calculate % improvement and job counts
df['Percent Improvement'] = ((df[exp_2_name] - df[exp_1_name]) / df[exp_2_name]) * 100

job_counts = []
for label in labels:
    count = len(exp1_net['proc_binned'][exp1_net['proc_binned'] == label])
    job_counts.append(f"{count} ({count/total_jobs*100:.1f}%)")  # Add count and percentage
job_counts.append(total_jobs)  # Add overall job count
df['Job Count'] = job_counts

# Save the updated DataFrame to a CSV file
df = df.round(1) 
df.to_csv(csv_name, index=False)