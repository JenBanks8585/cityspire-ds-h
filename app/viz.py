import json
import pandas as pd
import plotly.graph_objects as go
from fastapi import APIRouter
from pydantic import BaseModel

from app.helper import load_data_rent_visual


router = APIRouter()


class RentVisual(BaseModel):
    zip: int   


@router.post('/rentforecast_visualize')
async def plotrentforecast(rentvisual: RentVisual):
    """
    Parameters: 
        zip code: int      
         
    Returns: dict
        JSON string for render with react-plotly.js
    """

    df_melt = load_data_rent_visual()[0]
    df_me = load_data_rent_visual()[1]
    df_mew = load_data_rent_visual()[2]

    zips = list(df_me['RegionName'])
    zip = rentvisual.zip    

    if zip in zips:        
        title = df_me.loc[df_me['RegionName']==zip, 'MsaName'].item()
        marl_low = df_melt[(df_melt['zip']==zip) & (df_melt['level']=='low')]
        marl_high = df_melt[(df_melt['zip']==zip) & (df_melt['level']=='high')]
        orig_vals = df_mew.loc[df_mew['zip']== zip, ['date','rent_forecast']]  

        fig = go.Figure()

        fig.add_trace(go.Scatter(name="Observed", 
                                x=list(orig_vals['date']), 
                                y=list(orig_vals['rent_forecast']),
            fill=None,
            mode='markers',
            line_color='red'))

        fig.add_trace(go.Scatter(name="Low Forecast", 
                                x=list(marl_low['month']), 
                                y=list(marl_low['rent_forecast']),
            fill=None,
            mode='lines',
            line_color='green'))

        fig.add_trace(go.Scatter(name="High Forecast",
                                x=list(marl_high['month']), 
                                y=list(marl_high['rent_forecast']),
            fill='tonexty', 
            mode='lines', line_color='green'))  

        fig.update_layout({
            'autosize':False,
            'plot_bgcolor':'rgba(2,0,0,5)',
            'paper_bgcolor':'rgba(2,0,0,5)',
            'font_color':"white",
            'title': f'Region name: {title}',
            'yaxis_title': 'Rent ($)',
            'xaxis_title': 'Date'
            })

        fig.update_yaxes(automargin = True, gridcolor = "gray")
        fig.update_xaxes(automargin = True, gridcolor = "gray")

        return fig.to_json() 

    else:
        return {"message":"No data for this location"}


