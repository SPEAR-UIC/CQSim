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


def figure7b():
    polaris_before = pd.concat([pot, pop]).copy()
    polaris_after = pd.concat([top, pop]).copy()
    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Siloed scheduling',
            polaris_before,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x'
        ),
        bar_bin_counts(
            'Multi resource scheduling',
            polaris_after,
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
    # polaris job counts
    pio.write_image(fig_go, f'{output}/figure7b.png')


def figure7a():
    polaris_before = pd.concat([pot, pop]).copy()
    polaris_after = pd.concat([top, pop]).copy()

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
    # polaris avg wait time
    pio.write_image(fig_go, f'{output}/figure7a.png')


def figure7d():

    theta_before = pd.concat([top, tot]).copy()
    theta_after = pd.concat([pot, tot]).copy()

    fig_go = go.Figure(data=[
        bar_bin_counts(
            'Siloed scheduling',
            theta_before,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x'
        ),
        bar_bin_counts(
            'Multi resource scheduling',
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
    # theta jobs
    pio.write_image(fig_go, f'{output}/figure7d.png')

def figure7c():

    theta_before = pd.concat([top, tot]).copy()
    theta_after = pd.concat([pot, tot]).copy()

    theta_before['wait_y'] = theta_before['wait_y']/(3600)
    theta_after['wait_x'] = theta_after['wait_x']/(3600)

    fig_go = go.Figure(data=[
        bar_bin_avgs(
            'Siloed scheduling',
            theta_before,
            [1, 8, 32, 64, 128, 256, 512, 1024, 2180, 4360],
            'proc1_x',
            'wait_y'
        ),
        bar_bin_avgs(
            'Multi resource scheduling',
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
    pio.write_image(fig_go, f'{output}/figure7c.png')