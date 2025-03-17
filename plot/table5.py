# Table 5: Average wait time in seconds by original system and system selected by CQSim+.
# Original System, System Selected by CQSim+, Number of Jobs, AWT Siloed, AWT CQSim+, %Improv
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plot_utils import read_rst, read_ult, parse_data, bar_bin_avgs, bar_bin_counts, read_swf_polaris_theta
from dash import Dash, dcc, html
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os
import csv

output = 'reproduced/case_study'

def round_hrs(num):
    num = num/3600
    num = float(num)
    return round(num, 2)

def round_s(num):
    num = float(num)
    return round(num, 2)

def table5():
    
    swf = read_swf_polaris_theta('../preprocessing/output/polaris_theta_23.swf')
    sim_theta = read_rst('../data/Results/exp_polaris_theta/only_theta/theta/Results/theta_23.rst')
    sim_polaris = read_rst('../data/Results/exp_polaris_theta/only_polaris/polaris/Results/polaris_23.rst')
    ms_theta = read_rst('../data/Results/exp_polaris_theta/sgst/theta/Results/polaris_theta_23.rst')
    ms_polaris = read_rst('../data/Results/exp_polaris_theta/sgst/polaris/Results/polaris_theta_23.rst')

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
    # How many polaris and theta jobs originally?
    num_polaris_jobs = len(polaris_id_map)
    num_theta_jobs = len(theta_id_map)

    num_polaris_on_theta = 0
    num_theta_on_theta = 0
    for index, row in ms_theta.iterrows():
        if row['id'] in polaris_id_map:
            num_polaris_on_theta += 1
        
        if row['id'] in theta_id_map:
            num_theta_on_theta += 1


    num_theta_on_polaris = 0
    num_polaris_on_polaris = 0
    for index, row in ms_polaris.iterrows():
        if row['id'] in theta_id_map:
            num_theta_on_polaris += 1

        if row['id'] in polaris_id_map:
            num_polaris_on_polaris += 1


    sim_polaris['meta_id'] = sim_polaris['id'].map(polaris_id_map)
    sim_theta['meta_id'] = sim_theta['id'].map(theta_id_map)

    # Get the jobs on ms_theta that were polaris jobs
    ms_theta_polaris = pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')

    # Get the jobs on ms_polaris that were theta jobs
    ms_polaris_theta = pd.merge(ms_polaris, sim_theta, left_on='id', right_on= 'meta_id', how='inner')

    # polaris jobs on theta
    pot = pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')


    # theta jobs on theta
    tot =  pd.merge(ms_theta, sim_theta, left_on='id', right_on= 'meta_id', how='inner')

    
    # theta jobs on polaris
    top =  pd.merge(ms_polaris, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')

    # polaris jobs on polaris
    pop =  pd.merge(ms_polaris, sim_theta, left_on='id', right_on= 'meta_id', how='inner')

    bins = [1, 8, 32, 64, 128, 256, 560]

    # Bin the data
    pop['proc1_binned'] = pd.cut(pop['proc1_x'], bins=bins)
    pot['proc1_binned'] = pd.cut(pot['proc1_x'], bins=bins)

    # Count the occurrences in each bin
    pop_counts = pop['proc1_binned'].value_counts()
    pot_counts = pot['proc1_binned'].value_counts()


    # Convert Interval objects to strings
    pop_counts.index = pop_counts.index.astype(str)
    pot_counts.index = pot_counts.index.astype(str)

    # Create the pie charts using Plotly Express with custom category ordering
    bin_labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins) - 1)]

    bins = [1, 128, 256, 512, 1024, 2180, 4360]

    # Bin the data
    top['proc1_binned'] = pd.cut(top['proc1_x'], bins=bins)
    tot['proc1_binned'] = pd.cut(tot['proc1_x'], bins=bins)

    # Count the occurrences in each bin
    top_counts = top['proc1_binned'].value_counts()
    tot_counts = tot['proc1_binned'].value_counts()


    # Convert Interval objects to strings
    top_counts.index = top_counts.index.astype(str)
    tot_counts.index = tot_counts.index.astype(str)


    only_polaris = pd.concat([
        pd.merge(ms_polaris, sim_polaris, left_on='id', right_on= 'meta_id', how='inner'),
        pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')
    ])
    polaris_gpu = pd.merge(only_polaris, swf, left_on='meta_id', right_on='id', how='left')


    header = ["Original System", "System selected by CQSim+", "Number of Jobs" ,"Wait Time (hrs) (siloed)", "Wait Time (hrs) (CQSim+)", "%Improv"]

    # Polaris on Polaris
    pop_awt_old = pop['wait_y'].mean()
    pop_awt_plus = pop['wait_x'].mean()
    pop_improv = ((pop_awt_old - pop_awt_plus)/pop_awt_old) * 100
    pop_row = ["Polaris", "Polaris", num_polaris_on_polaris, round_hrs(pop_awt_old), round_hrs(pop_awt_plus), round_s(pop_improv)]
    # Theta on Polaris
    top_awt_old = top['wait_y'].mean()
    top_awt_plus = top['wait_x'].mean()
    top_improv = ((top_awt_old - top_awt_plus)/top_awt_old) * 100
    top_row = ["Theta", "Polaris", num_theta_on_polaris, round_hrs(top_awt_old), round_hrs(top_awt_plus), round_s(top_improv)]

    # Polaris on Theta
    pot_awt_old = pot['wait_y'].mean()
    pot_awt_plus = pot['wait_x'].mean()
    pot_improv = ((pot_awt_old - pot_awt_plus)/pot_awt_old) * 100
    pot_row = ["Polaris", "Theta", num_polaris_on_theta, round_hrs(pot_awt_old), round_hrs(pot_awt_plus), round_s(pot_improv)]

    # Theta on Theta    
    tot_awt_old = tot['wait_y'].mean()
    tot_awt_plus = tot['wait_x'].mean()
    tot_improv = ((tot_awt_old - tot_awt_plus)/tot_awt_old) * 100
    tot_row = ["Theta", "Theta", num_theta_on_theta, round_hrs(tot_awt_old), round_hrs(tot_awt_plus), round_s(tot_improv)]

    data = [header, pop_row, top_row, pot_row, tot_row]

    with open(f'{output}/table5.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)