from textwrap import dedent as d
import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from factory.containers.events_container import EventsContainer
from factory.content_factory import ContentFactory
from content.app_content import (fill_drop_rate_tab_with_content, fill_economy_tab_with_content,
fill_funnel_with_content, fill_sessions_with_content, fill_win_ratio_tab_with_content) 
import base64
import urllib
import io
import datetime
from common.app_settings import Tabs, StyleSheets
import json

TODAY_DATE = str(datetime.date.today()).replace("-","_")

## Reading logo.
logo_filename = "../dashboard/assets/gamemetricslogo.png"
encoded_logo = base64.b64encode(open(logo_filename, "rb").read())

## Importing data.
win_lose_events = pd.read_pickle(path="../dataprovider/datasets/query_win_ratio.pkl")
drop_rate_events = pd.read_pickle(path="../dataprovider/datasets/query_drop_rate.pkl")
funnel_events = pd.read_pickle(path="../dataprovider/datasets/query_funnel.pkl")
session_events = pd.read_pickle(path="../dataprovider/datasets/query_session.pkl")
economy_events = pd.read_pickle(path="../dataprovider/datasets/query_economy.pkl")
economy_events_2 = pd.read_pickle(path="../dataprovider/datasets/query_economy_2.pkl")

## Creating events container with all data.
events = EventsContainer(
    win_lose_events, drop_rate_events, funnel_events,
    session_events, economy_events, economy_events_2
)

## Extracting last 2 versions of application.
first_version, second_version = events.get_n_last_versions(2)

## Defining level bundle option.
all_options = {
    first_version : list(
        win_lose_events[win_lose_events["app_version"] == first_version]["levels_bundle"].unique()
        ),
    second_version : list(
        win_lose_events[win_lose_events["app_version"] == second_version]["levels_bundle"].unique()
        )
    }

## App"s configuration.
app = dash.Dash(__name__, external_stylesheets=StyleSheets.external_stylesheets)
app.title = "Metrics"
app.config.suppress_callback_exceptions = True

## App"s main layout.
app.layout = html.Div([
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(className="row", children=[
        html.Div([
            dcc.Markdown(d("""
                **Choose App version:**
            """)),
            html.Div([dcc.RadioItems(
                            id="app-version",
                            options=[
                                {"label": "Version {}".format(str(first_version)),
                                    "value": first_version},
                                {"label": "Version {}".format(str(second_version)),
                                    "value": second_version}
                            ],
                            value=first_version,
                            labelStyle={"display": "inline-block", "vertical-align": "top"}
                            )], style={"width": "95%", "display": "inline-block", "margin-top": "10px"} )
        ], className="three columns"),

        html.Div([
            dcc.Markdown(d("""
                **Choose levels bundle:**
            """)),
        html.Div([dcc.Dropdown(
                    id="levels-boundle",
                    multi=True,
                    clearable=False,
                    )], style={"width": "75%", "horizontal-align": "center"}),
        ], className="three columns"),

        html.Div([
            dcc.Markdown(d("""
                **Download Full Report:**
            """)),
        html.Div([html.A("App Report {}".format(TODAY_DATE.replace("_", "-")),
                            id="download-link",
                            download="",
                            href="",
                            target="_blank")
                    ], style={"width": "75%",
                              "display": "inline-block",
                              "text-align": "center",
                              "color": "#f9f9f9",
                              "border-radius": "4px",
                              "padding": "5.5px",
                              "background-color": "#f9f9f9",
                              "vertical-align": "baseline",
                              "box-shadow": "1px 1px 1px lightgrey"}),
        ], className="three columns"),

        html.Div([
            html.Img(id="display-image",
                     src="data:image/png;base64,{}".format(encoded_logo.decode()),
                     height=60,
                     width=230),
        ], style={"float": "right", "margin-top": "8px", "margin-right": "50px"})
    ]),
    html.Div([html.Hr(),
                dcc.Tabs(id="tabs-styled-with-inline", value="tab-1", children=[
                    dcc.Tab(label="FUNNEL", value="tab-1", style=Tabs.tab_style, selected_style=Tabs.tab_selected_style),
                    dcc.Tab(label="WIN-RATIO", value="tab-2", style=Tabs.tab_style, selected_style=Tabs.tab_selected_style, children=[
                        html.P(),
                        html.Div([
                            dcc.Dropdown(
                                id="diff-levels-win-ratio",
                                options=[
                                    {"label": "Diff_level: Normal", "value": "normal"},
                                    {"label": "Diff_level: Challenging", "value": "challenging"},
                                    {"label": "Diff_level: Expert", "value": "expert"}
                                ],
                                value=["normal", "challenging", "expert"],
                                multi=True
                                ),
                            ] , style={"width": "40%", "display": "inline-block", "vertical-align": "middle"}
                        ),
                        html.Div([
                            dcc.Checklist(
                                id="randomness-id",
                                options=[
                                    {"label": "low", "value": "low"},
                                    {"label": "medium", "value": "medium"},
                                    {"label": "high", "value": "high"}
                                ],
                                value=["low", "medium", "high"],
                                labelStyle={"display": "inline-block", "vertical-align": "bottom"}
                            ),
                            ], style={"width": "15%", "height":"80%", "display": "inline-block", "vertical-align": "bottom", "float": "right"}),
                    ]),
                    dcc.Tab(label="DROP-RATE", value="tab-3", style=Tabs.tab_style, selected_style=Tabs.tab_selected_style, children=[
                        html.P(),
                        html.Div([
                            html.Div([dcc.Dropdown(
                                id="diff-levels-drop-rate",
                                options=[
                                    {"label": "Diff_level: Normal", "value": "normal"},
                                    {"label": "Diff_level: Challenging", "value": "challenging"},
                                    {"label": "Diff_level: Expert", "value": "expert"}
                                ],
                                value=["normal", "challenging", "expert"],
                                multi=True
                                    )]
                                ),
                            ]
                        )
                    ]),
                    dcc.Tab(label="SESSIONS", value="tab-4", style=Tabs.tab_style, selected_style=Tabs.tab_selected_style),
                    dcc.Tab(label="ECONOMY", value="tab-5", style=Tabs.tab_style, selected_style=Tabs.tab_selected_style, children=[
                        html.P(),
                        html.Div([
                            html.Div([dcc.Dropdown(
                                id="economy-dropdown",
                                options=[
                                    {"label": "Soft Currency", "value": "sc"},
                                    {"label": "Hard Currency", "value": "hc"},
                                    {"label": "Stars", "value": "stars"},
                                    {"label": "Keys", "value": "keys"},
                                    {"label": "Energy", "value": "energy"}
                                ],
                                value="energy",
                                multi=False
                                    )], style={"width": "15%", "height":"80%", "display": "inline-block", "vertical-align": "bottom", "float": "right"}
                                ),
                            html.Div([dcc.RadioItems(
                                id="economy-radioitems",
                                options=[
                                    {"label": "Chart with ranked levels", "value": "df"},
                                    {"label": "Chart with board_id levels", "value": "df2"}
                                ],
                                value="df",
                                labelStyle={"display": "inline-block", "vertical-align": "bottom"}
                                    )], style={"width": "45%", "height":"80%", "display": "inline-block", "vertical-align": "bottom", "float": "left"}
                                )
                            ]
                        )
                    ])
            ], style=Tabs.tabs_styles),
    html.Div(id="tabs-content-inline")])
])

## Clickable elements on dasboard.
@app.callback(
    Output("levels-boundle", "options"),
    [Input("app-version", "value")])
def set_levels_bundle_options(app_version):
    return [{"label": i, "value": i} for i in all_options[app_version]]

@app.callback(
    Output("levels-boundle", "value"),
    [Input("levels-boundle", "options")])
def set_levels_bundle_values(available_options):
    return [i["value"] for i in available_options]

@app.callback(
    Output('intermediate-value', 'children'),
    [Input("app-version", "value"),
     Input("diff-levels-win-ratio", "value"),
     Input("diff-levels-drop-rate", "value"),
     Input("randomness-id", "value"),
     Input("economy-dropdown", "value"),
     Input("economy-radioitems", "value"),
     Input("levels-boundle", "value")])
def generate_data(app_version, diff_lvl_wr, diff_lvl_dr,
    randomness_label, resource, df_data, lvls):

    cf = ContentFactory(events, app_version, diff_lvl_dr,
        diff_lvl_wr, randomness_label, resource, df_data, lvls)

    data = {
        'droprate_df': cf.drop_rate_df.to_json(orient='split'),
        'winratio_df': cf.win_ratio_df.to_json(orient='split'),
        'funnel_df': cf.funnel_df.to_json(orient='split'),
        'funnel2_df': cf.funnel_2_df.to_json(orient='split'),
        'economy_df': cf.economy_df.to_json(orient='split'),
        'economy2_df': cf.economy_2_df.to_json(orient='split'),
        'resource': cf.resource,
        'data': cf.df_data,
        'app_v1': cf.app_version,
        'app_v2': cf.app_version_2,
        'sessm' : cf.session_stats[0],
        'sessmd' : cf.session_stats[1],
        'sessions' : cf.session_stats[2].to_json(orient='split')
     }

    return json.dumps(data)


@app.callback(
    Output("tabs-content-inline", "children"),
    [Input("tabs-styled-with-inline", "value"),
     Input('intermediate-value', 'children')])
def render_content(tab, cached_json_data):
    """
    This is main function that aggregates data 
    and creates all interactions on dashboard.
    """
    data = json.loads(cached_json_data)
    droprate = pd.read_json(data['droprate_df'], orient='split')
    winratio = pd.read_json(data['winratio_df'], orient='split')
    funnel1 = pd.read_json(data['funnel_df'], orient='split')
    funnel2 = pd.read_json(data['funnel2_df'], orient='split')
    economy = pd.read_json(data['economy_df'], orient='split')
    economy2 = pd.read_json(data['economy2_df'], orient='split')
    sessions = pd.read_json(data['sessions'], orient='split')

    ### Creating tabs filled with content.
    if tab == "tab-1":
        return fill_funnel_with_content(funnel1, funnel2, data['app_v1'], data['app_v2'])
    elif tab == "tab-2":
        return fill_win_ratio_tab_with_content(winratio)
    elif tab == "tab-3":
        return fill_drop_rate_tab_with_content(droprate)
    elif tab == "tab-4":
        return fill_sessions_with_content(data['sessm'], data['sessmd'], sessions)
    elif tab == "tab-5":
        return fill_economy_tab_with_content(economy, economy2, data['resource'], data['data'])

@app.callback([Output("download-link", "href"),
               Output("download-link", "download")],
              [Input("app-version", "value"),
               Input('intermediate-value', 'children')])
def download_excel_report(app_version, cached_json_data):
    """
    Returns formattd Excel"s file ready to download.
    """
    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine="xlsxwriter")

    data = json.loads(cached_json_data)
    tables = {
        k:pd.read_json(v, orient='split')
        for k,v in data.items() if k.endswith('_df')
         }

    for table_name, df in tables.items():
        df.to_excel(writer, sheet_name=table_name, index=False)
        worksheet = writer.sheets[table_name]
        worksheet.set_column(0, 15, 20)
    writer.save()
    xlsx_io.seek(0)
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    data = f"data:{media_type};base64,{data}"
    file_name = f"App_report_{TODAY_DATE}.xlsx"
    return data, file_name


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")