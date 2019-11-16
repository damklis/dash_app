import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt
from dash.dependencies import Input, Output
import plotly.graph_objs as go

def fill_win_ratio_tab_with_content(df):
    """
    Returns well-formatted content of win-ratio table => WIN-RATIO TAB.

    """
    return html.Div([
            dcc.Graph(id="win-ratio",
                    figure = {
                    "data":[
                        go.Table(
                        columnwidth=[0.20, 0.20, 0.27, 0.23, 0.23, 0.35, 0.4, 0.30, 0.30, 0.30],
                        header=dict(
                            values=["diff_level", "board_id", "total_games", "wins", "loss", "moves_left",
                                    "median_attempt", "win_ratio", "std_err", "randomness"],
                            font=dict(size=15),
                            line = dict(color="#7D7F80"),
                            align = "center",
                            fill = dict(color="rgb(249, 105, 79)"),
                            ),
                        cells=dict(
                            values=[df[k].to_list() for k in df[["diff_level", "board_id", "total_games",
                                                                 "wins", "loss", "moves_left",
                                                                 "median_attempt", "win_ratio",
                                                                 "std_err", "randomness"]]],
                            line = dict(color= "#7D7F80"),
                            align = "center",
                            fill = dict(color=["#247ec9","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa"]),
                            font = dict(color = ["white","black","black","black","black", "black","black"], size = 11))
                        )
                    ],
                    "layout":
                        go.Layout(
                        height=1000,
                        autosize=True,
                        margin = dict(t=50),
                        showlegend=False)}
                )
        ])

def fill_drop_rate_tab_with_content(df):
    """
    Returns well-formatted content of drop-rate table => DROP-RATE TAB.

    """
    return html.Div([
            dcc.Graph(id="drop-rate",
                    figure = {
                    "data":[
                        go.Table(
                        columnwidth=[0.3, 0.4, 0.5, 0.5, 0.5, 0.5],
                        header=dict(
                            values=["diff_level", "board_id", "total_users", "drop_rate", "stay_rate", "diff"],
                            font=dict(size=15),
                            line = dict(color="#7D7F80"),
                            align = "center",
                            fill = dict(color="rgb(249, 105, 79)"),
                            ),
                        cells=dict(
                            values=[df[k].to_list() for k in df[["diff_level", "board_id", "total_users", "drop_rate", "stay_rate", "diff"]]],
                            line = dict(color= "#7D7F80"),
                            align = "center",
                            fill = dict(color=["#247ec9","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa"]),
                            font = dict(color = ["white","black","black","black","black", "black"], size = 11))
                        )
                    ],
                    "layout":
                        go.Layout(
                        height=1000,
                        autosize=True,
                        margin = dict(t=50),
                        showlegend=False)}
                )
        ])

def fill_funnel_with_content(df,df2, app_version, app_version_2):
    """
    Returns well-formatted content of funnel charts => FUNNEL TAB.

    """
    return html.Div([
            dcc.Graph(id="funnel",
                    figure = {
                    "data":[
                        go.Bar(
                        x=df["step"],
                        y=df["unique_users"],
                        name="Version: " + app_version,
                        marker=dict(
                            color="rgb(49,130,189)"
                            )
                        ),
                        go.Scatter(
                        x=df2["step"],
                        y=df2["unique_users"],
                        mode = "lines+markers",
                        name="Version: " + app_version_2,
                        marker=dict(
                            color="rgb(249,105,79)"
                            )
                        )
                    ],
                    "layout":
                        go.Layout(
                        title="INTRO FUNNEL - PERCENT OF UNIQUE USERS ON A GIVEN TUTORIAL STEP",
                        autosize=True,
                        height=500,
                        showlegend=True,
                        yaxis={"title": "Percent of unique users",
                               "titlefont": {"color": "grey"}}
                        )
                        }
                ),
            dcc.Graph(id="funnel_abs",
                    figure = {
                    "data":[
                        go.Bar(
                        x=df["step"],
                        y=df["total_users"],
                        name="Version: " + app_version,
                        marker=dict(
                            color="rgb(249, 105, 79)"
                            )
                        ),
                        go.Scatter(
                        x=df2["step"],
                        y=df2["total_users"],
                        mode = "lines+markers",
                        name="Version: " + app_version_2,
                        marker=dict(
                            color="rgb(49,130,189)"
                            )
                        )

                    ],
                    "layout":
                        go.Layout(
                        title="INTRO FUNNEL - TOTAL OF UNIQUE USERS ON A GIVEN TUTORIAL STEP",
                        autosize=True,
                        height=500,
                        yaxis={"title": "Total number of unique users",
                               "titlefont": {"color": "grey"}}
                        )
                    }
                )
        ])

def fill_sessions_with_content(mean, median, df):
    """
    Returns well-formatted content of sessions charts => SESSIONS TAB.

    """

    return html.Div([
            html.Div(
                [html.Div(
                    [html.H4("Global session median : {} in minutes".format(median))],
                         style={"width": "25%",
                                "margin": "50px",
                                "background-color": "#f9f9f9",
                                "border-radius": "5px",
                                "padding": "17px",
                                "text-align": "center",
                                "position": "relative",
                                "box-shadow": "1px 1px 1px lightgrey"}),
                 html.Div(
                    [html.H4("Global session mean : {} in minutes".format(mean))],
                         style={"width": "25%",
                                "margin": "50px",
                                "background-color": "#f9f9f9",
                                "border-radius": "5px",
                                "padding": "17px",
                                "text-align": "center",
                                "position": "relative",
                                "box-shadow": "1px 1px 1px lightgrey"})
            ], style={"width": "25%", "display": "inline-block", "vertical-align": "baseline"}),
            html.Div([dcc.Graph(id="session_graph",
                        figure = {
                        "data":[
                            go.Bar(
                            x=[x for x in df["session"]],
                            y=[x for x in df["drop"]],
                            marker=dict(
                                color="rgb(49,130,189)"
                                )
                            )
                        ],
                        "layout":
                            go.Layout(
                            title="PERCENTAGE OF USERS DURING GIVEN SESSION",
                            width=1300,
                            height=600,
                            yaxis={"title": "Percent of unique users",
                                "titlefont": {"color": "grey"}},
                            xaxis={"title": "Session",
                                "titlefont": {"color": "grey"}}
                            )
                        }
                    )
            ], style={"width": "70%", "display": "inline-block", "float":"none","vertical-align": "top"})
        ])

def fill_economy_tab_with_content(df, df2, resource, data):
    """
    Returns well-formatted content of economy table => TAB ECONOMY.

    """
    
    selected_dataframe = {"df": df, "df2": df2}

    return html.Div([
            html.Div([dcc.Graph(id="economy_chart",
                        figure = {
                        "data":[
                            go.Bar(
                            x=selected_dataframe[data]["level"],
                            y=selected_dataframe[data][resource],
                            marker=dict(
                                color="rgb(49,130,189)"
                                )
                            )
                        ],
                        "layout":
                            go.Layout(
                            title="AMOUNT OF RESOURCE ON A GIVEN LEVEL / BOARD_ID",
                            autosize=True,
                            yaxis={"title": "Median amount of resource",
                                   "titlefont": {"color": "grey"}},
                            xaxis={"title": "Level / Board_id",
                                   "titlefont": {"color": "grey"},
                                   "type": "category",
                                   "tickmode" : "array",
                                   "tickvals" : [level for level in selected_dataframe[data]["level"][::35]]}
                            )
                        }
                    )], style={"width": "99%", "vertical-align": "top"}
                ),
            html.Hr(),
            html.Div([
                html.Div([
                    dcc.Graph(id="economy",
                            figure = {
                            "data":[
                                go.Table(
                                columnwidth=[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                header=dict(
                                    values=["level", "sc", "energy", "stars", "keys", "hc"],
                                    font=dict(size=15),
                                    line = dict(color="#7D7F80"),
                                    align = "center",
                                    fill = dict(color="rgb(249, 105, 79)"),
                                    ),
                                cells=dict(
                                    values=[df[k].to_list() for k in df[["level", "sc", "energy", "stars", "keys", "hc"]]],
                                    line = dict(color= "#7D7F80"),
                                    align = "center",
                                    fill = dict(color=["#247ec9","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa"]),
                                    font = dict(color = ["white","black","black","black","black", "black"], size = 11))
                                )
                            ],
                            "layout":
                                go.Layout(
                                height=600,
                                width=900,
                                title="Resources after winning a following level (ranked levels)",
                                autosize=False,
                                margin = dict(t=30),
                                showlegend=False)}
                            )
                ], style={"width": "49%", "display": "inline-block"}),
                html.Div([
                    dcc.Graph(id="economy_2",
                            figure = {
                            "data":[
                                go.Table(
                                columnwidth=[0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                                header=dict(
                                    values=["level", "sc", "energy", "stars", "keys", "hc"],
                                    font=dict(size=15),
                                    line = dict(color="#7D7F80"),
                                    align = "center",
                                    fill = dict(color="rgb(249, 105, 79)"),
                                    ),
                                cells=dict(
                                    values=[df2[k].to_list() for k in df2[["level", "sc", "energy", "stars", "keys", "hc"]]],
                                    line = dict(color= "#7D7F80"),
                                    align = "center",
                                    fill = dict(color=["#247ec9","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa","#f5f5fa"]),
                                    font = dict(color = ["white","black","black","black","black", "black"], size = 11))
                                )
                            ],
                            "layout":
                                go.Layout(
                                height=600,
                                width=900,
                                title="Resources after winning a specific level (board_id)",
                                autosize=False,
                                margin = dict(t=30),
                                showlegend=False)}
                            )
                ], style={"width": "50%", "display": "inline-block", "float": "right"})
            ])
        ])
