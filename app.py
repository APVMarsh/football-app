import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

external_stylesheets = ['/assets/stylesheet.css', dbc.themes.BOOTSTRAP]
mapbox_access_token = open('.mapbox_token').read()
df1 = pd.read_excel('All_Teams_Coordinates.xlsx', sheet_name=None)
df1_all = df1['All'].set_index('Team')
df2 = pd.read_excel('All_Team_Data.xlsx', sheet_name=None)
df3 = pd.read_csv('All_Matches_Data.csv')

LOGO = "/assets/Logo.png"

navbar = dbc.Navbar(
    [
        html.Div(
            dbc.Row(
                children=[
                    dbc.Col(html.Img(src=LOGO, height="35px")),
                    dbc.Col(dbc.NavbarBrand(
                        "Historical Football League Data", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
        ),
        dbc.DropdownMenu(
            label="Sources",
            children=[
                dbc.DropdownMenuItem(
                    "Match Data", href='https://www.enfa.co.uk/'),
                dbc.DropdownMenuItem(
                    "Season Data",
                    href='https://github.com/jalapic/engsoccerdata'),
                ],
            style=dict(
                marginBottom='0px', height='35px',
                listStyleType='none', color='white'),
            className='ml-auto',
            nav=True,
            in_navbar=True,
        ),
        dbc.DropdownMenu(
            label="Contact",
            children=[
                dbc.DropdownMenuItem("Email: emailaddress@gmail.com"),
                ],
            style=dict(
                marginBottom='0px', height='35px', listStyleType='none',
                color='white', left='auto', right='0', marginRight='-10px',
                textTransform='none'),
            nav=True,
            in_navbar=True,
        ),
    ],
    color="dark",
    dark=True,
)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div(navbar),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="three columns",
                children=[
                    dcc.Graph(
                        id='Map',
                        config=dict(displayModeBar=False,),
                    ),
                    dcc.Dropdown(
                        id='L-NL-D-option',
                        options=[
                            {'label': 'All', 'value': 'All'},
                            {'label': 'League', 'value': 'League'},
                            {'label': 'Non-League', 'value': 'Non-League'},
                            {'label': 'Defunct', 'value': 'Defunct'}
                        ],
                        value='All',
                        style=dict(color='white',),
                    ),
                    html.Div(
                        id='chosen-team',
                        children='Pick a team',
                        style=dict(
                            fontSize=24,
                            textAlign='center',
                            paddingTop='77px',
                            paddingBottom='77px',),
                    ),
                    html.Div(
                        id='team-info',
                        style=dict(
                            textAlign='center',
                            fontSize=12,
                            whiteSpace='pre-wrap'),
                    ),
                    dcc.Graph(
                        id='line',
                        config=dict(displayModeBar=False)
                    ),
                    html.A(id='chosen-team-wiki',
                           children="Team Wiki",
                           href='https://plot.ly',
                           target="_blank",
                           className='five columns',
                           style=dict(
                               float='left', textAlign='left', color='#343a40',
                               fontStyle='italic', fontSize=13),
                    ),
                    html.A(id='chosen-team-website',
                           children="Team Website",
                           href='https://plot.ly',
                           target="_blank",
                           className='five columns',
                           style=dict(
                               float='right', textAlign='right',
                               color='#343a40', fontStyle='italic',
                               fontSize=13),
                    ),
                ], style=dict(padding = '8px 8px 8px 8px')
            ),
            html.Div(
                className="four columns",
                children=[
                    dcc.Graph(
                        id='team-pos',
                        config=dict(displayModeBar=False,),
                    ),
                    dcc.Graph(
                        id='team-WDL',
                        config=dict(displayModeBar=False,),
                    ),
                    dcc.Graph(
                        id='team-GD',
                        config=dict(displayModeBar=False,),
                    ),
                    dcc.Dropdown(
                        id='tot-pos-dropdown',
                        options=[
                            {'label': 'League Position',
                             'value': 'League Position'},
                            {'label': 'Points', 'value': 'Points'},
                            {'label': 'Points %', 'value': 'Points %'},
                            {'label': 'Home & Away Points',
                             'value': 'Home & Away Points'},
                            {'label': 'Home & Away Points %',
                             'value': 'Home & Away Points %'},
                        ],
                        value='League Position',
                        style=dict(color='white',),
                    ),
                    dcc.Dropdown(
                        id='WDL-graph-dropdown',
                        options=[
                            {'label': 'All', 'value': 'All'},
                            {'label': 'Home', 'value': 'Home'},
                            {'label': 'Away', 'value': 'Away'},
                            {'label': 'Home & Away', 'value': 'Home & Away'}
                        ],
                        value='All',
                        style=dict(color='white',),
                    ),
                    dcc.Dropdown(
                        id='GD-graph-dropdown',
                        options=[
                            {'label': 'All', 'value': 'All'},
                            {'label': 'Home', 'value': 'Home'},
                            {'label': 'Away', 'value': 'Away'},
                            {'label': 'Home & Away', 'value': 'Home & Away'}
                        ],
                        value='All',
                        style=dict(color='white',),
                    ),
                ], style=dict(padding = '8px 8px 8px 0px')
            ),
            html.Div(
                className="two columns",
                children=[
                    dcc.Graph(
                        id='pts-pie',
                        config=dict(displayModeBar=False),
                        style=dict(padding = '18px, 8px, 28px, 20px')
                    ),
                    dcc.Graph(
                        id='wdl-pie',
                        config=dict(displayModeBar=False),
                        style=dict(padding = '18px, 8px, 28px, 20px')
                    ),
                    dcc.Graph(
                        id='gd-pie',
                        config=dict(displayModeBar=False),
                        style=dict(padding = '18px, 8px, 8px, 0px')
                    ),
                    html.Div(id='range-dates',
                             children="1889/90 - 2018/19",
                             style=dict(
                                textAlign='center', color='white', fontSize=13,
                                padding = '0px 8px 8px 8px'),
                    ),
                    dcc.RangeSlider(
                        id='range-slider-all-pies',
                        min=0,
                        max=130,
                        step=1,
                        value=[0, 130],
                        disabled=True,
                        allowCross=False,
                        marks={
                            0: {'label': '1889/89',
                            'style': {'color': 'white'}},
                            65: {'label':'1953/54',
                            'style': {'color': 'white'}},
                            130: {'label':'2018/19',
                            'style': {'color': 'white'}},
                        },
                    ),
                ], style=dict(padding = '8px 8px 8px 0px'),
            ),
            html.Div(
                className="four columns",
                children=[
                    html.Div(id='team-name-vs',
                            className="five columns",
                            children="Team",
                            style=dict(
                                textAlign='center', color='white',
                                padding = '5px 0px 5px 0px',
                                height='34px', width='200px',
                            )
                    ),
                    html.Div(id='vs',
                            className="one columns",
                            children="vs",
                            style=dict(
                                textAlign='center', color='white',
                                padding = '5px 0px 5px 0px', height='34px',
                            )
                    ),
                    dcc.Dropdown(
                        id='versus-team-dropdown',
                        className="six columns",
                        options=[
                            {'label': '', 'value': ''}
                        ],
                        value=None,
                        disabled=True,
                        placeholder='Pick an opposition team',
                        style=dict(color='white', height='35px',
                        ),
                    ),
                    dcc.Graph(
                        id='line-opposition',
                        config=dict(displayModeBar=False,)
                    ),
                    html.Div(id='opposition-games-bar-title',
                            children="Games Played: N/A",
                            style=dict(
                                textAlign='center', fontSize=13, color='white',
                                padding = '5px 0px 2px 0px',
                            )
                    ),
                    dcc.Graph(
                        id='opposition-pies',
                        className='four columns',
                        config=dict(displayModeBar=False),
                        style=dict(float='left', padding='0px 0px 5px 0px'),
                    ),
                    dcc.Graph(
                        id='opposition-tot-pos',
                        className='eight columns',
                        config=dict(displayModeBar=False),
                        style=dict(float='center', padding='0px 0px 5px 0px'),
                    ),
                    html.Div(id='biggest-win',
                        className='four columns',
                             children="Biggest Win:\nN/A",
                             style=dict(
                                textAlign='center', color='white', fontSize=13,
                                whiteSpace='pre-wrap', width='33%',
                                padding='0px 0px 10px 0px', height='60px',
                             )
                    ),
                    html.Div(id='biggest-loss',
                        className='four columns',
                             children="Biggest Loss:\nN/A",
                             style=dict(
                                textAlign='center', color='white', fontSize=13,
                                whiteSpace='pre-wrap', width='33%',
                                padding='0px 0px 10px 0px', height='60px',
                             )
                    ),
                    html.Div(id='most-goals',
                        className='four columns',
                             children="Most Goals:\nN/A",
                             style=dict(
                                textAlign='center', color='white', fontSize=13,
                                whiteSpace='pre-wrap', width='33%',
                                padding='0px 0px 10px 0px', height='60px',
                             )
                    ),
                    dcc.Graph(
                        className='twelve columns',
                        id='matches-table',
                        config=dict(displayModeBar=False),
                        style=dict(padding='0px 0px 0px 0px')
                    ),
                ], style=dict(padding = '8px 8px 8px 0px')
            ),
        ],
    ),
])

@app.callback(
    [Output('biggest-win', 'children'),
     Output('biggest-loss', 'children'),
     Output('most-goals', 'children'),],
    [Input('Map', 'clickData'),
     Input('versus-team-dropdown', 'value'),])
def update_output(chosen_team, chosen_opposition):
    biggest_win = """Biggest Win:\nN/A"""
    biggest_loss = """Biggest Loss:\nN/A"""
    most_goals = """Most Goals:\nN/A"""

    if chosen_opposition == None:
        pass
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        team_name = team
        versus_name = chosen_opposition

        df3_team = df3.loc[((df3['home'] == team_name) | (df3['visitor'] == team_name))
                            & ((df3['home'] == versus_name) | (df3['visitor'] == versus_name))].copy()

        if len(df3_team['Season']) == 0:
            pass
        else:
            df3_team.insert(13, "WDL", None, True)
            df3_team.insert(14, "GF", None, True,)
            df3_team.insert(15, "zeros", '1', True)
            df3_team.insert(16, "diff", '0', True)
            df3_team.insert(17, "HA", 'H', True)

            df3_team.loc[((df3_team.result == 'H') & (df3.home == team_name)), 'WDL'] = 'W'
            df3_team.loc[((df3_team.result == 'A') & (df3.home == team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'H') & (df3.home != team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'A') & (df3.home != team_name)), 'WDL'] = 'W'
            df3_team.loc[df3_team.result == 'D', 'WDL'] = 'D'
            df3_team.loc[(df3_team.home != team_name), 'HA'] = 'A'
            df3_team.loc[(df3_team.home == team_name), 'GF'] = df3_team['hgoal']
            df3_team.loc[(df3_team.visitor == team_name), 'GF'] = df3_team['vgoal']
            df3_team.loc[(df3_team.home != team_name), 'GA'] = df3_team['hgoal']
            df3_team.loc[(df3_team.visitor != team_name), 'GA'] = df3_team['vgoal']
            df3_team.loc[(df3_team.home == team_name), 'diff'] = (df3_team['hgoal'] - df3_team['vgoal'])
            df3_team.loc[(df3_team.home != team_name), 'diff'] = (df3_team['vgoal'] - df3_team['hgoal'])

            df3_team.insert(17, "totgoals", (df3_team['GF'] + df3_team['GA']), True)

            df3_team_wins = df3_team.loc[(df3_team['WDL'] == 'W')].copy()
            df3_team_draws = df3_team.loc[(df3_team['WDL'] == 'D')].copy()
            df3_team_losses = df3_team.loc[(df3_team['WDL'] == 'L')].copy()

            max_diff = df3_team_wins['diff'].max()
            df_2 = df3_team_wins.loc[df3_team_wins['diff'] == max_diff]

            if max_diff <= 0:
                pass
            elif len(df_2['FT']) == 1:
                biggest_win = 'Biggest Win:\n%s (%s, %s)' % ((df_2.reset_index()).at[0, 'FT'], (df_2.reset_index()).at[0, 'result'], (df_2.reset_index()).at[0, 'Season'])
            else:
                max_goals = df_2['GF'].max()
                df_3 = df_2.loc[df_2['GF'] == max_goals]

                if len(df_3['FT']) == 1:
                    biggest_win = 'Biggest Win:\n%s (%s, %s)' % ((df_3.reset_index()).at[0, 'FT'], (df_3.reset_index()).at[0, 'result'], (df_3.reset_index()).at[0, 'Season'])
                else:
                    biggest_win_years_list = []
                    for result, season in zip(df_3['result'], df_3['Season']):
                        biggest_win_years_list.append('(%s, %s)' % (result, season))
                        biggest_win_years = ', '.join(map(str, biggest_win_years_list))
                        biggest_win = 'Biggest Win:\n%s %s' % ((df_3.reset_index()).at[0, 'FT'], biggest_win_years)

            max_diff = df3_team_losses['diff'].min()
            df_2 = df3_team_losses.loc[df3_team_losses['diff'] == max_diff]

            if max_diff >= 0:
                pass
            elif len(df_2['FT']) == 1:
                biggest_loss = 'Biggest Loss:\n%s (%s, %s)' % ((df_2.reset_index()).at[0, 'FT'], (df_2.reset_index()).at[0, 'result'], (df_2.reset_index()).at[0, 'Season'])
            else:
                max_goals = df_2['GA'].max()
                df_3 = df_2.loc[df_2['GA'] == max_goals]

                if len(df_3['FT']) == 1:
                    biggest_loss = 'Biggest Loss:\n%s (%s, %s)' % ((df_3.reset_index()).at[0, 'FT'], (df_3.reset_index()).at[0, 'result'], (df_3.reset_index()).at[0, 'Season'])
                else:
                    biggest_loss_years_list = []
                    for result, season in zip(df_3['result'], df_3['Season']):
                        biggest_loss_years_list.append('(%s, %s)' % (result, season))
                        biggest_loss_years = ', '.join(map(str, biggest_loss_years_list))
                        biggest_loss = 'Biggest Loss:\n%s %s' % ((df_3.reset_index()).at[0, 'FT'], biggest_loss_years)

            max_goals = df3_team['totgoals'].max()
            df_2 = df3_team.loc[df3_team['totgoals'] == max_goals]

            if len(df_2['FT']) == 1:
                most_goals = 'Most Goals:\n%s (%s, %s)' % ((df_2.reset_index()).at[0, 'FT'], (df_2.reset_index()).at[0, 'result'], (df_2.reset_index()).at[0, 'Season'])
            else:
                most_goals_list = []
                for ft, result, season in zip(df_2['FT'], df_2['result'], df_2['Season']):
                    most_goals_list.append('%s (%s, %s)' % (ft, result, season))
                    most_goals_list_all = ', '.join(map(str, most_goals_list))
                    most_goals = 'Most Goals:\n %s' % most_goals_list_all

    return biggest_win, biggest_loss, most_goals

@app.callback(
    Output('opposition-tot-pos', 'figure'),
    [Input('Map', 'clickData'),
     Input('versus-team-dropdown', 'value'),])
def update_output(chosen_team, chosen_opposition):

    dff2 = df2['Master']

    fig = go.Figure()

    fig = make_subplots(rows=2, cols=1, specs=[[{'type':'xy'}], [{'type':'bar'}]], row_width=[1, 10], vertical_spacing = 0)

    fig.add_trace(go.Scatter(
        name='team_trace',
        visible=False,
        ),
        row=1,
        col=1,)

    fig.add_trace(go.Scatter(
        line=dict(color='white'),
        x=dff2['Season'],
        y=dff2['Teams_in_Tier_1'],
        hoverinfo='none'
        ),
        row=1,
        col=1,)

    fig.add_trace(go.Scatter(
        line=dict(color='white'),
        x=dff2['Season'],
        y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
        hoverinfo='none'
        ),
        row=1,
        col=1,)

    fig.add_trace(go.Scatter(
        line=dict(color='white'),
        x=dff2['Season'],
        y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
        hoverinfo='none'
        ),
        row=1,
        col=1,)

    fig.add_trace(go.Scatter(
        line=dict(color='white'),
        x=dff2['Season'],
        y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
        hoverinfo='none'
        ),
        row=1,
        col=1,)

    fig.add_annotation(go.layout.Annotation(
                                        text = '1st Tier',
                                        font=dict(size=8),
                                        x = 122,
                                        y = 6.5,
                                        showarrow = False,
                                        valign = 'middle',),
                      row=1,
                      col=1,)

    fig.add_annotation(go.layout.Annotation(
                                        text = '2nd Tier',
                                        font=dict(size=8),
                                        x = 122,
                                        y = 26,
                                        showarrow = False,
                                        valign = 'middle',),
                      row=1,
                      col=1,)

    fig.add_annotation(go.layout.Annotation(
                                        text = '3rd Tier',
                                        font=dict(size=8),
                                        x = 122,
                                        y = 50,
                                        showarrow = False,
                                        valign = 'middle',),
                      row=1,
                      col=1,)

    fig.add_annotation(go.layout.Annotation(
                                        text = '4th Tier',
                                        font=dict(size=8),
                                        x = 122,
                                        y = 74,
                                        showarrow = False,
                                        valign = 'middle',),
                      row=1,
                      col=1,)

    fig.add_trace(go.Bar(
                    x = [1],
                    y= [1],
                    marker = dict(color='#111111',
                                  line=dict(color='#111111',
                                            width=0.75),),
                    ),
                row=2,
                col=1,
                )


    fig.update_layout(
        template='plotly_dark',
        showlegend=False,
        xaxis1 = dict(range = (-0.5, 130.5),
            fixedrange=True,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            ),
        yaxis1 = dict(
            zeroline=False,
            showgrid=False,
            range = (95.5, -0.5),
            tickmode = 'array',
            tickvals = [1, 20, 40, 60, 80],
            title=dict(text='Final League Position', font=dict(size=13), standoff=10),
            ),
        xaxis2=dict(
            fixedrange=True,
            type='date',
            range = ('1888-01-01', '2019-07-01'),
            zeroline=False,
            showgrid=False,
            mirror=False,
            ticks='',
            linecolor='#343a40',
            showline=True,
        ),
        yaxis2=dict(
            range = (0, 0.85),
            showticklabels=False,
            zeroline=False,
            showgrid=False,
        ),
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),
        height=180,
    )

    if chosen_opposition == None:
        pass

    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        team_name = team
        versus_name = chosen_opposition

        df3_team = df3.loc[((df3['home'] == team_name) | (df3['visitor'] == team_name))
                                    & ((df3['home'] == versus_name) | (df3['visitor'] == versus_name))].copy()
        if len(df3_team['Season']) == 0:
            pass
        else:
            df3_team.insert(13, "WDL", None, True)
            df3_team.insert(14, "GF", None, True,)
            df3_team.insert(15, "zeros", '1', True)
            df3_team.loc[((df3_team.result == 'H') & (df3.home == team_name)), 'WDL'] = 'W'
            df3_team.loc[((df3_team.result == 'A') & (df3.home == team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'H') & (df3.home != team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'A') & (df3.home != team_name)), 'WDL'] = 'W'
            df3_team.loc[df3_team.result == 'D', 'WDL'] = 'D'
            df3_team.loc[(df3.home == team_name), 'GF'] = df3_team['hgoal']
            df3_team.loc[(df3.visitor == team_name), 'GF'] = df3_team['vgoal']
            df3_team.loc[(df3.home != team_name), 'GA'] = df3_team['hgoal']
            df3_team.loc[(df3.visitor != team_name), 'GA'] = df3_team['vgoal']

            wins = (df3_team.WDL == 'W').sum(skipna=True)
            draws = (df3_team.WDL == 'D').sum(skipna=True)
            losses = (df3_team.WDL == 'L').sum(skipna=True)
            pld = wins + draws + losses

            gf = (df3_team['GF']).sum(skipna=True)
            ga = (df3_team['GA']).sum(skipna=True)
            allgoals = gf + ga

            df3_team_wins = df3_team.loc[(df3_team['WDL'] == 'W')].copy()
            df3_team_draws = df3_team.loc[(df3_team['WDL'] == 'D')].copy()
            df3_team_losses = df3_team.loc[(df3_team['WDL'] == 'L')].copy()

            zeros = df3_team['zeros']
            wins_date = df3_team_wins['Date']
            draws_date = df3_team_draws['Date']
            losses_date = df3_team_losses['Date']

            if df1_all.at[team_name, 'colour'] == df1_all.at[versus_name, 'colour']:
                versus_color = df1_all.at[versus_name, 'colour_away']
            else:
                versus_color = df1_all.at[versus_name, 'colour']

            fig = go.Figure()

            fig = make_subplots(rows=2, cols=1, specs=[[{'type':'xy'}], [{'type':'bar'}]], row_width=[1, 10], vertical_spacing = 0)

            fig.add_trace(go.Scatter(
                name='team_trace',
                visible=False,
                showlegend=False,
                ),
                row=1,
                col=1,)

            fig.add_trace(go.Scatter(
                line=dict(color='white'),
                x=dff2['Season'],
                y=dff2['Teams_in_Tier_1'],
                hoverinfo='none',
                showlegend=False,
                ),
                row=1,
                col=1,)

            fig.add_trace(go.Scatter(
                line=dict(color='white'),
                x=dff2['Season'],
                y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
                hoverinfo='none',
                showlegend=False,
                ),
                row=1,
                col=1,)

            fig.add_trace(go.Scatter(
                line=dict(color='white'),
                x=dff2['Season'],
                y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
                hoverinfo='none',
                showlegend=False,
                ),
                row=1,
                col=1,)

            fig.add_trace(go.Scatter(
                line=dict(color='white'),
                x=dff2['Season'],
                y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
                hoverinfo='none',
                showlegend=False,
                ),
                row=1,
                col=1,)

            fig.add_trace(go.Scatter(
                name=versus_name,
                line=dict(color=versus_color),
                x=df2[versus_name]['Season'],
                y=df2[versus_name]['TotPos'],
                customdata=df2[versus_name]['Pos'],
                hovertemplate="Season: %{x}<br>" +
                      "League Position: %{customdata}<br>" +
                      "Full League Position: %{y}<br>" +
                      "<extra></extra>",
                showlegend=True,),
                row=1,
                col=1,)

            fig.add_trace(go.Scatter(
                name=team_name,
                line=dict(color=df1_all.at[team_name, 'colour']),
                x=df2[team_name]['Season'],
                y=df2[team_name]['TotPos'],
                customdata=df2[team_name]['Pos'],
                hovertemplate="Season: %{x}<br>" +
                      "League Position: %{customdata}<br>" +
                      "Full League Position: %{y}<br>" +
                      "<extra></extra>",
                showlegend=True,),
                row=1,
                col=1,)

            fig.add_annotation(go.layout.Annotation(
                                                text = '1st Tier',
                                                font=dict(size=8),
                                                x = 122,
                                                y = 6.5,
                                                showarrow = False,
                                                valign = 'middle',
                                                ),
                              row=1,
                              col=1,)

            fig.add_annotation(go.layout.Annotation(
                                                text = '2nd Tier',
                                                font=dict(size=8),
                                                x = 122,
                                                y = 26,
                                                showarrow = False,
                                                valign = 'middle',
                                                ),
                              row=1,
                              col=1,)

            fig.add_annotation(go.layout.Annotation(
                                                text = '3rd Tier',
                                                font=dict(size=8),
                                                x = 122,
                                                y = 50,
                                                showarrow = False,
                                                valign = 'middle',
                                                ),
                              row=1,
                              col=1,)

            fig.add_annotation(go.layout.Annotation(
                                                text = '4th Tier',
                                                font=dict(size=8),
                                                x = 122,
                                                y = 74,
                                                showarrow = False,
                                                valign = 'middle',
                                                ),
                              row=1,
                              col=1,)

            fig.add_trace(go.Bar(
                            x = wins_date,
                            y= zeros,
                            marker = dict(color='#56b36f',
                                          line=dict(color='#56b36f',
                                                    width=0.9),),
                            showlegend=False,),
                        row=2,
                        col=1,
                        )
            fig.add_trace(go.Bar(
                            x = draws_date,
                            y= zeros,
                            marker = dict(color='white',
                                          line=dict(color='white',
                                                    width=0.9),),
                            showlegend=False,),
                        row=2,
                        col=1,
                        )
            fig.add_trace(go.Bar(
                            x = losses_date,
                            y= zeros,
                            marker = dict(color='#eb5a4e',
                                          line=dict(color='#eb5a4e',
                                                    width=0.9),),
                            showlegend=False,),
                        row=2,
                        col=1,
                        )

            fig.update_layout(
                template='plotly_dark',
                showlegend=True,
                legend=dict(traceorder='reversed',
                            tracegroupgap=5,
                            font=dict(size=10),
                            x=0,
                            y=0.1),
                xaxis1 = dict(range = (-0.5, 130.5),
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    ),
                yaxis1 = dict(
                    zeroline=False,
                    showgrid=False,
                    range = (95.5, -0.5),
                    tickmode = 'array',
                    tickvals = [1, 20, 40, 60, 80],
                    title=dict(text='Final League Position', font=dict(size=13), standoff=10),
                    ),
                xaxis2=dict(
                    type='date',
                    range = ('1888-01-01', '2019-07-01'),
                    zeroline=False,
                    showgrid=False,
                    mirror=False,
                    ticks='',
                    linecolor='#343a40',
                    showline=True,
                ),
                yaxis2=dict(
                    range = (0, 0.8),
                    showticklabels=False,
                    zeroline=False,
                    showgrid=False,
                ),
                margin=dict(
                    l=0,
                    r=0,
                    t=0,
                    b=0,
                ),
                height=180,
            )

    return fig

@app.callback(
    Output('opposition-pies', 'figure'),
    [Input('Map', 'clickData'),
     Input('versus-team-dropdown', 'value'),])
def update_output(chosen_team, chosen_opposition):
    fig = go.Figure()

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16,
                        specs=[[{'type':'pie'}], [{'type':'pie'}]])

    fig.add_trace(go.Pie(
        ids=['A'],
        labels=[1],
        values=[1],
        marker=dict(colors=['#111111'],
                           line=dict(color='white',
                                     width=3,),
                ),
        hole=0.5,
        hoverinfo='none',
        textinfo='none',
            ),
            row=1,
            col=1,
        )

    fig.add_trace(go.Pie(
        ids=['B'],
        labels=[1],
        values=[1],
        marker=dict(colors=['#111111'],
                           line=dict(color='white',
                                     width=3,),
                ),
        hole=0.5,
        hoverinfo='none',
        textinfo='none',
            ),
            row=2,
            col=1,
        )

    fig.update_layout(
                showlegend=False,
                template='plotly_dark',
                margin = dict(t=20, l=0, r=0, b=2),
                height=180,
                annotations=[
                    dict(
                        text='Win / Draw / Loss',
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=1.14,
                        valign='middle',
                        showarrow=False,

                    ),
                    dict(
                        text='Goals For / Against',
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=0.50,
                        valign='middle',
                        showarrow=False,
                    ),
                ]),

    if chosen_opposition == None:
        pass
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        team_name = team
        versus_name = chosen_opposition

        df3_team = df3.loc[((df3['home'] == team_name) | (df3['visitor'] == team_name))
                            & ((df3['home'] == versus_name) | (df3['visitor'] == versus_name))].copy()

        if len(df3_team['Season']) == 0:
            pass
        else:
            df3_team.insert(13, "WDL", None, True)
            df3_team.insert(14, "GF", None, True,)

            df3_team.loc[((df3_team.result == 'H') & (df3.home == team_name)), 'WDL'] = 'W'
            df3_team.loc[((df3_team.result == 'A') & (df3.home == team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'H') & (df3.home != team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'A') & (df3.home != team_name)), 'WDL'] = 'W'
            df3_team.loc[df3_team.result == 'D', 'WDL'] = 'D'
            df3_team.loc[(df3.home == team_name), 'GF'] = df3_team['hgoal']
            df3_team.loc[(df3.visitor == team_name), 'GF'] = df3_team['vgoal']
            df3_team.loc[(df3.home != team_name), 'GA'] = df3_team['hgoal']
            df3_team.loc[(df3.visitor != team_name), 'GA'] = df3_team['vgoal']

            wins = (df3_team.WDL == 'W').sum(skipna=True)
            draws = (df3_team.WDL == 'D').sum(skipna=True)
            losses = (df3_team.WDL == 'L').sum(skipna=True)
            pld = wins + draws + losses

            gf = (df3_team['GF']).sum(skipna=True)
            ga = (df3_team['GA']).sum(skipna=True)
            allgoals = gf + ga

            fig = go.Figure()

            fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16,
                                specs=[[{'type':'pie'}], [{'type':'pie'}]])

            fig.add_trace(go.Pie(
                ids=['Win', 'Draw', 'Loss'],
                labels=['Win', 'Draw', 'Loss'],
                values=[wins, draws, losses],
                marker=dict(colors=['#56b36f', 'white', '#eb5a4e'],
                                   line=dict(color='#111111',
                                             width=3,),
                        ),
                textinfo='none',
                hole=0.5,
                hovertemplate= "%{label}: %{value:.0f}<br>" +
                               "%{label}%: %{percent}<br>" +
                               "<extra></extra>"
                    ),
                    row=1,
                    col=1,
                )

            fig.add_trace(go.Pie(
                ids=['Goals For', 'Goals Against'],
                labels=['Goals For', 'Goals Against'],
                values=[gf, ga],
                marker=dict(colors=['#56b36f', '#eb5a4e'],
                                   line=dict(color='#111111',
                                             width=3,),
                        ),
                hole=0.5,
                textinfo='none',
                hovertemplate= "%{label}: %{value:.0f}<br>" +
                               "<extra></extra>"
                    ),
                    row=2,
                    col=1,
                )

            fig.update_layout(
                        showlegend=False,
                        template='plotly_dark',
                        margin = dict(t=20, l=0, r=0, b=2),
                        height=180,
                        annotations=[
                            dict(
                                text='Win / Draw / Loss',
                                xref='paper',
                                yref='paper',
                                x=0.5,
                                y=1.14,
                                valign='middle',
                                showarrow=False,

                            ),
                            dict(
                                text='Goals For / Against',
                                xref='paper',
                                yref='paper',
                                x=0.5,
                                y=0.50,
                                valign='middle',
                                showarrow=False,
                            ),
                        ]),

    return fig

@app.callback(
    Output('line-opposition', 'figure'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    fig = go.Figure()

    fig.update_layout(
        margin=go.layout.Margin(
                l=0,
                r=0,
                b=4,
                t=0,
        ),
        xaxis=dict(range=(0, 0),
                       visible=False,
                       showgrid=False,
                       showticklabels=False,),
        yaxis=dict(range=(0, 0),
                      visible=False,
                      showgrid=False,
                      showticklabels=False,),
        height=10,
        plot_bgcolor='#111111',
        paper_bgcolor='white',
    )
    if chosen_team == None:
        pass
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')
        team_primary_color = df1_all.at[team, 'colour']

        fig.update_layout(
        paper_bgcolor=team_primary_color,
        )

    return fig

@app.callback(
    Output('opposition-games-bar-title', 'children'),
    [Input('Map', 'clickData'),
     Input('versus-team-dropdown', 'value'),])
def update_output(chosen_team, chosen_opposition):
    if chosen_opposition == None:
        return "Games Played: N/A"
    elif chosen_opposition != None:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        team_name = team
        versus_name = chosen_opposition

        df3_team = df3.loc[((df3['home'] == team_name) | (df3['visitor'] == team_name))
                            & ((df3['home'] == versus_name) | (df3['visitor'] == versus_name))].copy()

        games_played = len(df3_team['Season'])

        if games_played == None:
            games_played = '0'
        else:
            pass

        return 'Games Played: {}'.format(games_played)

@app.callback(
    Output('team-name-vs', 'children'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    if chosen_team == None:
        return "Team"
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        return '{}'.format(team)

@app.callback(
    [Output('versus-team-dropdown', 'options'),
    Output('versus-team-dropdown', 'disabled')],
    [Input('Map', 'clickData'),])
def update_output(chosen_team):
    if chosen_team == 'None':
        pass
    else:
        return [{'label': i, 'value': i} for i in df1['All']['Team']], False

@app.callback(
    Output('matches-table', 'figure'),
    [Input('Map', 'clickData'),
     Input('versus-team-dropdown', 'value')])
def update_output(chosen_team, chosen_opposition):

    fig = go.Figure()

    zeros = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']

    fig.add_trace(go.Table(
        header = dict(values = ['Date', 'Home', 'Away', 'Score', 'Tier'],
                      fill = dict(color = '#343a40')),
        cells = dict(values = [zeros, zeros, zeros, zeros, zeros],
                     align = 'center',
                     fill = dict(color = '#111111')
                     ),
        columnwidth=[0.6, 1, 1, 0.3, 0.4],
    ))

    fig.update_layout(
        template='plotly_dark',
        margin = dict(t=0, l=0, r=0, b=0),
        height=248,)

    if chosen_opposition == None:
        pass
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        team_name = team
        versus_name = chosen_opposition

        df3_team = df3.loc[((df3['home'] == team_name) | (df3['visitor'] == team_name))
                    & ((df3['home'] == versus_name) | (df3['visitor'] == versus_name))].copy()

        if len(df3_team['Season']) == 0:
            pass
        else:
            df3_team.insert(13, "WDL", None, True)

            df3_team.loc[((df3_team.result == 'H') & (df3.home == team_name)), 'WDL'] = 'W'
            df3_team.loc[((df3_team.result == 'A') & (df3.home == team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'H') & (df3.home != team_name)), 'WDL'] = 'L'
            df3_team.loc[((df3_team.result == 'A') & (df3.home != team_name)), 'WDL'] = 'W'
            df3_team.loc[df3_team.result == 'D', 'WDL'] = 'D'

            fig = go.Figure()

            cell_colors = {'W': '#56b36f', 'D': 'white', 'L': '#eb5a4e',}
            text_colors = {'W': 'white', 'D': '#111111', 'L': 'white'}

            fig.add_trace(go.Table(
                header = dict(values = ['Date', 'Home', 'Away', 'Score', 'Tier'],
                              fill = dict(color = '#343a40')),
                cells = dict(values = [df3_team['Date'], df3_team['home'], df3_team['visitor'], df3_team['FT'], df3_team['tier']],
                             align = 'center',
                             font = dict(color = ['white',
                                                  'white',
                                                  'white',
                                                  '#111111',
                                                  'white',]
                             ),
                             fill = dict(color = ['#111111',
                                                  '#111111',
                                                  '#111111',
                                                  [cell_colors[score] for score in df3_team['WDL']],
                                                  '#111111',]),
                             ),
                columnwidth=[0.6, 1, 1, 0.3, 0.4],
            ))

            fig.update_layout(
                template='plotly_dark',
                margin = dict(t=0, l=0, r=0, b=0),
                height=248,)

    return fig





@app.callback(
    Output('range-dates', 'children'),
    [Input('Map', 'clickData'),
     Input('range-slider-all-pies', 'value'),])
def update_output(chosen_team, range_values):
    if chosen_team == None:
        return '1888/89 - 2018/19'
    else:
        text = '%s - %s' % (df2['Master'].at[range_values[0], 'Season'], df2['Master'].at[range_values[1], 'Season'])
        return text

@app.callback(
    Output('range-slider-all-pies', 'disabled'),
    [Input('Map', 'clickData'),])
def update_output(chosen_team):
    if chosen_team == None:
        return True
    else:
        return False

@app.callback(
    Output('gd-pie', 'figure'),
    [Input('Map', 'clickData'),
    Input('range-slider-all-pies', 'value')])
def update_output(chosen_team, years_range):

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=['A'],
        values=[1],
        marker=dict(colors=['#111111'],
                   line=dict(color='white',
                             width=3,)
        ),
        hole=0.5,
        textinfo='none',
        hoverinfo='none',
    ))

    fig.update_layout(
        annotations=[
            dict(text="Goals For / Against",
                 font=dict(color='white'),
                 xref='paper',
                 yref='paper',
                 x=0.5,
                 y=1.25,
                 showarrow=False,
            )
        ],
        showlegend=False,
        template='plotly_dark',
        margin = dict(t=35, l=0, r=0, b=3),
        height=148,
    )

    if chosen_team == None:
        pass
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        df2_team = df2[team][years_range[0]:years_range[1]+1]

        HF = df2_team['HF'].sum(skipna=True)
        HA = df2_team['HA'].sum(skipna=True)
        AF = df2_team['AF'].sum(skipna=True)
        AA = df2_team['AA'].sum(skipna=True)
        Pld = df2_team['Pld'].sum(skipna=True)

        if Pld == 0:
            pass
        else:

            fig = go.Figure()

            fig.add_trace(go.Pie(
                ids=['Home', 'Away'],
                labels=['Home', 'Away'],
                values=[(HF+HA),(AF+AA)],
                marker=dict(colors=[df1_all.at[team, 'colour'], df1_all.at[team, 'colour_away']],
                           line=dict(color='#111111',
                                     width=3,)
                ),
                rotation=(AF+AA)/(AF+AA+HF+HA)*360,
                hole=0,
                textinfo='none',
                hoverinfo='none',
                sort=False,
                customdata=[],
                meta=[],
                hovertemplate= "%{label}<br>" +
                               "<extra></extra>",
            ))



            fig.add_trace(go.Pie(
                ids=['Away For', 'Home For', 'Home Against', 'Away Against',],
                labels=['Away For', 'Home For', 'Home Against', 'Away Against',],
                values=[100*(AF/(AF+HF+HA+AA)),
                        100*(HF/(AF+HF+HA+AA)),
                        100*(HA/(AF+HF+HA+AA)),
                        100*(AA/(AF+HF+HA+AA)),
                       ],
                marker=dict(colors=['#39a757', '#39a757', '#ea4335', '#ea4335',],
                           line=dict(color='#111111',
                                     width=3,)
                ),
                hole=0.5,
                textinfo='none',
                sort=False,
                customdata=['For', 'For', 'Against', 'Against',],
                meta=[(100*((AF+HF)/(AF+HF+HA+AA))),
                      (100*((AF+HF)/(AF+HF+HA+AA))),
                      (100*((AA+HA)/(AF+HF+HA+AA))),
                      (100*((AA+HA)/(AF+HF+HA+AA))),],
                hovertemplate= "%{label} %: %{percent}<br>" +
                               "Total %{customdata} %: %{meta:.1f}%<br>"
                                    "<extra></extra>",
            ))

            fig.update_layout(
                annotations=[
                    dict(text="Goals For / Against",
                         font=dict(color='white'),
                         xref='paper',
                         yref='paper',
                         x=0.5,
                         y=1.25,
                         showarrow=False,
                    )
                ],
                showlegend=False,
                template='plotly_dark',
                margin = dict(t=32, l=0, r=0, b=0),
                height=148,
                legend=dict(traceorder='normal'))

    return fig

@app.callback(
    Output('wdl-pie', 'figure'),
    [Input('Map', 'clickData'),
    Input('range-slider-all-pies', 'value')])
def update_output(chosen_team, years_range):

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=['A'],
        values=[1],
        marker=dict(colors=['#111111'],
                   line=dict(color='white',
                             width=3,)
        ),
        hole=0.5,
        textinfo='none',
        hoverinfo='none',
    ))

    fig.update_layout(
        annotations=[
            dict(text="Win / Draw / Loss",
                 font=dict(color='white'),
                 xref='paper',
                 yref='paper',
                 x=0.5,
                 y=1.25,
                 showarrow=False,
            )
        ],
        showlegend=False,
        template='plotly_dark',
        margin = dict(t=35, l=0, r=0, b=35),
        height=180,
    )

    if chosen_team == None:
        pass
    else:

        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        df2_team = df2[team][years_range[0]:years_range[1]+1]

        fig = go.Figure()

        HW = df2_team['HW'].sum(skipna=True)
        HD = df2_team['HD'].sum(skipna=True)
        HL = df2_team['HL'].sum(skipna=True)
        AW = df2_team['AW'].sum(skipna=True)
        AD = df2_team['AD'].sum(skipna=True)
        AL = df2_team['AL'].sum(skipna=True)
        Pld = df2_team['Pld'].sum(skipna=True)


        fig.add_trace(go.Pie(
            ids=['Home', 'Away'],
            labels=['Home', 'Away'],
            values=[1,1],
            marker=dict(colors=[df1_all.at[team, 'colour'], df1_all.at[team, 'colour_away']],
                       line=dict(color='#111111',
                                 width=3,)
            ),
            rotation=180,
            hole=0,
            textinfo='none',
            hoverinfo='none',
            sort=False,
            customdata=[],
            meta=[],
            hovertemplate= "%{label}<br>" +
                           "<extra></extra>",
        ))

        fig.add_trace(go.Pie(
            ids=['Away Win', 'Home Win', 'Home Draw', 'Home Loss', 'Away Loss', 'Away Draw'],
            labels=['Away Win', 'Home Win', 'Home Draw', 'Home Loss', 'Away Loss', 'Away Draw'],
            values=[AW,
                    HW,
                    HD,
                    HL,
                    AL,
                    AD],
            marker=dict(colors=['#39a757', '#39a757', 'white', '#ea4335', '#ea4335', 'white'],
                       line=dict(color='#111111',
                                 width=3,)
            ),
            hole=0.5,
            textinfo='none',
            sort=False,
            customdata=['Win', 'Win', 'Draw', 'Loss', 'Loss', 'Draw',],
            meta=[(100*((AW+HW)/Pld)),
                  (100*((AW+HW)/Pld)),
                  (100*((AD+HD)/Pld)),
                  (100*((AL+HL)/Pld)),
                  (100*((AL+HL)/Pld)),
                  (100*((AD+HD)/Pld)),],
            hovertemplate= "%{label} %: %{percent}<br>" +
                           "Total %{customdata} %: %{meta:.1f}%<br>"
                                "<extra></extra>",
        ))

        fig.update_layout(
            annotations=[
                dict(text="Win / Draw / Loss",
                     font=dict(color='white'),
                     xref='paper',
                     yref='paper',
                     x=0.5,
                     y=1.25,
                     showarrow=False,
                )
            ],
            showlegend=False,
            template='plotly_dark',
            margin = dict(t=35, l=0, r=0, b=35),
            height=180,
            legend=dict(traceorder='normal'))

    return fig


@app.callback(
    Output('pts-pie', 'figure'),
    [Input('Map', 'clickData'),
    Input('range-slider-all-pies', 'value')])
def update_output(chosen_team, years_range):
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=['A'],
        values=[1],
        marker=dict(colors=['#111111'],
                   line=dict(color='white',
                             width=3,)
        ),
        hole=0.5,
        textinfo='none',
        hoverinfo='none',
    ))

    fig.update_layout(
        annotations=[
            dict(text="Points",
                 font=dict(color='white'),
                 xref='paper',
                 yref='paper',
                 x=0.5,
                 y=1.25,
                 showarrow=False,
            ),
        ],
        showlegend=False,
        template='plotly_dark',
        margin = dict(t=35, l=0, r=0, b=35),
        height=180,
    )

    if chosen_team == None:
        pass

    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        df2_team = df2[team][years_range[0]:years_range[1]+1]


        HPts = df2_team['HPts'].sum(skipna=True)
        APts = df2_team['APts'].sum(skipna=True)

        if HPts == 0 or APts == 0:
            pass
        else:

            fig = go.Figure()

            fig.add_trace(go.Pie(
                ids=['Home', 'Away'],
                labels=['Home', 'Away'],
                values=[HPts, APts],
                marker=dict(colors=[df1_all.at[team, 'colour'], df1_all.at[team, 'colour_away']],
                           line=dict(color='#111111',
                                     width=3,)
                ),
                rotation=APts/(HPts+APts)*360,
                hole=0.5,
                textinfo='none',
                hovertemplate= "%{label} Pts: %{percent}<br>" +
                                    "<extra></extra>",
            ))

            fig.update_layout(
                annotations=[
                    dict(text="Points",
                         font=dict(color='white'),
                         xref='paper',
                         yref='paper',
                         x=0.5,
                         y=1.25,
                         showarrow=False,
                    ),
                    dict(text="Home",
                         font=dict(color=df1_all.at[team, 'colour']),
                         xref='paper',
                         yref='paper',
                         x=0.05,
                         y=0,
                         showarrow=False,
                    ),
                    dict(text="Away",
                         font=dict(color=df1_all.at[team, 'colour_away']),
                         xref='paper',
                         yref='paper',
                         x=0.95,
                         y=0,
                         showarrow=False,
                    )
                ],
                showlegend=False,
                template='plotly_dark',
                margin = dict(t=35, l=0, r=0, b=35),
                height=180,)

    return fig




@app.callback(
    Output('team-GD', 'figure'),
    [Input('GD-graph-dropdown', 'value'),
    Input('Map', 'clickData')])
def team_GD_generator(graph_option, chosen_team):

    if graph_option == 'All':
        fig = go.Figure()

        dff2 = df2['Master']

        fig.add_trace(go.Bar(
            name='for',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))
        fig.add_trace(go.Bar(
            name='against',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))

        fig.add_annotation(go.layout.Annotation(
                                        text = 'For',
                                        textangle = 270,
                                        x = 0,
                                        y = 80,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))

        fig.add_annotation(go.layout.Annotation(
                                        text = 'Against',
                                        textangle = 270,
                                        x = 0,
                                        y = -100,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))
        fig.update_layout(template = 'plotly_dark',
                  barmode='relative',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                               showgrid=False,
                               tickangle=0,
                               tickmode = 'array',
                               tickvals = [0, 32, 65, 97, 130],
                               fixedrange=True),
                  yaxis = dict(range = (-135, 135),
                               zeroline=False,
                               showgrid=False,
                               tickmode='array',
                               tickvals=[-100, -50, 0, 50, 100],
                               ticktext=[100, 50, 0, 50, 100],
                               title=dict(text='Goals', standoff=10),
                               fixedrange=True,),
                  xaxis_title = 'Season',
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=0,
                      t=0,
                      b=0,
                  ),
                  height=210,
                  )

        if chosen_team == None:
            pass

        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            if df2_team['GD'].sum(skipna=True) == 0:
                pass
            else:

                best_gd = int(df2_team['GD'].max())
                worst_gd = int(df2_team['GD'].min())

                color_list = []

                if best_gd >= worst_gd:
                    largest_mag_gd = abs(best_gd)
                else:
                    largest_mag_gd = abs(worst_gd)

                for i in range((largest_mag_gd)*(-1), (largest_mag_gd+1)):
                    color_list.append(i)

                fig.update_traces(
                    selector=dict(name='against'),
                    x = df2_team['Season'],
                    y = -(df2_team['GA']),
                    marker=dict(
                        cmin=largest_mag_gd*(-1),
                        cmax=largest_mag_gd,
                        color=df2_team['GD'],
                        colorbar=dict(
                            thickness=15,
                            showticklabels=False,
                            title=dict(text='Goal Difference',
                                    side='right',)
                                    ),
                        colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                        ),
                    meta=df2_team['GA'],
                    customdata=df2_team['GD'],
                    hovertemplate="Season: %{x}<br>" +
                            "Goals Against: %{meta}<br>" +
                            "Goal Difference: %{customdata}<br>" +
                            "<extra></extra>",
                )

                fig.update_traces(
                    selector=dict(name='for'),
                    x = df2_team['Season'],
                    y = df2_team['GF'],
                    marker=dict(
                        cmin=largest_mag_gd*(-1),
                        cmax=largest_mag_gd,
                        color=(df2_team['GD']),
                        colorbar=dict(
                            thickness=15,
                            showticklabels=False,
                            title=dict(text='Goal Difference',
                                    side='right',)
                        ),
                        colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                        ),
                        customdata=df2_team['GD'],
                        hovertemplate="Season: %{x}<br>" +
                          "Goals For: %{y}<br>" +
                          "Goal Difference: %{customdata}<br>" +
                          "<extra></extra>",
                )

        return fig

    elif graph_option == 'Home':
        fig = go.Figure()

        dff2 = df2['Master']

        fig.add_trace(go.Bar(
            name='for',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))
        fig.add_trace(go.Bar(
            name='against',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))

        fig.add_annotation(
                                        name='for',
                                        text = 'For',
                                        textangle = 270,
                                        x = 0,
                                        y = 80,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        )

        fig.add_annotation(go.layout.Annotation(
                                        name='against',
                                        text = 'Against',
                                        textangle = 270,
                                        x = 0,
                                        y = -100,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))
        fig.update_layout(template = 'plotly_dark',
                  barmode='relative',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                               showgrid=False,
                               tickangle=0,
                               tickmode = 'array',
                               tickvals = [0, 32, 65, 97, 130],
                               fixedrange=True,),
                  yaxis = dict(range = (-135, 135),
                               zeroline=False,
                               showgrid=False,
                               tickmode='array',
                               tickvals=[-100, -50, 0, 50, 100],
                               ticktext=[100, 50, 0, 50, 100],
                               title=dict(text='Goals', standoff=10),
                               fixedrange=True,),
                  xaxis_title = 'Season',
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=0,
                      t=0,
                      b=0,
                  ),
                  height=210,
                  )

        if chosen_team == None:
            pass

        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            best_gd = int(df2_team['HGD'].max())
            worst_gd = int(df2_team['HGD'].min())
            color_list = []

            if best_gd >= worst_gd:
                largest_mag_gd = abs(best_gd)
            else:
                largest_mag_gd = abs(worst_gd)

            for i in range((largest_mag_gd)*(-1), (largest_mag_gd+1)):
                color_list.append(i)

            fig.update_traces(
                selector=dict(name='against'),
                x = df2_team['Season'],
                y = -(df2_team['HA']),
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=df2_team['HGD'],
                    colorbar=dict(
                        thickness=15,
                        showticklabels=False,
                        title=dict(text='Goal Difference',
                                side='right',)
                                ),
                    colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                    ),
                meta=df2_team['HA'],
                customdata=df2_team['HGD'],
                hovertemplate="Season: %{x}<br>" +
                        "Home Goals Against: %{meta}<br>" +
                        "Home Goal Difference: %{customdata}<br>" +
                        "<extra></extra>",
            )

            fig.update_traces(
                selector=dict(name='for'),
                x = df2_team['Season'],
                y = df2_team['HF'],
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=(df2_team['HGD']),
                    colorbar=dict(
                        thickness=15,
                        showticklabels=False,
                        title=dict(text='Goal Difference',
                                side='right',)
                    ),
                    colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                    ),
                    customdata=df2_team['HGD'],
                    hovertemplate="Season: %{x}<br>" +
                      "Home Goals For: %{y}<br>" +
                      "Home Goal Difference: %{customdata}<br>" +
                      "<extra></extra>",
            )
            fig.add_annotation(go.layout.Annotation(
                    text = 'For',
                    textangle = 270,
                    x = 0,
                    y = 41,
                    xshift = -35,
                    font = dict(size=12),
                    showarrow = False,
                    valign = 'middle',
            ))
            fig.add_annotation(go.layout.Annotation(
                    text = 'Against',
                    textangle = 270,
                    x = 0,
                    y = -52,
                    xshift = -35,
                    font = dict(size=12),
                    showarrow = False,
                    valign = 'middle',
            ))
            fig.update_layout(
                xaxis = dict(range = (-0.5, 130.5),
                             showgrid=False,
                             tickangle=0,
                             tickmode = 'array',
                             tickvals = [0, 32, 65, 97, 130],
                             fixedrange=True,),
                yaxis = dict(range = (-75, 75),
                             zeroline=False,
                             showgrid=False,
                             tickmode='array',
                             tickvals=[-60, -30, 0, 30, 60],
                             ticktext=[60, 30, 0, 30, 60],
                             title=dict(text='Goals', standoff=16),
                             fixedrange=True,),
            )

        return fig

    elif graph_option == 'Away':
        fig = go.Figure()

        dff2 = df2['Master']

        fig.add_trace(go.Bar(
            name='for',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))
        fig.add_trace(go.Bar(
            name='against',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))

        fig.add_annotation(go.layout.Annotation(
                                        text = 'For',
                                        textangle = 270,
                                        x = 0,
                                        y = 80,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))

        fig.add_annotation(go.layout.Annotation(
                                        text = 'Against',
                                        textangle = 270,
                                        x = 0,
                                        y = -100,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))
        fig.update_layout(template = 'plotly_dark',
                  barmode='relative',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                               showgrid=False,
                               tickangle=0,
                               tickmode = 'array',
                               tickvals = [0, 32, 65, 97, 130],
                               fixedrange=True,),
                  yaxis = dict(range = (-135, 135),
                               zeroline=False,
                               showgrid=False,
                               tickmode='array',
                               tickvals=[-100, -50, 0, 50, 100],
                               ticktext=[100, 50, 0, 50, 100],
                               title=dict(text='Goals', standoff=10),
                               fixedrange=True,),
                  xaxis_title = 'Season',
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=0,
                      t=0,
                      b=0,
                  ),
                  height=210,
                  )

        if chosen_team == None:
            pass

        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            best_gd = int(df2_team['AGD'].max())
            worst_gd = int(df2_team['AGD'].min())
            color_list = []

            if best_gd >= worst_gd:
                largest_mag_gd = abs(best_gd)
            else:
                largest_mag_gd = abs(worst_gd)

            for i in range((largest_mag_gd)*(-1), (largest_mag_gd+1)):
                color_list.append(i)

            fig.update_traces(
                selector=dict(name='against'),
                x = df2_team['Season'],
                y = -(df2_team['AA']),
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=df2_team['AGD'],
                    colorbar=dict(
                        thickness=15,
                        showticklabels=False,
                        title=dict(text='Goal Difference',
                                side='right',)
                                ),
                    colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                    ),
                meta=df2_team['AA'],
                customdata=df2_team['AGD'],
                hovertemplate="Season: %{x}<br>" +
                        "Away Goals Against: %{meta}<br>" +
                        "Away Goal Difference: %{customdata}<br>" +
                        "<extra></extra>",
            )

            fig.update_traces(
                selector=dict(name='for'),
                x = df2_team['Season'],
                y = df2_team['AF'],
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=(df2_team['AGD']),
                    colorbar=dict(
                        thickness=15,
                        showticklabels=False,
                        title=dict(text='Goal Difference',
                                side='right',)
                    ),
                    colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                    ),
                    customdata=df2_team['AGD'],
                    hovertemplate="Season: %{x}<br>" +
                      "Away Goals For: %{y}<br>" +
                      "Away Goal Difference: %{customdata}<br>" +
                      "<extra></extra>",
            )

            fig.add_annotation(go.layout.Annotation(
                    text = 'For',
                    textangle = 270,
                    x = 0,
                    y = 41,
                    xshift = -35,
                    font = dict(size=12),
                    showarrow = False,
                    valign = 'middle',
            ))
            fig.add_annotation(go.layout.Annotation(
                    text = 'Against',
                    textangle = 270,
                    x = 0,
                    y = -52,
                    xshift = -35,
                    font = dict(size=12),
                    showarrow = False,
                    valign = 'middle',
            ))
            fig.update_layout(
                xaxis = dict(range = (-0.5, 130.5),
                             showgrid=False,
                             tickangle=0,
                             tickmode = 'array',
                             tickvals = [0, 32, 65, 97, 130],
                             fixedrange=True,),
                yaxis = dict(range = (-75, 75),
                             zeroline=False,
                             showgrid=False,
                             tickmode='array',
                             tickvals=[-60, -30, 0, 30, 60],
                             ticktext=[60, 30, 0, 30, 60],
                             title=dict(text='Goals', standoff=16),
                             fixedrange=True,),
            )

        return fig

    elif graph_option == 'Home & Away':
        fig = go.Figure()

        dff2 = df2['Master']

        fig.add_trace(go.Bar(
            name='for',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))
        fig.add_trace(go.Bar(
            name='against',
            x = dff2['Season'],
            y = dff2['Zeros'],
            marker=dict(
                color='#111111',
                colorbar=dict(
                    thickness=15,
                    showticklabels=False,
                    title=dict(text='Goal Difference',
                            side='right',)
                            ),
                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
            ),
            hoverinfo='none'
        ))

        fig.add_annotation(go.layout.Annotation(
                                        text = 'For',
                                        textangle = 270,
                                        x = 0,
                                        y = 80,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))

        fig.add_annotation(go.layout.Annotation(
                                        text = 'Against',
                                        textangle = 270,
                                        x = 0,
                                        y = -100,
                                        xshift = -35,
                                        font = dict(size=12),
                                        showarrow = False,
                                        valign = 'middle',
        ))
        fig.update_layout(template = 'plotly_dark',
                  barmode='relative',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                               showgrid=False,
                               tickangle=0,
                               tickmode = 'array',
                               tickvals = [0, 32, 65, 97, 130],
                               fixedrange=True,),
                  yaxis = dict(range = (-135, 135),
                               zeroline=False,
                               showgrid=False,
                               tickmode='array',
                               tickvals=[-100, -50, 0, 50, 100],
                               ticktext=[100, 50, 0, 50, 100],
                               title=dict(text='Goals', standoff=10),
                               fixedrange=True,),
                  xaxis_title = 'Season',
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=0,
                      t=0,
                      b=0,
                  ),
                  height=210,
                  )

        if chosen_team == None:
            pass

        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig = go.Figure()

            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,)

            all_gds = [abs((df2_team['HGD'].max())), abs((df2_team['HGD'].min())), abs((df2_team['AGD'].max())), abs((df2_team['AGD'].min()))]
            largest_mag_gd = abs(max(all_gds))

            fig.add_trace(go.Bar(
                x = df2_team['Season'],
                y = -(df2_team['HA']),
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=df2_team['HGD'],
                    colorbar=dict(
                            showticklabels=False,
                            thickness=15,
                            title=dict(text='Goal Difference',
                                side='right',)
                                ),
                                colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                                ),
                                meta=df2_team['HA'],
                                customdata=df2_team['HGD'],
                                hovertemplate="Season: %{x}<br>" +
                                "Home Goals Against: %{meta}<br>" +
                                "Home Goal Difference: %{customdata}<br>" +
                                "<extra></extra>",
                                ),
            row=1,
            col=1,
            )

            fig.add_trace(go.Bar(
                x = df2_team['Season'],
                y = df2_team['HF'],
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=(df2_team['HGD']),
                    colorbar=dict(
                        showticklabels=False,
                        thickness=15,
                        title=dict(text='Goal Difference',
                            side='right',)
                            ),
                            colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                            ),
                            customdata=df2_team['HGD'],
                            hovertemplate="Season: %{x}<br>" +
                            "Home Goals For: %{y}<br>" +
                            "Home Goal Difference: %{customdata}<br>" +
                            "<extra></extra>",
                            ),
                    row=1,
                    col=1,
                )

            fig.add_trace(go.Bar(
                x = df2_team['Season'],
                y = -(df2_team['AA']),
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=df2_team['AGD'],
                    colorbar=dict(
                        showticklabels=False,
                        thickness=15,
                        title=dict(text='Goal Difference',
                               side='right',)
                               ),
                    colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                    ),
                    meta=df2_team['AA'],
                    customdata=df2_team['AGD'],
                    hovertemplate="Season: %{x}<br>" +
                        "Away Goals Against: %{meta}<br>" +
                        "Away Goal Difference: %{customdata}<br>" +
                        "<extra></extra>",
                    ),
                row=2,
                col=1,
                )

            fig.add_trace(go.Bar(
                x = df2_team['Season'],
                y = df2_team['AF'],
                marker=dict(
                    cmin=largest_mag_gd*(-1),
                    cmax=largest_mag_gd,
                    color=(df2_team['AGD']),
                    colorbar=dict(
                        showticklabels=False,
                        thickness=15,
                        title=dict(text='Goal Difference',
                                   side='right',)
                                   ),
                        colorscale=[[0, '#ea4335'], [0.5, '#f0f0f0'],  [1, '#39a757']],
                        ),
                    customdata=df2_team['AGD'],
                    hovertemplate="Season: %{x}<br>" +
                            "Away Goals For: %{y}<br>" +
                            "Away Goal Difference: %{customdata}<br>" +
                            "<extra></extra>",
                            ),
                row=2,
                col=1,
            )

            fig.update_layout(template = 'plotly_dark',
                      height=210,
                      margin=dict(
                          l=0,
                          r=0,
                          t=0,
                          b=0,
                      ),
                      barmode='relative',
                      bargap = 0,
                      xaxis1 = dict(range = (-0.5, 130.5),
                                   zeroline=False,
                                   showgrid=False,
                                   tickmode = 'array',
                                   tickvals = [0, 32, 65, 97, 130],
                                   fixedrange=True,),
                      xaxis2 = dict(range = (-0.5, 130.5),
                                   zeroline=False,
                                   showgrid=False,
                                   tickmode = 'array',
                                   tickvals = [0, 32, 65, 97, 130],
                                   title='Season',
                                   fixedrange=True,),
                      yaxis1 = dict(range = (-60, 75),
                                   zeroline=False,
                                   showgrid=False,
                                   tickmode='array',
                                   tickvals=[-60, 0, 60],
                                   ticktext=[60, 0, 60],
                                   fixedrange=True,
                                   title=dict(text=' ', standoff=16),
                                   ),
                      yaxis2 = dict(range = (-75, 60),
                                   zeroline=False,
                                   showgrid=False,
                                   tickmode='array',
                                   tickvals=[-60, 0, 60],
                                   ticktext=[60, 0, 60],
                                   fixedrange=True,
                                   title=dict(text=' ', standoff=16),
                                   ),
                      showlegend = False,
                      annotations=[
                          dict(
                              xref='x2',
                              yref='y2',
                              text = 'Away',
                              x = 66,
                              y = 60,
                              font = dict(size=12),
                              showarrow = False,
                              valign = 'middle',
                          ),
                          dict(
                              xref='x1',
                              yref='y1',
                              text = 'Home',
                              x = 66,
                              y = -59,
                              font = dict(size=12),
                              showarrow = False,
                              valign = 'middle',
                          ),
                        dict(
                              xref='x1',
                              yref='y1',
                              text = 'For',
                              textangle = 270,
                              x = 0,
                              y = 52,
                              xshift = -25,
                              font = dict(size=10),
                              showarrow = False,
                              valign = 'middle',
                          ),
                          dict(
                              xref='x1',
                              yref='y1',
                              text = 'Against',
                              textangle = 270,
                              x = 0,
                              y = -45,
                              xshift = -25,
                              font = dict(size=10),
                              showarrow = False,
                              valign = 'middle',
                          ),
                        dict(
                              xref='x2',
                              yref='y2',
                              text = 'For',
                              textangle = 270,
                              x = 0,
                              y = 52,
                              xshift = -25,
                              font = dict(size=10),
                              showarrow = False,
                              valign = 'middle',
                          ),
                          dict(
                              xref='x2',
                              yref='y2',
                              text = 'Against',
                              textangle = 270,
                              x = 0,
                              y = -45,
                              xshift = -25,
                              font = dict(size=10),
                              showarrow = False,
                              valign = 'middle',
                          ),
                          dict(
                              xref='x1',
                              yref='y1',
                              text = 'Goals',
                              textangle = 270,
                              x = 0,
                              y = -70,
                              yshift = -15,
                              xshift = -37,
                              font = dict(size=14),
                              showarrow = False,
                              valign = 'middle',
                          ),
                      ])

        return fig


@app.callback(
    Output('team-WDL', 'figure'),
    [Input('WDL-graph-dropdown', 'value'),
     Input('Map', 'clickData')])
def update_output(graph_option, chosen_team):

    if graph_option == 'All':

        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Bar(
                     name='placeholder',
                     visible=True,
                     hoverinfo='none',
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='losses',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='draws',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                        color = 'white',
        )))
        fig.add_trace(go.Bar(
                     name='wins',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#56b36f',
        )))

        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.86',
                                  line = dict(color = '#56b36f'),
                                  fillcolor = '#56b36f'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.64',
                                  line = dict(color = 'white'),
                                  fillcolor = 'white'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.41',
                                  line = dict(color = '#eb5a4e'),
                                  fillcolor = '#eb5a4e'
                                  ))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Win',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.86,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Draw',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.115,
                                            y = 0.59,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Loss',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.37,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(template = 'plotly_dark',
                  barmode='stack',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                      zeroline=False,
                      showgrid=False,
                      tickmode = 'array',
                      tickvals = [0, 32, 65, 97, 130],),
                  yaxis = dict(range = (-5, 110),
                      zeroline=False,
                      showgrid=False,
                      title=dict(text='Games (%)', standoff=10),
                      fixedrange=True,),
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=61,
                      t=0,
                      b=0,
                  ),
                  height=180,)

        if chosen_team == None:
            pass
        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig.update_traces(
                         selector=dict(name='placeholder'),
                         visible=False,
            ),
            fig.update_traces(
                         selector=dict(name='losses'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['L']/df2_team['Pld']),
                         marker = dict(
                             color = '#eb5a4e',),
                         hovertemplate="Season: %{x}<br>" +
                              "Loss %: %{y:.0f}<br>" +
                              "<extra></extra>",
            )
            fig.update_traces(
                         selector=dict(name='draws'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['D']/df2_team['Pld']),
                         marker = dict(
                            color = '#f0f0f0',),
                        hovertemplate="Season: %{x}<br>" +
                             "Draw %: %{y:.0f}<br>" +
                             "<extra></extra>",

            )
            fig.update_traces(
                         selector=dict(name='wins'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['W']/df2_team['Pld']),
                         marker = dict(
                             color = '#56b36f',),
                        hovertemplate="Season: %{x}<br>" +
                             "Win %: %{y:.0f}<br>" +
                             "<extra></extra>",
            )


        return fig

    elif graph_option == 'Home':
        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Bar(
                     name='placeholder',
                     visible=True,
                     hoverinfo='none',
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='losses',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='draws',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                        color = 'white',
        )))
        fig.add_trace(go.Bar(
                     name='wins',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#56b36f',
        )))

        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.86',
                                  line = dict(color = '#56b36f'),
                                  fillcolor = '#56b36f'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.64',
                                  line = dict(color = 'white'),
                                  fillcolor = 'white'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.41',
                                  line = dict(color = '#eb5a4e'),
                                  fillcolor = '#eb5a4e'
                                  ))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Win',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.86,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Draw',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.115,
                                            y = 0.59,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Loss',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.37,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(template = 'plotly_dark',
                  barmode='stack',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                      zeroline=False,
                      showgrid=False,
                      tickmode = 'array',
                      tickvals = [0, 32, 65, 97, 130],),
                  yaxis = dict(range = (-5, 110),
                      zeroline=False,
                      showgrid=False,
                      title=dict(text='Games (%)', standoff=10)),
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=61,
                      t=0,
                      b=0,
                  ),
                  height=180,)

        if chosen_team == None:
            pass
        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig.update_traces(
                         selector=dict(name='placeholder'),
                         visible=False,
            ),
            fig.update_traces(
                         selector=dict(name='losses'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['HL']/(df2_team['Pld']/2)),
                         marker = dict(
                             color = '#eb5a4e',),
                         hovertemplate="Season: %{x}<br>" +
                              "Home Loss %: %{y:.0f}<br>" +
                              "<extra></extra>",
            )
            fig.update_traces(
                         selector=dict(name='draws'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['HD']/(df2_team['Pld']/2)),
                         marker = dict(
                            color = '#f0f0f0',),
                        hovertemplate="Season: %{x}<br>" +
                             "Home Draw %: %{y:.0f}<br>" +
                             "<extra></extra>",

            )
            fig.update_traces(
                         selector=dict(name='wins'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['HW']/(df2_team['Pld']/2)),
                         marker = dict(
                             color = '#56b36f',),
                        hovertemplate="Season: %{x}<br>" +
                             "Home Win %: %{y:.0f}<br>" +
                             "<extra></extra>",
            )


        return fig

    elif graph_option == 'Away':
        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Bar(
                     name='placeholder',
                     visible=True,
                     hoverinfo='none',
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='losses',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='draws',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                        color = 'white',
        )))
        fig.add_trace(go.Bar(
                     name='wins',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#56b36f',
        )))

        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.86',
                                  line = dict(color = '#56b36f'),
                                  fillcolor = '#56b36f'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.64',
                                  line = dict(color = 'white'),
                                  fillcolor = 'white'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.41',
                                  line = dict(color = '#eb5a4e'),
                                  fillcolor = '#eb5a4e'
                                  ))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Win',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.86,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Draw',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.115,
                                            y = 0.59,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Loss',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.37,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(template = 'plotly_dark',
                  barmode='stack',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                      zeroline=False,
                      showgrid=False,
                      tickmode = 'array',
                      tickvals = [0, 32, 65, 97, 130],),
                  yaxis = dict(range = (-5, 110),
                      zeroline=False,
                      showgrid=False,
                      title=dict(text='Games (%)', standoff=10)),
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=61,
                      t=0,
                      b=0,
                  ),
                  height=180,)

        if chosen_team == None:
            pass
        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig.update_traces(
                         selector=dict(name='placeholder'),
                         visible=False,
            ),
            fig.update_traces(
                         selector=dict(name='losses'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['AL']/(df2_team['Pld']/2)),
                         marker = dict(
                             color = '#eb5a4e',),
                         hovertemplate="Season: %{x}<br>" +
                              "Away Loss %: %{y:.0f}<br>" +
                              "<extra></extra>",
            )
            fig.update_traces(
                         selector=dict(name='draws'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['AD']/(df2_team['Pld']/2)),
                         marker = dict(
                            color = '#f0f0f0',),
                        hovertemplate="Season: %{x}<br>" +
                             "Away Draw %: %{y:.0f}<br>" +
                             "<extra></extra>",

            )
            fig.update_traces(
                         selector=dict(name='wins'),
                         visible=True,
                         x = df2_team['Season'],
                         y = 100 * (df2_team['AW']/(df2_team['Pld']/2)),
                         marker = dict(
                             color = '#56b36f',),
                        hovertemplate="Season: %{x}<br>" +
                             "Away Win %: %{y:.0f}<br>" +
                             "<extra></extra>",
            )


        return fig

    elif graph_option == 'Home & Away':
        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Bar(
                     name='placeholder',
                     visible=True,
                     hoverinfo='none',
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='losses',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#111111',
        )))
        fig.add_trace(go.Bar(
                     name='draws',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                        color = 'white',
        )))
        fig.add_trace(go.Bar(
                     name='wins',
                     visible=False,
                     x = dff2['Season'],
                     y = dff2['Zeros'],
                     marker = dict(
                         color = '#56b36f',
        )))

        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.86',
                                  line = dict(color = '#56b36f'),
                                  fillcolor = '#56b36f'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.64',
                                  line = dict(color = 'white'),
                                  fillcolor = 'white'
                                  ))
        fig.add_shape(go.layout.Shape(
                                  type = 'circle',
                                  layer = 'above',
                                  x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                  xref='paper',
                                  yref='paper',
                                  xsizemode='pixel',
                                  ysizemode='pixel',
                                  xanchor='1.05',
                                  yanchor='0.41',
                                  line = dict(color = '#eb5a4e'),
                                  fillcolor = '#eb5a4e'
                                  ))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Win',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.86,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Draw',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.115,
                                            y = 0.59,
                                            showarrow = False,
                                            valign = 'middle',))
        fig.add_annotation(go.layout.Annotation(
                                            text = 'Loss',
                                            xref='paper',
                                            yref='paper',
                                            x = 1.11,
                                            y = 0.37,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(template = 'plotly_dark',
                  barmode='stack',
                  bargap = 0,
                  xaxis = dict(range = (-0.5, 130.5),
                      zeroline=False,
                      showgrid=False,
                      tickmode = 'array',
                      tickvals = [0, 32, 65, 97, 130],),
                  yaxis = dict(range = (-5, 110),
                      zeroline=False,
                      showgrid=False,
                      title=dict(text='Games (%)', standoff=10)),
                  showlegend = False,
                  margin=dict(
                      l=0,
                      r=61,
                      t=0,
                      b=0,
                  ),
                  height=180,)

        if chosen_team == None:
            pass
        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig = go.Figure()
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2)

            fig.add_trace(go.Bar(
                         x = df2_team['Season'],
                         y = 100 * (df2_team['HL']/(df2_team['Pld']/2)),
                         name = 'Losses',
                         marker = dict(
                             color = '#eb5a4e',
            )),
            row=1,
            col=1,
            )

            fig.add_trace(go.Bar(
                         x = df2_team['Season'],
                         y = 100 * (df2_team['HD']/(df2_team['Pld']/2)),
                         name = 'Draws',
                         marker = dict(
                            color = '#f0f0f0',
            )),
            row=1,
            col=1,
            )

            fig.add_trace(go.Bar(
                         x = df2_team['Season'],
                         y = 100 * (df2_team['HW']/(df2_team['Pld']/2)),
                         name = 'Wins',
                         marker = dict(
                             color = '#56b36f',
            )),
            row=1,
            col=1,
            )

            fig.add_trace(go.Bar(
                         x = df2_team['Season'],
                         y = 100 * (df2_team['AL']/(df2_team['Pld']/2)),
                         name = 'Losses',
                         marker = dict(
                             color = '#eb5a4e',
            )),
            row=2,
            col=1,
            )

            fig.add_trace(go.Bar(
                         x = df2_team['Season'],
                         y = 100 * (df2_team['AD']/(df2_team['Pld']/2)),
                         name = 'Draws',
                         marker = dict(
                            color = '#f0f0f0',
            )),
            row=2,
            col=1,
            )

            fig.add_trace(go.Bar(
                         x = df2_team['Season'],
                         y = 100 * (df2_team['AW']/(df2_team['Pld']/2)),
                         name = 'Wins',
                         marker = dict(
                             color = '#56b36f',
            )),
            row=2,
            col=1,
            )

            fig.add_shape(go.layout.Shape(
                                      type = 'circle',
                                      layer = 'above',
                                      x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                      xref='paper',
                                      yref='paper',
                                      xsizemode='pixel',
                                      ysizemode='pixel',
                                      xanchor='1.05',
                                      yanchor='0.86',
                                      line = dict(color = '#56b36f'),
                                      fillcolor = '#56b36f'
                                      ))
            fig.add_shape(go.layout.Shape(
                                      type = 'circle',
                                      layer = 'above',
                                      x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                      xref='paper',
                                      yref='paper',
                                      xsizemode='pixel',
                                      ysizemode='pixel',
                                      xanchor='1.05',
                                      yanchor='0.64',
                                      line = dict(color = 'white'),
                                      fillcolor = 'white'
                                      ))
            fig.add_shape(go.layout.Shape(
                                      type = 'circle',
                                      layer = 'above',
                                      x0 = 0, x1 = 8, y0 = 0, y1 = 8,
                                      xref='paper',
                                      yref='paper',
                                      xsizemode='pixel',
                                      ysizemode='pixel',
                                      xanchor='1.05',
                                      yanchor='0.41',
                                      line = dict(color = '#eb5a4e'),
                                      fillcolor = '#eb5a4e'
                                      ))
            fig.add_annotation(go.layout.Annotation(
                                                text = 'Win',
                                                xref='paper',
                                                yref='paper',
                                                x = 1.11,
                                                y = 0.86,
                                                showarrow = False,
                                                valign = 'middle',))
            fig.add_annotation(go.layout.Annotation(
                                                text = 'Draw',
                                                xref='paper',
                                                yref='paper',
                                                x = 1.115,
                                                y = 0.59,
                                                showarrow = False,
                                                valign = 'middle',))
            fig.add_annotation(go.layout.Annotation(
                                                text = 'Loss',
                                                xref='paper',
                                                yref='paper',
                                                x = 1.11,
                                                y = 0.37,
                                                showarrow = False,
                                                valign = 'middle',))
            fig.add_annotation(go.layout.Annotation(
                                                text = 'Home',
                                                xref='paper',
                                                yref='paper',
                                                x = 0.5,
                                                y = 0.57,
                                                showarrow = False,
                                                valign = 'middle',))
            fig.add_annotation(go.layout.Annotation(
                                                text = 'Away',
                                                xref='paper',
                                                yref='paper',
                                                x = 0.5,
                                                y = 0.43,
                                                showarrow = False,
                                                valign = 'middle',))

            fig.update_layout(template = 'plotly_dark',
                      barmode='stack',
                      bargap = 0,
                      xaxis1 = dict(range = (-0.5, 130.5),
                                   zeroline=False,
                                   showgrid=False,
                                   tickmode = 'array',
                                   tickvals = [0, 32, 65, 97, 130],
                                   fixedrange=True,),
                      xaxis2 = dict(range = (-0.5, 130.5),
                                   zeroline=False,
                                   showgrid=False,
                                   tickmode = 'array',
                                   tickvals = [0, 32, 65, 97, 130],
                                   fixedrange=True,),
                      yaxis1 = dict(range = (-5, 110),
                          zeroline=False,
                          showgrid=False,
                          title=dict(text='Games (%)', standoff=10, font=dict(size=14))),
                      yaxis2 = dict(range = (-5, 110),
                          zeroline=False,
                          showgrid=False,
                          title=dict(text='Games (%)', standoff=10, font=dict(size=14))),
                      showlegend = False,
                      margin=dict(
                          l=0,
                          r=61,
                          t=0,
                          b=0,
                      ),
                      height=180,)



        return fig


@app.callback(
    Output('team-pos', 'figure'),
    [Input('tot-pos-dropdown', 'value'),
    Input('Map', 'clickData')])
def update_output(graph_option, chosen_team):
    if graph_option == 'League Position':
        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name='team_trace',
            visible=False,
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_annotation(go.layout.Annotation(
                                            text = '1st Tier',
                                            x = 122,
                                            y = 6.5,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '2nd Tier',
                                            x = 122,
                                            y = 26,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '3rd Tier',
                                            x = 122,
                                            y = 50,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '4th Tier',
                                            x = 122,
                                            y = 74,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            xaxis = dict(range = (-0.5, 130.5),
                showgrid=False,
                tickangle=0,
                tickmode = 'array',
                tickvals = [0, 32, 65, 97, 130],
                ),
            yaxis = dict(
                zeroline=False,
                showgrid=False,
                range = (95.5, -0.5),
                tickmode = 'array',
                tickvals = [1, 20, 40, 60, 80],
                title=dict(text='Final League Position', standoff=15),
                ),
            margin=dict(
                l=0,
                r=62,
                t=0,
                b=0,
            ),
            height=180,
        )

        if chosen_team == None:
            pass
        else:
            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')

            df2_team = df2[team]

            fig.update_traces(
                selector=dict(name='team_trace'),
                visible=True,
                x=df2_team['Season'],
                y=df2_team['TotPos'],
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour']),
                marker=dict(
                    size=2,
                    color=df1_all.at[team, 'colour']),
                customdata=df2_team['Pos'],
                hovertemplate="Season: %{x}<br>" +
                      "League Position: %{customdata}<br>" +
                      "Full League Position: %{y}<br>" +
                      "<extra></extra>",
            )

    elif graph_option == 'Points %':

        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name='team_trace',
            visible=False,
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_annotation(go.layout.Annotation(
                                            text = '1st Tier',
                                            x = 122,
                                            y = 6.5,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '2nd Tier',
                                            x = 122,
                                            y = 26,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '3rd Tier',
                                            x = 122,
                                            y = 50,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '4th Tier',
                                            x = 122,
                                            y = 74,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            xaxis = dict(range = (-0.5, 130.5),
                showgrid=False,
                tickangle=0,
                tickmode = 'array',
                tickvals = [0, 32, 65, 97, 130],
                ),
            yaxis = dict(
                zeroline=False,
                showgrid=False,
                range = (95.5, -0.5),
                tickmode = 'array',
                tickvals = [1, 20, 40, 60, 80],
                title=dict(text='Final League Position', standoff=15),
                ),
            margin=dict(
                l=0,
                r=62,
                t=0,
                b=0,
            ),
            height=180,
        )

        if chosen_team == None:
            pass
        else:

            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df2_team['Season'],
                y=100 * (df2_team['Pts']/df2_team['Max_Pts']),
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour']),
                        marker=dict(
                            size=2,
                            color=df1_all.at[team, 'colour']),
                        customdata=df2_team['Pts'],
                        hovertemplate="Season: %{x}<br>" +
                              "Points: %{customdata}<br>" +
                              "Points (as % of max): %{y:0f}<br>" +
                              "<extra></extra>",)
            )

            fig.update_layout(
                    template='plotly_dark',
                    showlegend=False,
                    xaxis = dict(range = (-0.5, 130.5),
                        showgrid=False,
                        tickangle=0,
                        tickmode = 'array',
                        tickvals = [0, 32, 65, 97, 130],
                        ),
                    yaxis = dict(
                        zeroline=False,
                        showgrid=False,
                        range = (-5, 105),
                        tickmode = 'array',
                        tickvals = [0, 25, 50, 75, 100],
                        title=dict(text='Points (% of max)' , standoff=10),
                        ),
                    margin=dict(
                        l=0,
                        r=62,
                        t=0,
                        b=0,
                    ),
                    height=180,
                )

    elif graph_option == 'Points':
        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name='team_trace',
            visible=False,
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_annotation(go.layout.Annotation(
                                            text = '1st Tier',
                                            x = 122,
                                            y = 6.5,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '2nd Tier',
                                            x = 122,
                                            y = 26,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '3rd Tier',
                                            x = 122,
                                            y = 50,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '4th Tier',
                                            x = 122,
                                            y = 74,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            xaxis = dict(range = (-0.5, 130.5),
                showgrid=False,
                tickangle=0,
                tickmode = 'array',
                tickvals = [0, 32, 65, 97, 130],
                ),
            yaxis = dict(
                zeroline=False,
                showgrid=False,
                range = (95.5, -0.5),
                tickmode = 'array',
                tickvals = [1, 20, 40, 60, 80],
                title=dict(text='Final League Position', standoff=10),
                ),
            margin=dict(
                l=0,
                r=62,
                t=0,
                b=0,
            ),
            height=180,
        )

        if chosen_team == None:
            pass
        else:

            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df2_team['Season'],
                y=df2_team['Pts'],
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour']),
                        marker=dict(
                            size=2,
                            color=df1_all.at[team, 'colour']),
                        customdata=(100*df2_team['Pts']/df2_team['Max_Pts']),
                        hovertemplate="Season: %{x}<br>" +
                              "Points: {y}<br>" +
                              "Points (as % of max): %{customdata:0f}<br>" +
                              "<extra></extra>",)
            )

            fig.update_layout(
                    template='plotly_dark',
                    showlegend=False,
                    xaxis = dict(range = (-0.5, 130.5),
                        showgrid=False,
                        tickangle=0,
                        tickmode = 'array',
                        tickvals = [0, 32, 65, 97, 130],
                        ),
                    yaxis = dict(
                        zeroline=False,
                        showgrid=False,
                        range = (-5, 105),
                        tickmode = 'array',
                        tickvals = [0, 25, 50, 75, 100],
                        title=dict(text='Points', standoff=10),
                        ),
                    margin=dict(
                        l=0,
                        r=62,
                        t=0,
                        b=0,
                    ),
                    height=180,
                )

    elif graph_option == 'Home & Away Points':
        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name='team_trace',
            visible=False,
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_annotation(go.layout.Annotation(
                                            text = '1st Tier',
                                            x = 122,
                                            y = 6.5,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '2nd Tier',
                                            x = 122,
                                            y = 26,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '3rd Tier',
                                            x = 122,
                                            y = 50,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '4th Tier',
                                            x = 122,
                                            y = 74,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            xaxis = dict(range = (-0.5, 130.5),
                showgrid=False,
                tickangle=0,
                tickmode = 'array',
                tickvals = [0, 32, 65, 97, 130],
                ),
            yaxis = dict(
                zeroline=False,
                showgrid=False,
                range = (95.5, -0.5),
                tickmode = 'array',
                tickvals = [1, 20, 40, 60, 80],
                title=dict(text='Final League Position', standoff=10),
                ),
            margin=dict(
                l=0,
                r=62,
                t=0,
                b=0,
            ),
            height=180,
        )

        if chosen_team == None:
            pass
        else:

            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df2_team['Season'],
                y=df2_team['HPts'],
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour']),
                        marker=dict(
                            size=2,
                            color=df1_all.at[team, 'colour']),
                        customdata=(df2_team['Pts']),
                        hovertemplate="Season: %{x}<br>" +
                              "Home Points: %{y}<br>" +
                              "Total Points: %{customdata:0f}<br>" +
                              "<extra></extra>",)
            )
            fig.add_trace(go.Scatter(
                x=df2_team['Season'],
                y=df2_team['APts'],
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour_away']),
                        marker=dict(
                            size=2,
                            color=df1_all.at[team, 'colour_away']),
                        customdata=(df2_team['Pts']),
                        hovertemplate="Season: %{x}<br>" +
                              "Away Points: %{y}<br>" +
                              "Total Points: %{customdata:0f}<br>" +
                              "<extra></extra>",)
            )
            fig.add_annotation(go.layout.Annotation(
                text='Home',
                font=dict(color=df1_all.at[team, 'colour']),
                showarrow=False,
                x=10,
                y=54,
            ))
            fig.add_annotation(go.layout.Annotation(
                text='Away',
                font=dict(color=df1_all.at[team, 'colour_away']),
                showarrow=False,
                x=125,
                y=0,
            ))

            fig.update_layout(
                    template='plotly_dark',
                    showlegend=False,
                    xaxis = dict(range = (-0.5, 130.5),
                        showgrid=False,
                        tickangle=0,
                        tickmode = 'array',
                        tickvals = [0, 32, 65, 97, 130],
                        ),
                    yaxis = dict(
                        zeroline=False,
                        showgrid=False,
                        range = (-5, 65),
                        tickmode = 'array',
                        tickvals = [0, 30, 60],
                        title=dict(text='Points', standoff=16),
                        ),
                    margin=dict(
                        l=0,
                        r=62,
                        t=0,
                        b=0,
                    ),
                    height=180,
                )

    elif graph_option == 'Home & Away Points %':

        dff2 = df2['Master']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name='team_trace',
            visible=False,
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_trace(go.Scatter(
            line=dict(color='white'),
            x=dff2['Season'],
            y=dff2['Teams_in_Tier_4'] + dff2['Teams_in_Tier_3'] + dff2['Teams_in_Tier_2'] + dff2['Teams_in_Tier_1'],
            hoverinfo='none'
            ))

        fig.add_annotation(go.layout.Annotation(
                                            text = '1st Tier',
                                            x = 122,
                                            y = 6.5,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '2nd Tier',
                                            x = 122,
                                            y = 26,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '3rd Tier',
                                            x = 122,
                                            y = 50,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.add_annotation(go.layout.Annotation(
                                            text = '4th Tier',
                                            x = 122,
                                            y = 74,
                                            showarrow = False,
                                            valign = 'middle',))

        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            xaxis = dict(range = (-0.5, 130.5),
                showgrid=False,
                tickangle=0,
                tickmode = 'array',
                tickvals = [0, 32, 65, 97, 130],
                ),
            yaxis = dict(
                zeroline=False,
                showgrid=False,
                range = (95.5, -0.5),
                tickmode = 'array',
                tickvals = [1, 20, 40, 60, 80],
                title=dict(text='Final League Position', standoff=15),
                ),
            margin=dict(
                l=0,
                r=62,
                t=0,
                b=0,
            ),
            height=180,
        )

        if chosen_team == None:
            pass
        else:

            team = chosen_team['points'][0]['text']
            team = (team.encode('utf-8')).encode('ascii', 'ignore')
            df2_team = df2[team]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df2_team['Season'],
                y=100 * (df2_team['HPts']/(df2_team['Max_Pts']/2)),
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour']),
                        marker=dict(
                            size=2,
                            color=df1_all.at[team, 'colour']),
                        customdata=100*(df2_team['Pts']/df2_team['Max_Pts']),
                        hovertemplate="Season: %{x}<br>" +
                              "Home Points (as % of max): %{y:0f}<br>" +
                              "Total Points (as % of max): %{customdata:0f}<br>" +
                              "<extra></extra>",)
            )
            fig.add_trace(go.Scatter(
                x=df2_team['Season'],
                y=100 * (df2_team['APts']/(df2_team['Max_Pts']/2)),
                mode='lines+markers',
                line=dict(color=df1_all.at[team, 'colour_away']),
                        marker=dict(
                            size=2,
                            color=df1_all.at[team, 'colour_away']),
                        customdata=100*(df2_team['Pts']/df2_team['Max_Pts']),
                        hovertemplate="Season: %{x}<br>" +
                              "Away Points (as % of max): %{y:0f}<br>" +
                              "Total Points (as % of max): %{customdata:0f}<br>" +
                              "<extra></extra>",)
            )
            fig.add_annotation(go.layout.Annotation(
                text='Home',
                font=dict(color=df1_all.at[team, 'colour']),
                showarrow=False,
                x=10,
                y=87,
            ))
            fig.add_annotation(go.layout.Annotation(
                text='Away',
                font=dict(color=df1_all.at[team, 'colour_away']),
                showarrow=False,
                x=125,
                y=3,
            ))

            fig.update_layout(
                    template='plotly_dark',
                    showlegend=False,
                    xaxis = dict(range = (-0.5, 130.5),
                        showgrid=False,
                        tickangle=0,
                        tickmode = 'array',
                        tickvals = [0, 32, 65, 97, 130],
                        ),
                    yaxis = dict(
                        zeroline=False,
                        showgrid=False,
                        range = (-5, 105),
                        tickmode = 'array',
                        tickvals = [0, 50, 100],
                        title=dict(text='Points (% of max)' , standoff=10),
                        ),
                    margin=dict(
                        l=0,
                        r=62,
                        t=0,
                        b=0,
                    ),
                    height=180,
                )


    return fig


@app.callback(
    Output('team-info', 'children'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    if chosen_team == None:
        raise PreventUpdate
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        text = """Nickname: %s\nEst. %s\nEntered League: %s\nCurrent status: \n%s
            """ % (df1_all.at[team, 'nickname'], int(df1_all.at[team, 'founded']), int(df1_all.at[team, 'entered_league']), df1_all.at[team, 'current_status'])

        return text

@app.callback(
    Output('line', 'figure'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    fig = go.Figure()

    fig.update_layout(
        margin=go.layout.Margin(
                l=0,
                r=0,
                b=4,
                t=0,
        ),
        xaxis=dict(range=(0, 0),
                       visible=False,
                       showgrid=False,
                       showticklabels=False,),
        yaxis=dict(range=(0, 0),
                      visible=False,
                      showgrid=False,
                      showticklabels=False,),
        height=10,
        plot_bgcolor='#111111',
        paper_bgcolor='white',
    )
    if chosen_team == None:
        pass
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')
        team_primary_color = df1_all.at[team, 'colour']

        fig.update_layout(
        paper_bgcolor=team_primary_color,
        )

    return fig

@app.callback(
    Output('chosen-team-wiki', 'style'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    if chosen_team == None:
        raise PreventUpdate
    else:
        return {'color':'white', 'textAlign':'left', 'fontSize': '13'}

@app.callback(
    Output('chosen-team-website', 'style'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    if chosen_team == None:
        raise PreventUpdate
    else:
        return {'color':'white', 'textAlign':'right', 'fontSize': '13',}

@app.callback(
    Output('chosen-team', 'children'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    if chosen_team == None:
        return 'Pick a team'
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')

        return '{} \n{}'.format(team, df1_all.at[team, 'suffix'])

@app.callback(
    Output('chosen-team', 'style'),
    [Input('Map', 'clickData')])
def update_output(chosen_team):
    if chosen_team == None:
        raise PreventUpdate
    else:
        return {'paddingTop': '2px', 'paddingBottom': '2px', 'fontSize': '19px',
                'textAlign': 'center', 'height': '78px', 'verticalAlign': 'middle',
                'whiteSpace':'pre-wrap'}

@app.callback(
    Output('chosen-team-wiki', 'href'),
    [Input('Map', 'clickData')])
def wiki_generator(chosen_team):
    if chosen_team == None:
        return None
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')
        wiki_link = df1_all.at[team, 'wiki']

        return wiki_link

@app.callback(
    Output('chosen-team-website', 'href'),
    [Input('Map', 'clickData')])
def website_generator(chosen_team):
    if chosen_team == None:
        return None
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')
        website_link = df1_all.at[team, 'website']

        return website_link

@app.callback(
    Output('Map', 'figure'),
    [Input('L-NL-D-option', 'value'),
    Input('Map', 'clickData')])
def map_generator(league_option, chosen_team):
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
            name='update_1',
            visible=False,
            lat=[1],
            lon=[1],
            mode='markers',
            marker=dict(
                symbol='circle',
                size=16,
                color='black'
            ),
            text=['1'],
            hovertemplate="%{text}<br>" +
                      "<extra></extra>",
        ))

    if league_option == 'All':
        fig.add_trace(go.Scattermapbox(
                lat=df1['League_Teams']['lat'],
                lon=df1['League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=7,
                    color='black'
                ),
                text=df1['League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['League_Teams']['lat'],
                lon=df1['League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df1['League_Teams']['colour']
                ),
                text=df1['League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['Non-League_Teams']['lat'],
                lon=df1['Non-League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=7,
                    color='black'
                ),
                text=df1['Non-League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['Non-League_Teams']['lat'],
                lon=df1['Non-League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df1['Non-League_Teams']['colour']
                ),
                text=df1['Non-League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['Defunct_Teams']['lat'],
                lon=df1['Defunct_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=7,
                    color='black'
                ),
                text=df1['Defunct_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['Defunct_Teams']['lat'],
                lon=df1['Defunct_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df1['Defunct_Teams']['colour']
                ),
                text=df1['Defunct_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))

    elif league_option == 'League':
        fig.add_trace(go.Scattermapbox(
                lat=df1['League_Teams']['lat'],
                lon=df1['League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=7,
                    color='black'
                ),
                text=df1['League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['League_Teams']['lat'],
                lon=df1['League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df1['League_Teams']['colour']
                ),
                text=df1['League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))

    elif league_option == 'Non-League':
        fig.add_trace(go.Scattermapbox(
                lat=df1['Non-League_Teams']['lat'],
                lon=df1['Non-League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=7,
                    color='black'
                ),
                text=df1['Non-League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['Non-League_Teams']['lat'],
                lon=df1['Non-League_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df1['Non-League_Teams']['colour']
                ),
                text=df1['Non-League_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))

    elif league_option == 'Defunct':
        fig.add_trace(go.Scattermapbox(
                lat=df1['Defunct_Teams']['lat'],
                lon=df1['Defunct_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=7,
                    color='black'
                ),
                text=df1['Defunct_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))
        fig.add_trace(go.Scattermapbox(
                lat=df1['Defunct_Teams']['lat'],
                lon=df1['Defunct_Teams']['lon'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df1['Defunct_Teams']['colour']
                ),
                text=df1['Defunct_Teams']['Team'],
                hovertemplate="%{text}<br>" +
                          "<extra></extra>",
            ))

    fig.update_layout(
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=4,
            t=4,
        ),
        paper_bgcolor='white',
        height=350,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            domain=go.layout.mapbox.Domain(
                x=[0, 1],
                y=[0, 1]),

            accesstoken=mapbox_access_token,
            style='mapbox://styles/apvm/ck5jrhhxx0r8e1ijyjktgefqh',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=53.0,
                lon=-2
            ),
            pitch=0,
            zoom=4.6,
            uirevision=False,
        )
        )

    if chosen_team == None:
        return fig
    else:
        team = chosen_team['points'][0]['text']
        team = (team.encode('utf-8')).encode('ascii', 'ignore')
        team_primary_color = df1_all.at[team, 'colour']

        fig.update_layout(
        paper_bgcolor=team_primary_color,
        )

        return fig






if __name__ == '__main__':
    app.run_server(debug=True)
