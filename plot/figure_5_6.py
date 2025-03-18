'''
Plots for homogeneous and heterogenous experiments
'''
import pandas as pd
import plotly.graph_objects as go
from plot_utils import read_rst, read_ult
from dash import Dash, dcc, html
from dash import Dash, html, dcc, Input, Output, callback
from plotly.subplots import make_subplots
import plotly.io as pio
import os

output = 'reproduced/experiments'


def avg_uti_per_week(
        exp1c1,
        exp2c1,
        exp_1_name,
        exp_2_name,
        fig_name,
        start_time_offset = 0,
        line_colors = ['orange', 'green'],
    ):

    c1 = read_ult(exp1c1)
    # c2 = read_ult(exp1c2)
    c3 = read_ult(exp2c1)
    # c4 = read_ult(exp2c2)
    
    fig = go.Figure()

    exp1_net = pd.concat([c1], axis=0)
    exp2_net = pd.concat([c3], axis=0)

    # Remove first 1000 and last 1000 jobs
    # Cluster warmup period
    exp1_net = exp1_net.sort_values(by='timestamp')
    exp2_net = exp2_net.sort_values(by='timestamp')
    exp1_net = exp1_net.iloc[1000:-1000]
    exp2_net = exp2_net.iloc[1000:-1000]

    exp1_net['timestamp'] = exp1_net['timestamp'] + start_time_offset
    exp2_net['timestamp'] = exp2_net['timestamp'] + start_time_offset


    # Convert UNIX timestamps to datetime objects
    exp1_net['datetime'] = pd.to_datetime(exp1_net['timestamp'], unit='s')
    exp2_net['datetime'] = pd.to_datetime(exp2_net['timestamp'], unit='s')

    # Calculate average utilization for each week
    avg_utilization_exp1 = exp1_net.groupby(pd.Grouper(key='datetime', freq='W'))['utilization'].mean()
    avg_utilization_exp2 = exp2_net.groupby(pd.Grouper(key='datetime', freq='W'))['utilization'].mean()

    fig.add_trace(go.Scatter(
        x=avg_utilization_exp1.index,
        y=avg_utilization_exp1.values,
        name=exp_1_name,
        line_color= line_colors[0]
    ))

    fig.add_trace(go.Scatter(
        x=avg_utilization_exp2.index,
        y=avg_utilization_exp2.values,
        name=exp_2_name,
        line_color= line_colors[1]
    ))

    # Customize the layout
    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Average Utilization",
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=25)
        ),
        xaxis = dict(
            title_font = dict(size=20), # Set the x-axis title font size
            tickfont = dict(size=25),  # Set the x-axis tick label font size
        ),
        yaxis = dict(
            title_font = dict(size=20), # Set the y-axis title font size
            tickfont = dict(size=25)  # Set the y-axis tick label font size
        ),
        plot_bgcolor='white'
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    pio.write_image(fig, fig_name, width=1200, height=600)


    return [
        dcc.Markdown(
            f"""
Avg Utilization Per Week
"""
        ),
        dcc.Graph(
            figure=fig
        ),
    ]

def job_submits_per_week(
        exp1c1,
        exp1c2,
        exp_1_name,
        exp_2_name,
        fig_name,
        start_time_offset = 0,
        line_colors = ['orange', 'green']
    ):

    c1 = read_ult(exp1c1)
    c2 = read_ult(exp1c2)
    
    fig = go.Figure()

    exp1_net = pd.concat([c1], axis=0)
    exp2_net = pd.concat([c2], axis=0)

    # Remove first 1000 and last 1000 jobs
    # Cluster warmup period
    exp1_net = exp1_net.sort_values(by='timestamp')
    exp2_net = exp2_net.sort_values(by='timestamp')
    exp1_net = exp1_net.iloc[1000:-1000]
    exp2_net = exp2_net.iloc[1000:-1000]

    exp1_net['timestamp'] = exp1_net['timestamp'] + start_time_offset
    exp2_net['timestamp'] = exp2_net['timestamp'] + start_time_offset


    # Convert UNIX timestamps to datetime objects
    exp1_net['datetime'] = pd.to_datetime(exp1_net['timestamp'], unit='s')
    exp2_net['datetime'] = pd.to_datetime(exp2_net['timestamp'], unit='s')


    # Count submit events per week
    count_submit_events_exp1 = exp1_net[exp1_net['event_type'] == 'S'].groupby(pd.Grouper(key='datetime', freq='W')).size()
    count_submit_events_exp2 = exp2_net[exp2_net['event_type'] == 'S'].groupby(pd.Grouper(key='datetime', freq='W')).size()

    fig.add_trace(go.Scatter(
        x=count_submit_events_exp1.index,
        y=count_submit_events_exp1.values,
        name=exp_1_name,
        line_color=line_colors[0]
    ))

    fig.add_trace(go.Scatter(
        x=count_submit_events_exp2.index,
        y=count_submit_events_exp2.values,
        name=exp_2_name,
        line_color=line_colors[1]
    ))

    # Customize the layout
    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="No. of Jobs Submitted",
        legend=dict(
            yanchor="top",
            y=1.15,
            xanchor="left",
            x=0.01,
            orientation='h',
            font=dict(size=25)
        ),
        xaxis = dict(
            title_font = dict(size=20), # Set the x-axis title font size
            tickfont = dict(size=25),  # Set the x-axis tick label font size
        ),
        yaxis = dict(
            title_font = dict(size=20), # Set the y-axis title font size
            tickfont = dict(size=25)  # Set the y-axis tick label font size
        ),
        plot_bgcolor='white'
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    pio.write_image(fig, fig_name, width=1200, height=600)

    return [
        dcc.Markdown(
            f"""
Number of jobs submitted per week
"""
        ),
        dcc.Graph(
            figure=fig
        ),
    ]



def figure5a():
    avg_uti_per_week(
        exp1c1 = '../data/Results/exp_theta_two_parts/probable_user_1_0.5/cluster_1/Results/theta_2022.ult',
        exp2c1 = '../data/Results/exp_theta_two_parts/probable_user_1_0.5/cluster_2/Results/theta_2022.ult',
        exp_1_name = "System 1",
        exp_2_name = "System 2",
        fig_name = f'{output}/figure5a.png',
        start_time_offset=1641021254,
        line_colors=['red', 'blue']
    )
    pass

def figure5b():
    avg_uti_per_week(
        exp1c1 ='../data/Results/exp_theta_two_parts/optimal_turnaround_1/cluster_1/Results/theta_2022.ult',
        exp2c1 = '../data/Results/exp_theta_two_parts/optimal_turnaround_1/cluster_2/Results/theta_2022.ult',
        exp_1_name = "System 1",
        exp_2_name = "System 2",
        fig_name = f'{output}/figure5b.png',
        start_time_offset=1641021254,
        line_colors=['red', 'blue']
    )
    pass

def figure5c():
    job_submits_per_week(
        exp1c1 = '../data/Results/exp_theta_two_parts/probable_user_1_0.5/cluster_1/Results/theta_2022.ult',
        exp1c2 = '../data/Results/exp_theta_two_parts/probable_user_1_0.5/cluster_2/Results/theta_2022.ult',
        exp_1_name = "System 1",
        exp_2_name = "System 2",
        fig_name = f'{output}/figure5c.png',
        start_time_offset=1641021254,
        line_colors=['red', 'blue']
    )
    pass

def figure5d():
    job_submits_per_week(
        exp1c1 ='../data/Results/exp_theta_two_parts/optimal_turnaround_1/cluster_1/Results/theta_2022.ult',
        exp1c2 = '../data/Results/exp_theta_two_parts/optimal_turnaround_1/cluster_2/Results/theta_2022.ult',
        exp_1_name = "System 1",
        exp_2_name = "System 2",
        fig_name = f'{output}/figure5d.png',
        start_time_offset=1641021254,
        line_colors=['red', 'blue']
    )
    pass

def figure6a():
    avg_uti_per_week(
        exp1c1 = '../data/Results/exp_theta_two_parts/probable_user_1.3_0.6/cluster_1/Results/theta_2022.ult',
        exp2c1 = '../data/Results/exp_theta_two_parts/probable_user_1.3_0.6/cluster_2/Results/theta_2022.ult',
        exp_1_name = "System 1",
        exp_2_name = "System 2",
        fig_name=f'{output}/figure6a.png',
        start_time_offset=1641021254,
        line_colors=['red', 'blue']
    )
    pass

def figure6b():
    avg_uti_per_week(
        exp1c1 ='../data/Results/exp_theta_two_parts/optimal_turnaround_1.3/cluster_1/Results/theta_2022.ult',
        exp2c1 = '../data/Results/exp_theta_two_parts/optimal_turnaround_1.3/cluster_2/Results/theta_2022.ult',
        exp_1_name = "System 1",
        exp_2_name = "System 2",
        fig_name=f'{output}/figure6b.png',
        start_time_offset=1641021254,
        line_colors=['red', 'blue']
    )
    pass
