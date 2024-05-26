# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:11:05 2024

@author: super
"""
import os
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objs as go
pio.renderers.default='browser'

def get_txt_files(directory):
    txt_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(file)
    
    return txt_files

if __name__=="__main__":
    
    num_directories = len(next(os.walk('.'))[1])
    current_directory = os.getcwd()
    directories = [d for d in os.listdir(current_directory) if os.path.isdir(d)]
    filenames = {}
    dataframes_dict = {}
    dataframes_means_dict = {}
    molardidad_media_ambos = {}
    molaridad_std_ambos = {}
    lambda_max_media_ambos = {}
    lambda_max_std_ambos = {}
    absorbancia_media_ambos = {}
    absorbancia_std_ambos = {}
    area_media_ambos = {}
    area_std_ambos = {}
    
    # Recorremos los directorios enumerados y guardamos los .txt
    for i in range(1,(num_directories+1)):
        filenames[i]= get_txt_files(f".\{directories[i-1]}")
        lambda_mean = []
        abs_mean = []
        # Cogemos los filenames y abrimos los datos y los guardamos en dataframes
        for file in filenames[i]:
            if file == 'ambos.txt':
                dataframes_dict[f'{i}/{file}'] = pd.read_csv(f".\{directories[i-1]}\{file}")
            else:
                dataframes_dict[file] = pd.read_csv(f".\{directories[i-1]}\{file}", sep='\t', decimal=','
                                                , skiprows=1)
                # Buscamos los indices mas cercanos a estos valores
                min_lambda = 300
                max_lambda = 800
                column_name = "Wavelength nm."
                
                # Calcular diferencias absolutas
                absolute_differences_min = (dataframes_dict[file][column_name] - 
                                        min_lambda).abs()
                absolute_differences_max = (dataframes_dict[file][column_name] - 
                                        max_lambda).abs()
                # Encontrar los indices más cercanos
                min_lambda_index = absolute_differences_min.idxmin()
                max_lambda_index = absolute_differences_max.idxmin()
                
                # Sobreescribimos en ese rango
                dataframes_dict[file] = dataframes_dict[file].loc[min_lambda_index: 
                                                                  max_lambda_index]
    
    # Ahora recorremos los ficheros por sus valores y hacemos la media
    for key, value in filenames.items():
        for file in value:
            if file == 'ambos.txt':
                molardidad_media_ambos[key] = dataframes_dict[f'{key}/{file}']['molaridad'].mean()
                molaridad_std_ambos[key] = dataframes_dict[f'{key}/{file}']['molaridad'].std()
                
                lambda_max_media_ambos[key] = dataframes_dict[f'{key}/{file}']['lambda máx'].mean()
                lambda_max_std_ambos[key] = dataframes_dict[f'{key}/{file}']['lambda máx'].std()
                
                absorbancia_media_ambos[key] = dataframes_dict[f'{key}/{file}']['absorbancia'].mean()
                absorbancia_std_ambos[key] = dataframes_dict[f'{key}/{file}']['absorbancia'].std()
                
                area_media_ambos[key] = dataframes_dict[f'{key}/{file}']['área'].mean()
                area_std_ambos[key] = dataframes_dict[f'{key}/{file}']['área'].std()
            
    # Extracting values from dictionaries
    molaridades = list(molardidad_media_ambos.values())
    lambdas_max = list(lambda_max_media_ambos.values())
    absorbancias = list(absorbancia_media_ambos.values())
    areas = list(area_media_ambos.values())
    absorbancias_errores = list(absorbancia_std_ambos.values())
    lambdas_max_errores = list(lambda_max_std_ambos.values())
    areas_errores = list(area_std_ambos.values())
    molaridades_text = ['{:.2e}'.format(value) for value in molaridades]
    eje_x = np.linspace(0.2,2,num=10)
    eje_x_text = ['{:.0e}'.format(value) for value in eje_x]
    
    # Create traces
    trace_lambdas = go.Scatter(
        x=molaridades, y=lambdas_max, 
        mode='markers+text',
        name='Lambdas máximas',
        text=directories,
        textposition='middle right',
        error_y=dict(
            type='data',
            array=lambdas_max_errores,
            visible=True)
        )
    trace_absorbancias = go.Scatter(
        x=molaridades, y=absorbancias, 
        mode='markers+text',
        name='Extinción',
        text=directories,
        textposition='middle right',
        error_y=dict(
            type='data',
            array=absorbancias_errores,
            visible=True)
        )
    trace_area = go.Scatter(
        x=molaridades, y=areas, 
        mode='markers+text',
        name='Área',
        text=directories,
        textposition='middle right',
        error_y=dict(
            type='data',
            array=areas_errores,
            visible=True)
        )
    
    # Fit a polynomial regression line
    z = np.polyfit(molaridades, lambdas_max, 3)
    p = np.poly1d(z)
    # Calculate trendline values for plotting
    trendline_values1 = np.linspace(min(molaridades), max(molaridades), 100)
    trendline_values2 = p(trendline_values1)
    
    z1 = np.polyfit(molaridades, absorbancias, 1)
    p1 = np.poly1d(z1)
    # Calculate trendline values for plotting
    trendline_values3 = p1(trendline_values1)
    
    z2 = np.polyfit(molaridades, areas, 1)
    p2 = np.poly1d(z2)
    # Calculate trendline values for plotting
    trendline_values4 = p2(trendline_values1)
    
    trendline_lambdas = go.Scatter(
        x=trendline_values1, y=trendline_values2, 
        mode='lines', 
        name='Trend line')
    
    trendline_absorbancias= go.Scatter(
        x=trendline_values1, y=trendline_values3, 
        mode='lines', 
        name='Trend line')
    
    trendline_areas = go.Scatter(
        x=trendline_values1, y=trendline_values4, 
        mode='lines', 
        name='Trend line')
    
    # Create layout
    layout1 = go.Layout(
        title='ml citrato vs λ máximas(nm)',
        xaxis=dict(title='ml citrato',
                   tickmode='array',
                   tickvals=eje_x),
        yaxis=dict(title='λ (nm)'),
        showlegend=True,
        hovermode='closest',
        legend=dict(x=0.01, y=0.99)
    )
    
    layout2 = go.Layout(
        title='ml citrato vs Extinción',
        xaxis=dict(title='ml citrato',
                   tickmode='array',
                   tickvals=eje_x),
        yaxis=dict(title='Extinción'),
        showlegend=True,
        hovermode='closest',
        legend=dict(x=0.01, y=0.99)
    )
    
    layout3 = go.Layout(
        title='ml citrato vs Área',
        xaxis=dict(title='ml citrato',
                   tickmode='array',
                   tickvals=eje_x),
        yaxis=dict(title='Área'),
        showlegend=True,
        hovermode='closest',
        legend=dict(x=0.01, y=0.99)
    )
    # Create figure object
    fig = go.Figure(data=[trace_lambdas, trendline_lambdas], layout=layout1)
    fig2 = go.Figure(data=[trace_absorbancias, trendline_absorbancias], layout=layout2)
    fig3 = go.Figure(data=[trace_area, trendline_areas], layout=layout3)
    
    # Display the plot in the browser
    pio.show(fig)
    pio.show(fig2)
    pio.show(fig3)

    
                
                
