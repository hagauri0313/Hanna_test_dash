## install dash
from dash import Dash, Input, Output, html, dcc, callback # need version dash 2.0.0 or higher
import plotly.express as px
import base64
from Bio import SeqIO

### style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### create dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)

###Application layout
app.layout = html.Div([
    html.Br(),
    ### web app title
    html.H1(children='FASTA Analysis', style={'textAlign': 'center'
        }),
    html.Br(), html.Hr(),

    ###upload button for fasta file
    dcc.Upload(html.Button('Upload Fasta File'), id='input_seq',
           style={'margin-left' : '365px','width' : '50%', 'textAlign': 'center'}),
    html.Hr(), html.Br(),

    ###display output : number of sequences as fasta_output1
    html.Div(id='fasta_output1', style={'textAlign': 'center','fontsize':50,'margin-left' : '100px'}), html.Br(),

    ###drop down menu for selecting sequence header
    dcc.Dropdown( id='dd_input', placeholder="Select a seequence"),
    html.Div(id='dd_output')
])


### first interactiveinteractive
@app.callback(
    Output(component_id='fasta_output1', component_property='children'),
    Input(component_id='input_seq', component_property='contents')
)

###parse fasta file
### print the number of sequences
def parse_fasta(input_contents):
    if input_contents is not None:
        data=base64.b64decode(input_contents.split(',')[-1].encode('ascii')).decode()

        num = len([1 for line in data if line.startswith(">")])
        return "The number of sequences contained in the file is " + str(num)

###second interactive component
@app.callback(
    Output(component_id='dd_input', component_property='options'),
    Input(component_id='input_seq', component_property='contents')
)

###find header from fasta sequence.
def get_header(input_contents):
    if input_contents is not None:
        data=base64.b64decode(input_contents.split(',')[-1].encode('ascii')).decode()
        text=open('Seqlist','w')
        n=text.write(data)
        text.close()

        headers = []
        with open("Seqlist", "r") as f:
            for record in SeqIO.parse(f, "fasta"):
                headers.append(record.description)
        return headers



if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


