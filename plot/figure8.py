import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plot_utils import read_rst, read_ult, parse_data, bar_bin_avgs, bar_bin_counts
from dash import Dash, dcc, html
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

output = 'reproduced/case_study'
top, pop, tot, pot = parse_data()


def figure8b():

    polaris_before = pot.copy()
    polaris_after = pot.copy()

    polaris_before['wait_y'] = polaris_before['wait_y']/(3600)
    polaris_after['wait_x'] = polaris_after['wait_x']/(3600)


    fig_go = go.Figure(data=[
        bar_bin_avgs(
            'Siloed scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x',
            'wait_y'
        ),
        bar_bin_avgs(
            'Multi resource scheduling',
            polaris_after,
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
    # pot avg wait
    pio.write_image(fig_go, f'{output}/figure8b.png')


def figure8a():

    polaris_before = pot.copy()
    polaris_after = pot.copy()

    polaris_before['run_y'] = polaris_before['run_y']/(3600)
    polaris_after['run_x'] = polaris_after['run_x']/(3600)

    polaris_before['turnaround_y'] = polaris_before['run_y'] + polaris_before['wait_y']
    polaris_after['turnaround_x'] = polaris_after['run_x'] + polaris_after['wait_x']

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Siloed scheduling',
            polaris_before,
            [0, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 24, 72, 168, 336],
            'turnaround_y'
        ),
        bar_bin_counts(
            'Multi resource scheduling',
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
    # pot turnaround
    pio.write_image(fig_go, f'{output}/figure8a.png')