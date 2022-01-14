from datetime import datetime
from datetime import date
from datetime import timedelta
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State  # pip install dash (version 2.0.0 or higher)
from default_calc import current_day, current_month, current_year, current_date, home_price_default, down_payment_default, \
    loan_time_default, interest_rate_default, pmi_rate_default, additional_payment_default, loan_rem_default, loan_pay_default, \
    pmi_amt_default, mort_amt_default, tax_amt_default, loan_start_default, pie_one_labels_add, pie_one_values_add, pie_one_labels, \
    pie_one_values, pie_two_labels_add, pie_two_values_add, pie_two_labels, pie_two_values, value_int_paid, value_int_paid_add, \
    df_year_graph, value_tot_paid_save, df_add_year_graph

def get_callbacks(app):
    #app callback to switch between the two loan options
    @app.callback(
        [Output(component_id='text2', component_property='children'),
         Output(component_id='row2', component_property='placeholder'),
         Output(component_id='text3', component_property='children'),
         Output(component_id='row3', component_property='placeholder'),
         Output(component_id='text5', component_property='children'),
         Output(component_id='row5', component_property='placeholder'),
         Output(component_id='dollarpercent', component_property='style'),
         Output(component_id='menu-row-right-2', component_property='style'),
         Output(component_id='loan-date', component_property='style'),
         ],
        [Input(component_id='loan_option', component_property='value')
         ]
    )
    def choose_loan_type(option_sel):
        if option_sel == 'noloan':
            text2 = 'Down Payment: '
            row2 = down_payment_default
            text3 = 'Loan Length: '
            row3 = loan_time_default
            text5 = 'PMI Rate (%): '
            row5 = pmi_rate_default
            percent_option = 'block'
            right_row = 'none'
            loan_date = 'flex'
        else:
            text2 = 'Principal Remaining: '
            row2 = loan_rem_default
            text3 = 'Monthly Payment(Loan only): '
            row3 = loan_pay_default
            text5 = 'PMI Monthly Payment: '
            row5 = pmi_amt_default
            percent_option = 'none'
            right_row = 'block'
            loan_date = 'none'
        return text2, row2, text3, row3, text5, row5, {'display': percent_option}, {'display': right_row}, \
               {'display': loan_date},

    #app callback to run the program and return the graph and df to download
    @app.callback(
        [Output('amort_schd', 'data'),
         Output('amort_schd_add', 'data')
         ],
        [Input(component_id='calc-button', component_property='n_clicks')
         ],
        [State(component_id='loan_option', component_property='value'),
         State(component_id='row1', component_property='value'),
         State(component_id='row2', component_property='value'),
         State(component_id='row3', component_property='value'),
         State(component_id='row4', component_property='value'),
         State(component_id='row5', component_property='value'),
         State(component_id='row6', component_property='value'),
         State(component_id='row7', component_property='value'),
         State(component_id='row8', component_property='value'),
         State(component_id='date_dropdown', component_property='value'),
         State(component_id='row9', component_property='value'),
         ]
    )
    def calc_df(click, loan_type, value1, value2, value3, value4, value5, value6, value7, value8, date_dropdown, row9):
        #initial run set to value
        if value1 is None:
            value1=home_price_default
            value2=loan_rem_default
            value3=loan_pay_default
            value4=interest_rate_default
            value5=pmi_amt_default
            value6=mort_amt_default
            value7=tax_amt_default
            value8=additional_payment_default

        #calculating the loan with first principles and putting it into a dataframe
        if loan_type == 'noloan':
            home_price = float(value1)
            down_pay = float(value2)
            loan_time = float(value3)
            interest = float(value4)
            pmi_rate = float(value5)
            mtg_ins_yr = float(value6)
            tax_amt_yr = float(value7)
            add_pay = float(value8)
            loan_start = date(row9, date_dropdown, 15)
        else:
            home_price = float(value1)
            loan_rem = float(value2)
            loan_pay = float(value3)
            interest = float(value4)
            pmi_amt = float(value5)
            mtg_ins_yr = float(value6)
            tax_amt_yr = float(value7)
            add_pay = float(value8)
        if loan_type == 'noloan':
            df_add = pd.read_csv('Mortgage.csv')
            df = pd.read_csv('Mortgage.csv')
            pmt_no = 1
            interest_mth = interest / 100 / 12
            discount = interest_mth / (1 + interest_mth)
            payment_date = current_date
            beginning_bal = home_price - down_pay
            scheduled_pay = beginning_bal * (interest_mth * math.pow((1 + interest_mth), loan_time * 12)) / (
                        math.pow((1 + interest_mth), loan_time * 12) - 1)
            extra_pay = add_pay
            total_pay = scheduled_pay + add_pay
            mort_ins = mtg_ins_yr / 12
            tax_pay = tax_amt_yr / 12
            lvt = (home_price - down_pay) / home_price
            months_left = round(
                math.log(-total_pay / ((beginning_bal * interest_mth) - total_pay)) / math.log(1 + interest_mth), 0)
            while pmt_no <= months_left:
                ending_bal = beginning_bal - ((scheduled_pay + extra_pay) - beginning_bal * interest_mth)
                interest_pay = beginning_bal * interest_mth
                principal_pay = total_pay - interest_pay
                lvt = ending_bal / home_price
                if lvt > .8:
                    pmi_pay = pmi_rate * (home_price - down_pay) / 12 / 100
                else:
                    pmi_pay = 0
                total_pay_w_esc = scheduled_pay + extra_pay + mort_ins + pmi_pay + tax_pay
                payment_date_shown = loan_start + timedelta(days=pmt_no / 12 * 365.25)
                payment_date_shown = payment_date_shown.replace(day=1)
                df_add.loc[len(df_add.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2),
                                                 round(scheduled_pay, 2), round(extra_pay, 2), round(total_pay, 2),
                                                 round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2),
                                                 round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2),
                                                 round(total_pay_w_esc, 2)]
                beginning_bal = ending_bal
                pmt_no = pmt_no + 1

            # reframing for no additional payment dataframe
            pmt_no = 1
            beginning_bal = home_price - down_pay
            extra_pay = 0
            total_pay = scheduled_pay
            lvt = (home_price - down_pay) / home_price
            months_left = round(
                math.log(-total_pay / ((beginning_bal * interest_mth) - total_pay)) / math.log(1 + interest_mth), 0)
            while pmt_no <= months_left:
                ending_bal = beginning_bal - ((scheduled_pay + extra_pay) - beginning_bal * interest_mth)
                interest_pay = beginning_bal * interest_mth
                principal_pay = total_pay - interest_pay
                lvt = ending_bal / home_price
                if lvt > .8:
                    pmi_pay = pmi_rate * (home_price - down_pay) / 12 / 100
                else:
                    pmi_pay = 0
                total_pay_w_esc = scheduled_pay + extra_pay + mort_ins + pmi_pay + tax_pay
                payment_date_shown = loan_start + timedelta(days=pmt_no / 12 * 365.25)
                payment_date_shown = payment_date_shown.replace(day=1)
                df.loc[len(df.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2),
                                         round(extra_pay, 2), round(total_pay, 2),
                                         round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2),
                                         round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2),
                                         round(total_pay_w_esc, 2)]
                beginning_bal = ending_bal
                pmt_no = pmt_no + 1
        else:
            # inserting into dataframe with given information
            df_add = pd.read_csv('Mortgage.csv')
            df = pd.read_csv('Mortgage.csv')
            pmt_no = 1
            interest_mth = interest / 100 / 12
            discount = interest_mth / (1 + interest_mth)
            payment_date = current_date
            beginning_bal = loan_rem
            scheduled_pay = loan_pay
            extra_pay = add_pay
            total_pay = scheduled_pay + add_pay
            mort_ins = mtg_ins_yr / 12
            tax_pay = tax_amt_yr / 12
            lvt = loan_rem / home_price
            months_left = round(
                math.log(-total_pay / ((beginning_bal * interest_mth) - total_pay)) / math.log(1 + interest_mth), 0)
            while pmt_no <= months_left:
                ending_bal = beginning_bal - ((scheduled_pay + extra_pay) - beginning_bal * interest_mth)
                interest_pay = beginning_bal * interest_mth
                principal_pay = total_pay - interest_pay
                lvt = ending_bal / home_price
                if lvt > .8:
                    pmi_pay = pmi_amt
                else:
                    pmi_pay = 0
                total_pay_w_esc = scheduled_pay + extra_pay + mort_ins + pmi_pay + tax_pay
                payment_date_shown = current_date + timedelta(days=pmt_no / 12 * 365.25)
                payment_date_shown = payment_date_shown.replace(day=1)
                df_add.loc[len(df_add.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2),
                                                 round(scheduled_pay, 2), round(extra_pay, 2), round(total_pay, 2),
                                                 round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2),
                                                 round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2),
                                                 round(total_pay_w_esc, 2)]
                beginning_bal = ending_bal
                pmt_no = pmt_no + 1

            # reframing for no additional payment dataframe
            pmt_no = 1
            beginning_bal = loan_rem
            extra_pay = 0
            total_pay = scheduled_pay
            lvt = loan_rem / home_price
            months_left = round(
                math.log(-total_pay / ((beginning_bal * interest_mth) - total_pay)) / math.log(1 + interest_mth), 0)
            while pmt_no <= months_left:
                ending_bal = beginning_bal - ((scheduled_pay + extra_pay) - beginning_bal * interest_mth)
                interest_pay = beginning_bal * interest_mth
                principal_pay = total_pay - interest_pay
                lvt = ending_bal / home_price
                if lvt > .8:
                    pmi_pay = pmi_amt
                else:
                    pmi_pay = 0
                total_pay_w_esc = scheduled_pay + extra_pay + mort_ins + pmi_pay + tax_pay
                payment_date_shown = current_date + timedelta(days=pmt_no / 12 * 365.25)
                payment_date_shown = payment_date_shown.replace(day=1)
                df.loc[len(df.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2),
                                         round(extra_pay, 2), round(total_pay, 2),
                                         round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2),
                                         round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2),
                                         round(total_pay_w_esc, 2)]
                beginning_bal = ending_bal
                pmt_no = pmt_no + 1
        df.to_json(path_or_buf='df.json')
        return df.to_json(orient='columns'), df_add.to_json(orient='columns')

    # app callback to convert df to figure
    @app.callback(
        [Output(component_id='line-chart', component_property='figure'),
         ],
        [Input('amort_schd', 'data'),
         Input('amort_schd_add', 'data')
         ],
    )
    def calc_df(amort_schd, amort_schd_add):
        # convert to yearly dataframes
        df_add_year = pd.read_json(amort_schd_add, orient='columns')
        df_add_year['PAYMENT YEAR'] = pd.DatetimeIndex(df_add_year['PAYMENT DATE']).year
        df_add_year_graph = df_add_year[pd.DatetimeIndex(df_add_year['PAYMENT DATE']).month == 12]
        df_add_year = df_add_year.drop(columns=['PMT NO', 'PAYMENT DATE'])
        df_add_year = df_add_year.groupby(['PAYMENT YEAR']).sum()

        df_year = pd.read_json(amort_schd, orient='columns')
        df_year['PAYMENT YEAR'] = pd.DatetimeIndex(df_year['PAYMENT DATE']).year
        df_year_graph = df_year[pd.DatetimeIndex(df_year['PAYMENT DATE']).month == 12]
        df_year = df_year.drop(columns=['PMT NO', 'PAYMENT DATE'])
        df_year = df_year.groupby(['PAYMENT YEAR']).sum()
        df_year_graph.to_csv(path_or_buf='df_year.csv')
        # df_add_year_graph.to_csv(path_or_buf='df_add_year.csv')

        fig = make_subplots()
        fig.add_trace(
            go.Scatter(x=df_year_graph["PAYMENT YEAR"], y=df_year_graph["ENDING BALANCE"], name="Default Loan"))
        if value_tot_paid_save != 0:
            fig.add_trace(go.Scatter(x=df_add_year_graph["PAYMENT YEAR"], y=df_add_year_graph["ENDING BALANCE"],
                                     name="With Additional Payment"))
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Principle Remaining",
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            # paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(240,240,240,.5)',
            legend_orientation="h",
            legend_y=1.15
        )
        return fig
