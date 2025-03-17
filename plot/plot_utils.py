import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

swf_columns_combined = [
    'id', 'submit', 'wait', 'run', 'used_proc', 'used_ave_cpu',
    'used_mem', 'req_proc', 'req_time', 'req_mem', 'status',
    'cluster_id', 'cluster_job_id', 'num_exe', 'is_gpu',
    'num_part', 'num_pre', 'think_time'
]

def read_rst(path):
    column_names = ['id', 'proc1', 'proc2','walltime', 'run', 'wait', 'submit', 'start', 'end']
    df = pd.read_csv(f'{path}', sep=';', header=None) 
    df.columns = column_names
    df_sorted = df.sort_values(by='id')
    return df_sorted

def read_ult(path):
    data = []
    with open(f'{path}', 'r') as f:
        for line in f:
            parts = line.strip().split(';')
            timestamp1, event_type, timestamp2 = parts[0:3]
            metrics = dict(item.split('=') for item in parts[3].split())
            data.append(
                [
                    float(timestamp1), 
                    event_type, 
                    float(timestamp2), 
                    float(metrics['uti']), 
                    float(metrics['waitNum']), 
                    float(metrics['waitSize'])
                ]
            )

    df = pd.DataFrame(data, columns=['timestamp', 'event_type', 'timestamp2', 'utilization', 'waitNum', 'waitSize'])
    df_sorted = df.sort_values(by='timestamp')
    return df_sorted

def read_swf_polaris_theta(trace_path):
    data = []

    with open(f'{trace_path}', 'r') as file:
        for line in file:
        
            # TODO: For now ignoring the header of the swf file
            if line[0] == ';':
                continue

            # Split the line into elements, convert non-empty elements to integers
            row = [int(x) for x in line.split() if x]
            data.append(row)
    df = pd.DataFrame(data, columns=swf_columns_combined)
    return df


def parse_data():
    
    swf = read_swf_polaris_theta('../preprocessing/output/polaris_theta_23.swf')
    sim_theta = read_rst('../data/Results/exp_polaris_theta/only_theta/theta/Results/theta_23.rst')
    sim_polaris = read_rst('../data/Results/exp_polaris_theta/only_polaris/polaris/Results/polaris_23.rst')
    ms_theta = read_rst('../data/Results/exp_polaris_theta/sgst/theta/Results/polaris_theta_23.rst')
    ms_polaris = read_rst('../data/Results/exp_polaris_theta/sgst/polaris/Results/polaris_theta_23.rst')

    # Create a map of old ids to new meta-scheduled ids for each cluster
    polaris_id_map = {
        k:v for k, v in zip(
            swf[swf['cluster_id'] == 0]['cluster_job_id'].to_list(),
            swf[swf['cluster_id'] == 0]['id'].to_list(), 
        )
    }
    theta_id_map = {
        k:v for k, v in zip(
            swf[swf['cluster_id'] == 1]['cluster_job_id'].to_list(),
            swf[swf['cluster_id'] == 1]['id'].to_list(), 
        )
    }


    # Create new columns in sim_polaris and sim_theta mapping called meta_id
    sim_polaris['meta_id'] = sim_polaris['id'].map(polaris_id_map)
    sim_theta['meta_id'] = sim_theta['id'].map(theta_id_map)

    # Join to get the following data

    # polaris jobs on sgst theta
    pot = pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')


    # theta jobs on sgst theta
    tot =  pd.merge(ms_theta, sim_theta, left_on='id', right_on= 'meta_id', how='inner')

    
    # theta jobs on sgst polaris
    top =  pd.merge(ms_polaris, sim_theta, left_on='id', right_on= 'meta_id', how='inner')

    # polaris jobs on sgst polaris
    pop =  pd.merge(ms_polaris, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')

    return top, pop, tot, pot


def bar_bin_counts(name, df, bins, bin_col):

    # Bin the data
    df['bin'] = pd.cut(df[bin_col], bins=bins)

    # Count the number of rows per bin
    bin_counts = df.groupby('bin').size()

    # Plotly Graph Objects bar chart
    return go.Bar(x=bin_counts.index.astype(str), y=bin_counts.values, name = name)


def bar_bin_avgs(name, df, bins, bin_col, avg_col):

    # Bin the data
    df['bin'] = pd.cut(df[bin_col], bins=bins)

    # Calculate the average of avg_col per bin
    bin_averages = df.groupby('bin')[avg_col].mean()

    # Plotly Graph Objects bar chart
    return go.Bar(x=bin_averages.index.astype(str), y=bin_averages.values, name=name)
