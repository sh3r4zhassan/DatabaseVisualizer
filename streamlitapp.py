import json
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph
import networkx as nx
from pyvis.network import Network
import webbrowser
import random
import plotly.express as px
import streamlit as st




# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "classicmodels",
}

# Fetch Data
conn = mysql.connector.connect(**DB_CONFIG)

query = "SHOW TABLES;"
cursor = conn.cursor()
cursor.execute(query)
tables = cursor.fetchall()
# print(tables)




query = "SELECT * FROM products;"
df = pd.read_sql(query, conn)

# Print Data with Headers
# print(df)

# Export to CSV (Headers Included)
# df.to_csv("payments.csv", index=False)



def plot_graph(data, x, title, type_of_graph, y=None):
    plot_color = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]


    graph_types = {
        'bar': px.bar,
        'scatter': px.scatter,
        'line': px.line,
        'box': px.box,
        'histogram': px.histogram,
        'violin': px.violin,
        'density_contour': px.density_contour,
        'density_heatmap': px.density_heatmap,
        'pie': px.pie
    }

    if type_of_graph not in graph_types:
        raise ValueError(f"Unsupported graph type. Choose from: {', '.join(graph_types.keys())}")
    

    if type_of_graph == 'violin':
        fig = graph_types[type_of_graph](data, x=x, y=y, title=title, color=x, color_discrete_sequence=plot_color)

    elif type_of_graph == 'pie':
        if y is None:
            data = data[x].value_counts().reset_index()
            data.columns = [x, 'count']
            fig = graph_types[type_of_graph](data, names=x, values='count', title=title, color_discrete_sequence=plot_color)
        else:
            fig = graph_types[type_of_graph](data, names=x, values=y, title=title, color_discrete_sequence=plot_color)
            
    elif type_of_graph == 'density_heatmap':
        if y is None:
            raise ValueError(f"'y' value must be provided for {type_of_graph} plots.")
        fig = graph_types[type_of_graph](data, x=x, y=y, title=title,color_continuous_scale='viridis')
    else:
        if y is None:
            raise ValueError(f"'y' value must be provided for {type_of_graph} plots.")
        fig = graph_types[type_of_graph](data, x=x, y=y, title=title, color_discrete_sequence=plot_color, color=x)

    fig.update_layout(
        title={'text': title, 'x': 0.05, 'xanchor': 'left'},
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    if type_of_graph in ['scatter', 'line', 'barplot', 'box', 'histogram', 'violin', 'density_contour', 'density_heatmap']:
        fig.update_xaxes(showline=False, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=False, linewidth=2, linecolor='black')
    else:
        fig.update_layout(showlegend=True)
    
    st.plotly_chart(fig, use_container_width=True)

    return fig



plot_graph(df, x='productLine', y='quantityInStock', title='Sample Graph', type_of_graph='box')
# fig.show()