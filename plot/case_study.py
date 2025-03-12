import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plot_utils import read_rst, read_ult
from dash import Dash, dcc, html
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os


output = 'reproduced/case_study'

swf_columns_combined = [
    'id', 'submit', 'wait', 'run', 'used_proc', 'used_ave_cpu',
    'used_mem', 'req_proc', 'req_time', 'req_mem', 'status',
    'cluster_id', 'cluster_job_id', 'num_exe', 'is_gpu',
    'num_part', 'num_pre', 'think_time'
]

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


def write_obs(str):
    # obsf = 'observations.txt'
    # with open(obsf, 'a') as f:
    #     f.write(str + '\n')
    pass



def polaris_table(df, name, bins = [1, 8, 32, 64, 128, 256, 560]):
    df['proc1_binned'] = pd.cut(df['proc1_x'], bins=bins)

    # Calculate the mean for wait_x and wait_y for each bin
    result = df.groupby('proc1_binned').agg({
        'wait_x': 'mean',
        'wait_y': 'mean'
    })

    # Calculate the count for each bin
    counts = df.groupby('proc1_binned').size()

    # Create a DataFrame from the result
    output_df = pd.DataFrame({
        'bin_name': result.index.astype(str),
        'count': counts,
        'wait_y_mean': result['wait_y'],
        'wait_x_mean': result['wait_x']
    })

    # Calculate % improvement
    output_df['pct_improvement'] = (
        (output_df['wait_y_mean'] - output_df['wait_x_mean']) / output_df['wait_y_mean'] * 100
    )

    # Save to CSV
    output_df.to_csv(f'{name}.csv', index=False)



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

def print_stats():
    
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
    write_obs(f'******Oringal Traces')
    write_obs(f'Number of polaris jobs: {num_polaris_jobs}')
    write_obs(f'Number of theta jobs: {num_theta_jobs}')


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

    # How many polaris jobs went to theta under sgst?
    write_obs(f'******Results Traces')
    write_obs(f'Number of polaris jobs on theta: {num_polaris_on_theta}')
    write_obs(f'Number of theta jobs on polaris: {num_theta_on_polaris}')
    write_obs(f'Number of polaris jobs on polaris: {num_polaris_on_polaris}')
    write_obs(f'Number of theta jobs on theta: {num_theta_on_theta}')



    # What was the original average wait time on polaris, what is the new wait time?
    write_obs(f'******Overall Original vs SGST wait times')
    write_obs(f'Average wait time polaris Only: {sim_polaris['wait'].mean()}')
    write_obs(f'Average wait time polaris SGST: {ms_polaris['wait'].mean()}')
    write_obs(f'Average wait time theta Only: {sim_theta['wait'].mean()}')
    write_obs(f'Average wait time theta SGST: {ms_theta['wait'].mean()}')



    # Create new columns in sim_polaris and sim_theta mapping called meta_id
    print(theta_id_map[1])

    sim_polaris['meta_id'] = sim_polaris['id'].map(polaris_id_map)
    sim_theta['meta_id'] = sim_theta['id'].map(theta_id_map)

    # Get the jobs on ms_theta that were polaris jobs
    ms_theta_polaris = pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')
    # This dataframe should be empty as all polaris jobs must be scaled by 4
    print("[TEST] This data frame should be empty: ", ms_theta_polaris[ms_theta_polaris['run_x'] != 4 * ms_theta_polaris['run_y']])

    # Get the jobs on ms_polaris that were theta jobs
    ms_polaris_theta = pd.merge(ms_polaris, sim_theta, left_on='id', right_on= 'meta_id', how='inner')
    # This dataframe should be empty as all theta jobs must be scaled by 0.25
    print("[TEST] This data frame should be empty: ", ms_polaris_theta[ms_polaris_theta['run_x'] != 0.25 * ms_polaris_theta['run_y']])



    # polaris jobs on theta
    pot = pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')


    # theta jobs on theta
    tot =  pd.merge(ms_theta, sim_theta, left_on='id', right_on= 'meta_id', how='inner')

    
    # theta jobs on polaris
    top =  pd.merge(ms_polaris, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')

    # polaris jobs on polaris
    pop =  pd.merge(ms_polaris, sim_theta, left_on='id', right_on= 'meta_id', how='inner')


    # What was the original average wait time on polaris, what is the new wait time?
    write_obs(f'******New Avg Wait Times per job grouped by origin and cluster')
    write_obs(f'Polaris on Theta: {pot['wait_x'].mean()}')
    write_obs(f'Theta on Theta: {tot['wait_x'].mean()}')
    write_obs(f'Theta on Polaris: {top['wait_x'].mean()}')
    write_obs(f'Polaris on Polaris: {pop['wait_x'].mean()}')

    write_obs(f'******Old Avg Wait Times per job grouped by origin and cluster')
    write_obs(f'Polaris on Theta: {pot['wait_y'].mean()}')
    write_obs(f'Theta on Theta: {tot['wait_y'].mean()}')
    write_obs(f'Theta on Polaris: {top['wait_y'].mean()}')
    write_obs(f'Polaris on Polaris: {pop['wait_y'].mean()}')

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

    fig_pop = px.pie(pop_counts, 
                    values=pop_counts.values, 
                    names=pop_counts.index, 
                    title='',
                    category_orders={"names": bin_labels},
                    labels={"value": "Count"})  # Add count label

    fig_pot = px.pie(pot_counts, 
                    values=pot_counts.values, 
                    names=pot_counts.index, 
                    title='',
                    category_orders={"names": bin_labels},
                    labels={"value": "Count"})  # Add count label

    fig_pop.update_layout(legend=dict(font=dict(size=30)))  # Increase legend text size
    fig_pot.update_layout(legend=dict(font=dict(size=30)))  # Increase legend text size

    # Increase font size of labels and percentage text
    fig_pop.update_traces(textfont_size=20, insidetextfont_size=15)
    fig_pot.update_traces(textfont_size=20, insidetextfont_size=15)

    # Save the images to separate files
    pio.write_image(fig_pop, f'{output}/pop_proc1_pie_chart.png')
    pio.write_image(fig_pot, f'{output}/pot_proc1_pie_chart.png')



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

    # Create the pie charts using Plotly Express with custom category ordering
    bin_labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins) - 1)]
    fig_top = px.pie(top_counts, values=top_counts.values, names=top_counts.index, 
                    title='',  # Remove title
                    category_orders={"names": bin_labels})
    fig_tot = px.pie(tot_counts, values=tot_counts.values, names=tot_counts.index, 
                    title='',  # Remove title
                    category_orders={"names": bin_labels})

    fig_top.update_layout(legend=dict(font=dict(size=30)))  # Increase legend text size
    fig_tot.update_layout(legend=dict(font=dict(size=30)))  # Increase legend text size

    # Increase font size of labels and percentage text
    fig_top.update_traces(textfont_size=20, insidetextfont_size=15)
    fig_tot.update_traces(textfont_size=20, insidetextfont_size=15)

    # Save the images to separate files
    pio.write_image(fig_top, f'{output}/top_proc1_pie_chart.png')
    pio.write_image(fig_tot, f'{output}/tot_proc1_pie_chart.png')



    only_polaris = pd.concat([
        pd.merge(ms_polaris, sim_polaris, left_on='id', right_on= 'meta_id', how='inner'),
        pd.merge(ms_theta, sim_polaris, left_on='id', right_on= 'meta_id', how='inner')
    ])
    polaris_gpu = pd.merge(only_polaris, swf, left_on='meta_id', right_on='id', how='left')


    write_obs(f'******Polaris GPU jobs')
    write_obs(f'Number of Jobs: {len(polaris_gpu [polaris_gpu ['is_gpu'] == 1])}')
    write_obs(f'Original Wait: {polaris_gpu [polaris_gpu ['is_gpu'] == 1]['wait_y'].mean()}')
    write_obs(f'New Wait: {polaris_gpu [polaris_gpu ['is_gpu'] == 1]['wait_x'].mean()}')
    


    write_obs(f'******Polaris CPU jobs')
    write_obs(f'Original Wait: {polaris_gpu [polaris_gpu ['is_gpu'] == 0]['wait_y'].mean()}')
    write_obs(f'New Wait: {polaris_gpu [polaris_gpu ['is_gpu'] == 0]['wait_x'].mean()}')

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




def bar_bin_counts(name, df, bins, bin_col):

    # Bin the data
    df['bin'] = pd.cut(df[bin_col], bins=bins)

    # Count the number of rows per bin
    bin_counts = df.groupby('bin').size()

    # Plotly Graph Objects bar chart
    return go.Bar(x=bin_counts.index.astype(str), y=bin_counts.values, name = name)


def plot_polaris_bar_charts(top, pop, tot, pot):
    polaris_before = pd.concat([pot, pop])
    polaris_after = pd.concat([top, pop])


    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            polaris_after,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Job Count',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )
    # fig_go.show()

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/polaris_jobs.png')

    polaris_before['wait_y'] = polaris_before['wait_y']/(3600)
    polaris_after['wait_x'] = polaris_after['wait_x']/(3600)


    fig_go = go.Figure(data=[
        bar_bin_avgs(
            'Before Meta-scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x',
            'wait_y'
        ),
        bar_bin_avgs(
            'After Meta-Schuediling',
            polaris_after,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x',
            'wait_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Average Wait Time (hrs)',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/polaris_avg_wait.png')

    polaris_before['run_y'] = polaris_before['run_y']/(3600)
    polaris_after['run_x'] = polaris_after['run_x']/(3600)

    polaris_before['turnaround_y'] = polaris_before['run_y'] + polaris_before['wait_y']
    polaris_after['turnaround_x'] = polaris_after['run_x'] + polaris_after['wait_x']

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            polaris_before,
            [0, 1, 2, 4, 8, 16, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            polaris_after,
            [0, 1, 2, 4, 8, 16, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (hrs)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/polaris_turnaround.png')


def plot_theta_bar_charts(top, pop, tot, pot):
    theta_before = pd.concat([top, tot])
    theta_after = pd.concat([pot, tot])


    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            theta_before,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            theta_after,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Job Count',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase x-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/theta_jobs.png')

    theta_before['wait_y'] = theta_before['wait_y']/(3600)
    theta_after['wait_x'] = theta_after['wait_x']/(3600)

    fig_go = go.Figure(data=[
        bar_bin_avgs(
            'Before Meta-scheduling',
            theta_before,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x',
            'wait_y'
        ),
        bar_bin_avgs(
            'After Meta-Schuediling',
            theta_after,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x',
            'wait_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Average Wait Time (hrs)',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/theta_avg_wait.png')

    theta_before['run_y'] = theta_before['run_y']/(3600)
    theta_after['run_x'] = theta_after['run_x']/(3600)

    theta_before['turnaround_y'] = theta_before['run_y'] + theta_before['wait_y']
    theta_after['turnaround_x'] = theta_after['run_x'] + theta_after['wait_x']

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            theta_before,
            [0, 1, 2, 4, 8, 16, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            theta_after,
            [0, 1, 2, 4, 8, 16, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (hrs)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/theta_turnaround.png')


def plot_overall_turnaround_1hr_3d(top, pop, tot, pot):

    all = pd.concat([pot, pop, top, tot])

    all['wait_y'] = all['wait_y']/(3600)
    all['wait_x'] = all['wait_x']/(3600)

    all['run_y'] = all['run_y']/(3600)
    all['run_x'] = all['run_x']/(3600)

    all['turnaround_y'] = all['run_y'] + all['wait_y']
    all['turnaround_x'] = all['run_x'] + all['wait_x']


    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            all,
            [1, 2, 4, 8, 16, 24, 48, 72],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            all,
            [1, 2, 4, 8, 16, 24, 48, 72],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (hrs)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/all_turnaround_1hr_3d.png')

def plot_overall_turnaround_more_3d(top, pop, tot, pot):

    all = pd.concat([pot, pop, top, tot])

    all['wait_y'] = all['wait_y']/(3600)
    all['wait_x'] = all['wait_x']/(3600)

    all['run_y'] = all['run_y']/(3600)
    all['run_x'] = all['run_x']/(3600)

    all['turnaround_y'] = all['run_y'] + all['wait_y']
    all['turnaround_x'] = all['run_x'] + all['wait_x']


    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            all,
            [72, 96, 120, 144, 168, 192, 216, 240],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            all,
            [72, 96, 120, 144, 168, 192, 216, 240],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (hrs)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/all_turnaround_more_4d.png')

def plot_overall_turnaround_under_1hr(top, pop, tot, pot):

    polaris_before = pd.concat([pot, pop])
    print(polaris_before[polaris_before['run_y'] < 60])

    all = pd.concat([pot, pop, top, tot])

    all['wait_y'] = all['wait_y']/(60)
    all['wait_x'] = all['wait_x']/(60)

    all['run_y'] = all['run_y']/(60)
    all['run_x'] = all['run_x']/(60)

    all['turnaround_y'] = all['run_y'] + all['wait_y']
    all['turnaround_x'] = all['run_x'] + all['wait_x']


    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            all,
            [0, 1, 2, 4, 8, 15, 30, 60],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            all,
            [0, 1, 2, 4, 8, 15, 30, 60],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (mins)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/all_turnaround_under_1hr.png')


def plot_gpu_job_analysys(top, pop, tot, pot):

    print("Polaris on Polaris", len(pop))

    swf = read_swf_polaris_theta('../preprocessing/output/polaris_theta_23.swf')
    _polaris_before = pd.merge(pop, swf, left_on='meta_id', right_on='id', how='left')
    _polaris_after = pd.merge(pop, swf, left_on='meta_id', right_on='id', how='left')
    polaris_before = _polaris_before[_polaris_before['is_gpu'] == 1]
    polaris_after = _polaris_after[_polaris_after['is_gpu'] == 1]

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Job Count',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )
    # fig_go.show()

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/gpu_jobs.png')

    polaris_before['wait_y'] = polaris_before['wait_y']/(3600)
    polaris_after['wait_x'] = polaris_after['wait_x']/(3600)


    fig_go = go.Figure(data=[
        bar_bin_avgs(
            'Before Meta-scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x',
            'wait_y'
        ),
        bar_bin_avgs(
            'After Meta-Schuediling',
            polaris_after,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x',
            'wait_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Average Wait Time (hrs)',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/gpu_avg_wait.png')

    polaris_before['run_y'] = polaris_before['run_y']/(3600)
    polaris_after['run_x'] = polaris_after['run_x']/(3600)

    polaris_before['turnaround_y'] = polaris_before['run_y'] + polaris_before['wait_y']
    polaris_after['turnaround_x'] = polaris_after['run_x'] + polaris_after['wait_x']

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            polaris_before,
            [0, 1, 2, 4, 8, 16, 24, 72, 168, 336],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling',
            polaris_after,
            [0, 1, 2, 4, 8, 16, 24, 72, 168, 192, 336],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (hrs)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/gpu_turnaround.png')

def plot_pot_analysis(top, pop, tot, pot):

    print("Polaris on Polaris", len(pop))

    swf = read_swf_polaris_theta('../preprocessing/output/polaris_theta_23.swf')
    _polaris_before = pd.merge(pop, swf, left_on='meta_id', right_on='id', how='left')
    _polaris_after = pd.merge(pop, swf, left_on='meta_id', right_on='id', how='left')
    polaris_before = pot
    polaris_after = pot

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Job Count',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )
    # fig_go.show()

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/pot_jobs.png')

    polaris_before['wait_y'] = polaris_before['wait_y']/(3600)
    polaris_after['wait_x'] = polaris_after['wait_x']/(3600)


    fig_go = go.Figure(data=[
        bar_bin_avgs(
            'Before Meta-scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x',
            'wait_y'
        ),
        bar_bin_avgs(
            'After Meta-Schuediling',
            polaris_after,
            [1, 8, 32, 64, 128, 256, 560],
            'proc1_x',
            'wait_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Job Size',
        yaxis_title='Average Wait Time (hrs)',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/pot_avg_wait.png')

    polaris_before['run_y'] = polaris_before['run_y']/(3600)
    polaris_after['run_x'] = polaris_after['run_x']/(3600)

    polaris_before['turnaround_y'] = polaris_before['run_y'] + polaris_before['wait_y']
    polaris_after['turnaround_x'] = polaris_after['run_x'] + polaris_after['wait_x']

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Before Meta-scheduling',
            polaris_before,
            [0, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 24, 72, 168, 336],
            'turnaround_y'
        ),
        bar_bin_counts(
            'After Meta-Schuediling', 
            polaris_after,
            [0, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 24, 72, 168, 336],
            'turnaround_x'
        )])
    
    fig_go.update_layout(
        xaxis_title='Turn Around Time (hrs)',
        yaxis_title='Job Counts',
        plot_bgcolor='white',  # Set background color to white
        xaxis=dict(
            showgrid=True,  # Show x-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        yaxis=dict(
            showgrid=True,  # Show y-axis grid
            gridcolor='lightgrey',  # Set grid color to light grey
            tickfont=dict(size=16),  # Increase y-axis tick font size
            title_font = dict(size=20), # Set the x-axis title font size
        ),
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=20)
        )
    )

    # Save the Graph Objects figure using pio
    pio.write_image(fig_go, f'{output}/pot_turnaround.png')



if __name__ == "__main__":
    if not os.path.exists(output):
        os.makedirs(output)


    top, pop, tot, pot = parse_data()

    plot_polaris_bar_charts(top, pop, tot, pot)
    plot_theta_bar_charts(top, pop, tot, pot)
    plot_overall_turnaround_1hr_3d(top, pop, tot, pot)
    plot_overall_turnaround_under_1hr(top, pop, tot, pot)
    plot_overall_turnaround_more_3d(top, pop, tot, pot)
    plot_gpu_job_analysys(top, pop, tot, pot)
    plot_pot_analysis(top, pop, tot, pot)
    print_stats()