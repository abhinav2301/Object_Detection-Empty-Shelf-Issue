import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import os
from shutil import copyfile
import shutil
import csv
import pprint

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

list1=['Id', 'Name','Quantiy', 'Below Threshold']
count_class = 0
kitems = []
k = 0
temp1 = []
Category = []
Sub_Category = []
Ritems = []
Eitems = []
global thitems
global z
z = []
values = []

with open('SKU.csv', 'r')as f:
    data = csv.reader(f)
    for i in data:
        kitems.append(i)
kitems = kitems[1:]

for i in kitems:
    if i[0] not in Category:
        Category.append(i[0])
for i in range(0, len(Category)):
    temp = []
    for j in range(0, len(kitems)):
        if kitems[j][0] == Category[i] and kitems[j][1] not in temp:
            temp.append(kitems[j][1])
    Sub_Category.append(temp)
fnameDict = dict(zip(Category, Sub_Category))

names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

app.layout = html.Div(
    [html.H2('Image Detection'),
        html.Div([
            html.H6('Select Category', style={'display': 'inline-block','padding-left': '15%'}),
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label': name, 'value': name} for name in names],
                value=list(fnameDict.keys())[0]
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'margin': '5px','padding-left': '15%'}),
        html.Div([
            #html.H6(children='Count:',style={'textAlign':'right','padding-left':'150%','display': 'inline-block'}),
            html.H6('Select Sub-Category', style={'display': 'inline-block'}),
            dcc.Dropdown(
                id='opt-dropdown',
            ),
        ], style={'padding-left': '5%', 'width': '20%', 'display': 'inline-block', 'margin': '5px'},
    ),
        
        html.Div([
        dcc.Graph(
        id='graph',style={'display': 'inline-block'}),

        html.H6(children='Count:', style={
                 'margin': '5px', 'display': 'inline-block','padding-left': '15%'}),
        dash_table.DataTable(
        id='editing-prune-data',
        columns=[{
            'name': '{}'.format(list1[i]),
            'id': 'column-{}'.format(i),
            'deletable': True
        } for i in range(4)],
        
        data=[
            {'column-{}'.format(i-2): kitems[0][i] for i in range(2,5)}
            
        ],style_table={ 'padding-left': '30%', 'maxHeight': '400px','overflowY': 'scroll','display': 'inline-block'},
        
        editable=True,
       
       
    )]),
       
        
       
        html.Div(id='time-stamp', style={'padding-left': '35%',
                                         'width': '20%', 'display': 'inline-block', 'margin': '10px'}),
        html.Hr(),
        html.Button('Refresh', id='button'),
        html.Div(id='container-button-basic',
                 style={'margin': '5px', 'display': 'inline-block', 'padding-left': '3%'})

        

    
    ]
)


@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('name-dropdown', 'value')]
)
def update_date_dropdown(name):
    a = name
    return [{'label': i, 'value': i} for i in fnameDict[name]]


@app.callback( dash.dependencies.Output('editing-prune-data', 'data'),
    [dash.dependencies.Input('opt-dropdown', 'value')],
    [dash.dependencies.State('name-dropdown', 'value')
    ,dash.dependencies.State('editing-prune-data', 'data')])

def display_output(a,b,rows):
    

    Ritems = []

    with open('Results.csv', 'r')as h4:
        data5 = csv.reader(h4)
        for i in data5:
            Ritems.append(i)
    flist = ''
    tlist = ''
    rows=[]
    threslist=[]
    item_list = []
    id_list = []
    qlist = []
    for i in kitems:
        if b == i[0] and a == i[1]:
            item_list.append(i[3])
            id_list.append(i[2])
    for i in range(len(item_list)):
        qlist.append(0)
        threslist.append('No')
    for i in Ritems:
        for j in range(0, len(i)):
            if i[j] in item_list:
                qlist[item_list.index(i[j])]=Ritems[len(Ritems)-1][j]
                if int(Ritems[len(Ritems)-1][j]) < 2:
                    threslist[item_list.index(i[j])]='Yes'
    for j in range(0,len(item_list)):
        rows.append(
            {'column-0' : id_list[j],
             'column-1' : item_list[j],
             'column-2' : qlist[j],
             'column-3' : threslist[j]} 
            
        ),

    return rows

@app.callback(
    dash.dependencies.Output('time-stamp', 'children'),
    [dash.dependencies.Input('opt-dropdown', 'value')])
def update(val):
    R2items = []
    with open('Results.csv', 'r')as h2:
        data3 = csv.reader(h2)
        for i in data3:
            R2items.append(i)
    tlist = 'Time Stamp : '+str(R2items[len(R2items)-1][0])
    return "{}".format(tlist)



@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_output(n_clicks):
    Eitems = []
    try:
        with open('Bound_Error.csv', 'r')as g:
            data1 = csv.reader(g)
            for i in data1:
                Eitems.append(i)
        Elist = ''
        for i in Eitems:
            Elist += str(i)[2:-2]+', '
        Elist = Elist[:-2]
        return "The Items Out of Bound are : {}".format(Elist)
    except:
        return "No Error in Placement of Products"


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('opt-dropdown', 'value')],
    [dash.dependencies.State('name-dropdown', 'value')])
def update_output4(e, f):
    z = []
    f2list = ''
    t2list = ''
    x = [1]
    t = 'bar'
    item_count = []
    atr = ['x', 'y', 'type', 'name']
    item_list2 = []
    for i in kitems:
        if f == i[0] and e == i[1]:
            item_list2.append(i[3])
            item_count.append(i[4])
    for i in range(0, len(item_list2)):
        a = []
        b = []
        a.append(x)
        b.append(item_count[i])
        a.append(b)
        a.append(t)
        a.append(item_list2[i])
        dic = dict(zip(atr, a))
        z.append(dic)
    return {
        'data': z,
        'layout': {
            'title': 'Item Stock Count'
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
