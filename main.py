import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Sound Item Dashboard'),
    dcc.Graph(id='plays-graph'),
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records')
    ),
    html.Div([
        html.H3('Completion Rate'),
        dcc.Progress(id='completion-bar', value=0, max=100),
    ])
])

@app.callback(
    dash.dependencies.Output('plays-graph', 'figure'),
    [dash.dependencies.Input('table', 'data')])
def update_graph(data):
    df = pd.DataFrame.from_dict(data)
    return {
        'data': [go.Bar(
            x=df['title'],
            y=df['unique_plays'],
            name='Unique Plays'
        ), go.Bar(
            x=df['title'],
            y=df['total_plays'],
            name='Total Plays'
        )],
        'layout': go.Layout(
            title='Unique and Total Plays by Sound Item',
            xaxis={'title': 'Sound Item'},
            yaxis={'title': 'Number of Plays'}
        )
    }

@app.callback(
    dash.dependencies.Output('completion-bar', 'value'),
    [dash.dependencies.Input('table', 'data')])
    
def update_progress(data):
    df = pd.DataFrame.from_dict(data)
    return df['completion_rate'].mean()

if __name__ == '__main__':
    app.run_server(debug=True)
