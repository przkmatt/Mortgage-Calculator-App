import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State  # pip install dash (version 2.0.0 or higher)
from plotly.subplots import make_subplots
from default_calc import current_day, current_month, current_year, current_date, home_price_default, down_payment_default, \
    loan_time_default, interest_rate_default, pmi_rate_default, additional_payment_default, loan_rem_default, loan_pay_default, \
    pmi_amt_default, mort_amt_default, tax_amt_default, loan_start_default, pie_one_labels_add, pie_one_values_add, pie_one_labels, \
    pie_one_values, pie_two_labels_add, pie_two_values_add, pie_two_labels, pie_two_values, value_int_paid, value_int_paid_add, \
    df_year_graph, value_tot_paid_save, df_add_year_graph


#create pie charts with values and labels
pie_one_add = go.Figure(data=[go.Pie(labels=pie_one_labels_add, values=pie_one_values_add, sort=False)])
pie_one = go.Figure(data=[go.Pie(labels=pie_one_labels, values=pie_one_values, sort=False)])
pie_two_add = go.Figure(data=[go.Pie(labels=pie_two_labels_add, values=pie_two_values_add)])
pie_two = go.Figure(data=[go.Pie(labels=pie_two_labels, values=pie_two_values)])

#craete bar graph to show differences in payment
bar_chart = go.Figure(data=[
    go.Bar(name='Default Loan', x=['Interest Paid'], y=[value_int_paid]),
    go.Bar(name='With additional payment', x=['Interest Paid'], y=[value_int_paid_add])
])
bar_chart.update_layout(barmode='group', bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1, title='Reduction to Interest Paid', title_y=.8,
    xaxis_fixedrange=True,
    yaxis_fixedrange=True)
bar_chart.add_annotation(
    go.layout.Annotation(
        x=.1,
        y=(value_int_paid_add+value_int_paid)/2,
        ax=40,
        ay=0,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
        ),
        bgcolor="#F10000",
        showarrow=False,
        text=str(round((1-(value_int_paid/value_int_paid_add))*100, 2))+"%")
    )

#FIGURE


fig=make_subplots()
fig.add_trace(go.Scatter(x=df_year_graph["PAYMENT YEAR"], y=df_year_graph["ENDING BALANCE"], name="Default Loan"))
if value_tot_paid_save != 0:
    fig.add_trace(go.Scatter(x=df_add_year_graph["PAYMENT YEAR"], y=df_add_year_graph["ENDING BALANCE"], name="With Additional Payment"))
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Principle Remaining",
    xaxis_fixedrange=True,
    yaxis_fixedrange=True,
    #paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(240,240,240,.5)',
    legend_orientation="h",
    legend_y=1.15
)

layout = html.Div(
    children=[
        #Header
        html.Div(
            children=[
                html.H1(
                    children="Matt's Mortgage Calculator", className="header-title"
                ),
            ],
            className="header",
        ),

        #Chart
        dcc.Graph(id="line-chart", figure=fig, config={'displayModeBar': False}, className='chart'),

        #All boxes for Flex
        html.Div(
            children=[
                #Menu
                html.Nobr(
                    children=[
                        dcc.RadioItems(id='loan_option',
                            options=[
                                {'label': 'I already have my loan!', 'value': 'loan'},
                                {'label': 'I need to calculate my loan!', 'value': 'noloan'},
                            ],
                            value='loan',
                            labelStyle={'display': 'inline-block'},
                            className='loan_option'
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                                html.Nobr(id='text1', children='Home Price: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row1',
                                    type='text',
                                    placeholder=home_price_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='$', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text2', children='Principal Remaining: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row2',
                                    type='text',
                                    placeholder=loan_rem_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(id='menu-row-right-2', children='$', className='menu-row-right'),
                                dcc.RadioItems(
                                    id='dollarpercent',
                                    options=[
                                       {'label': '$', 'value': 'dollar'},
                                       {'label': '%', 'value': 'percent'},
                                    ],
                                    value='percent',
                                    style={'display': 'none'},
                                    className='menu-row-right'
                                ),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text3', children='Monthly Payment(Loan only): ', className='menu-row-title'),
                                dcc.Input(
                                    id='row3',
                                    type='text',
                                    placeholder=loan_pay_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='$', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text4', children='Interest Rate: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row4',
                                    type='text',
                                    placeholder=interest_rate_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='%', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text5', children='PMI Monthly Payment: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row5',
                                    type='text',
                                    placeholder=pmi_amt_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='$', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text6', children='Mortgage Insurance: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row6',
                                    type='text',
                                    placeholder=mort_amt_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='$/yr', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text7', children='Property Tax: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row7',
                                    type='text',
                                    placeholder=tax_amt_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='$/yr', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text8', children='Additional Monthly Payment: ', className='menu-row-title'),
                                dcc.Input(
                                    id='row8',
                                    type='text',
                                    placeholder=additional_payment_default,
                                    className='menu-row-input'
                                ),
                                html.Nobr(children='$', className='menu-row-right'),
                            ],
                            className='menu-row'
                        ),
                        html.Div(
                            children=[
                                html.Nobr(id='text9', children='Loan Start Date: ', className='menu-row-title'),
                                dcc.Dropdown(
                                    id='date_dropdown',
                                    options=[
                                        {'label': 'Jan', 'value': 1},
                                        {'label': 'Feb', 'value': 2},
                                        {'label': 'Mar', 'value': 3},
                                        {'label': 'Apr', 'value': 4},
                                        {'label': 'May', 'value': 5},
                                        {'label': 'Jun', 'value': 6},
                                        {'label': 'Jul', 'value': 7},
                                        {'label': 'Aug', 'value': 8},
                                        {'label': 'Sep', 'value': 9},
                                        {'label': 'Oct', 'value': 10},
                                        {'label': 'Nov', 'value': 11},
                                        {'label': 'Dec', 'value': 12},
                                    ],
                                    value=current_month,
                                    clearable=False,
                                    className='date-dropdown'
                                ),
                                dcc.Input(
                                    id='row9',
                                    type='text',
                                    value=current_year,
                                    className='menu-row-input'
                                ),
                            ],
                            id='loan-date',
                            className='menu-row',
                            #style={'display': 'none'},
                        ),
                        html.Button('Calculate', id='calc-button', n_clicks=0)
                    ],
                    className='menu'
                ),
                #STORED DATA

                dcc.Store(id='amort_schd'),
                dcc.Store(id='amort_schd_add'),

                #Compare
                html.Div(
                    children=[
                        html.Div(children='Comparison Summary', className='box-title'),
                        # each box that contains the info
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='compare-top-1',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='compare-bottom-1',
                                    children='Saved from 14 PMI Payments',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='compare-top-2',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='compare-bottom-2',
                                    children='PMI Time Saved',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='compare-top-3',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='compare-bottom-3',
                                    children='Saved from 54 Payments',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='compare-top-4',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='compare-bottom-4',
                                    children='Loan Time Saved',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='compare-top-5',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='compare-bottom-5',
                                    children='Total Interest Saved',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='compare-top-6',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='compare-bottom-6',
                                    children='Total Escrow Saved',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        dcc.Graph(id='compare-chart', figure=bar_chart, config={'displayModeBar': False}, className='compare-chart')
                    ],
                    id='box-compare',
                    className='compare',
                    #style={'display': 'none'},
                ),
                #No additional payment box
                html.Div(
                    children=[
                        html.Div(children='No Additional Payment',className='box-title'),
                        #each box that contains the info
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-1',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-1',
                                    children='Monthly Payment w/ Escrow & PMI',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-2',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-2',
                                    children='After 66 Months',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-3',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-3',
                                    children='Loan Only Monthly Payment',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-4',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-4',
                                    children='66 PMI Payments',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-5',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-5',
                                    children='Total PMI Paid',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-6',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-6',
                                    children='PMI Pay off Date',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-7',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-7',
                                    children='Annual Payment Amount',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-8',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-8',
                                    children='Loan Pay Off Date',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-9',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-9',
                                    children='Down Payment Amount',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-10',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-10',
                                    children='Down Payment Percentage',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-11',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-11',
                                    children='Total Interest Paid',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-12',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-12',
                                    children='Total Tax Paid',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-13',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-13',
                                    children='Total Mortgage Insurance',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='no-add-top-14',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='no-add-bottom-14',
                                    children='Total of 360 Payments',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        dcc.RadioItems(id='no-add-pie-graph',
                            options=[
                                {'label': 'Monthly Payment', 'value': 'month'},
                                {'label': 'Total Cost', 'value': 'total'},
                            ],
                            value='month',
                            labelStyle={'display': 'inline-block'},
                            className='pie-option'
                        ),
                        dcc.Graph(id='pie', figure=pie_one, config={'displayModeBar': False}, className='pie')
                    ],
                    id='box-no-add',
                    className='no-add'
                ),
                #ADDitional payment box
                html.Div(
                    children=[
                        html.Div(children='Additional Payment',className='box-title'),
                        #each box that contains the info
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-1',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-1',
                                    children='Monthly Payment w/ Escrow & PMI',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-2',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-2',
                                    children='After 66 Months',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-3',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-3',
                                    children='Loan Only Monthly Payment',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-4',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-4',
                                    children='66 PMI Payments',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-5',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-5',
                                    children='Total PMI Paid',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-6',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-6',
                                    children='PMI Pay off Date',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-7',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-7',
                                    children='Annual Payment Amount',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-8',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-8',
                                    children='Loan Pay Off Date',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-9',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-9',
                                    children='Down Payment Amount',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-10',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-10',
                                    children='Down Payment Percentage',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-11',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-11',
                                    children='Total Interest Paid',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-12',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-12',
                                    children='Total Tax Paid',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-13',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-13',
                                    children='Total Mortgage Insurance',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        html.Nobr(
                            children=[
                                html.Div(
                                    id='add-top-14',
                                    children='$1,000',
                                    className='box-top'
                                ),
                                html.Div(
                                    id='add-bottom-14',
                                    children='Total of 360 Payments',
                                    className='box-bottom'
                                ),
                            ],
                            className='box'
                        ),
                        dcc.RadioItems(id='add-pie-graph',
                            options=[
                                {'label': 'Monthly Payment', 'value': 'month'},
                                {'label': 'Total Cost', 'value': 'total'},
                            ],
                            value='month',
                            labelStyle={'display': 'inline-block'},
                            className='pie-option'
                        ),
                        dcc.Graph(id='pie-add', figure=pie_one_add, config={'displayModeBar': False}, className='pie-add')
                    ],
                    id='box-add',
                    className='add'
                ),
            ],
            className='all-boxes'
        )
    ],
    className='page'
)