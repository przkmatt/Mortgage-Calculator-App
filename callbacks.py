from datetime import datetime
from datetime import date
from datetime import timedelta
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State  # pip install dash (version 2.0.0 or higher)
from default_calc import home_price_default, down_payment_default, \
    loan_time_default, interest_rate_default, pmi_rate_default, additional_payment_default, loan_rem_default, loan_pay_default, \
    pmi_amt_default, mort_amt_default, tax_amt_default
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
        if value2 is None:
            value2=loan_rem_default
        if value3 is None:
            value3=loan_pay_default
        if value4 is None:
            value4=interest_rate_default
        if value5 is None:
            value5=pmi_amt_default
        if value6 is None:
            value6=mort_amt_default
        if value7 is None:
            value7=tax_amt_default
        if value8 is None:
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
            loan_start = date(row9, date_dropdown, 15)
        if loan_type == 'noloan':
            df_add = pd.read_csv('Mortgage.csv')
            df = pd.read_csv('Mortgage.csv')
            pmt_no = 1
            interest_mth = interest / 100 / 12
            discount = interest_mth / (1 + interest_mth)
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
                payment_date_shown = loan_start + timedelta(days=pmt_no / 12 * 365.25)
                payment_date_shown = payment_date_shown.replace(day=1)
                df.loc[len(df.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2),
                                         round(extra_pay, 2), round(total_pay, 2),
                                         round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2),
                                         round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2),
                                         round(total_pay_w_esc, 2)]
                beginning_bal = ending_bal
                pmt_no = pmt_no + 1
        df.to_csv(path_or_buf='df.csv')
        df_add.to_csv(path_or_buf='df_add.csv')
        return df.to_dict(orient='records'), df_add.to_dict(orient='records')

    # app callback to convert df to figure
    @app.callback(
        Output(component_id='line-chart', component_property='figure'),
        [Input('amort_schd', 'data'),
         Input('amort_schd_add', 'data')
         ],
    )
    def line_fig(amort_schd, amort_schd_add):
        # convert to yearly dataframes
        df_add_year = pd.DataFrame.from_dict(amort_schd_add, orient='columns')
        row_add_year = len(df_add_year.index)
        df_add_year['PAYMENT YEAR'] = pd.DatetimeIndex(df_add_year['PAYMENT DATE']).year
        df_add_year_graph = df_add_year[pd.DatetimeIndex(df_add_year['PAYMENT DATE']).month == 12]
        df_add_year = df_add_year.drop(columns=['PMT NO', 'PAYMENT DATE'])
        df_add_year = df_add_year.groupby(['PAYMENT YEAR']).sum()

        df_year = pd.DataFrame.from_dict(amort_schd, orient='columns')
        row_year = len(df_year.index)
        df_year['PAYMENT YEAR'] = pd.DatetimeIndex(df_year['PAYMENT DATE']).year
        df_year_graph = df_year[pd.DatetimeIndex(df_year['PAYMENT DATE']).month == 12]
        df_year = df_year.drop(columns=['PMT NO', 'PAYMENT DATE'])
        df_year = df_year.groupby(['PAYMENT YEAR']).sum()

        row_difference = row_year - row_add_year

        fig = make_subplots()
        fig.add_trace(
            go.Scatter(x=df_year_graph["PAYMENT YEAR"], y=df_year_graph["ENDING BALANCE"], name="Default Loan"))
        if row_difference != 0:
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

    #return comparison box
    @app.callback(
        [Output(component_id='compare-top-1', component_property='children'),
         Output(component_id='compare-bottom-1', component_property='children'),
         Output(component_id='compare-top-2', component_property='children'),
         Output(component_id='compare-top-3', component_property='children'),
         Output(component_id='compare-bottom-3', component_property='children'),
         Output(component_id='compare-top-4', component_property='children'),
         Output(component_id='compare-top-5', component_property='children'),
         Output(component_id='compare-top-6', component_property='children'),
         Output(component_id='compare-chart', component_property='figure'),
         Output(component_id='compare-top-1', component_property='style'),
         Output(component_id='compare-bottom-1', component_property='style'),
         Output(component_id='compare-top-2', component_property='style'),
         Output(component_id='compare-bottom-2', component_property='style'),
         ],
        [Input('amort_schd', 'data'),
         Input('amort_schd_add', 'data'),
         ],
    )
    def compare_box(amort_schd, amort_schd_add):

        df_add = pd.DataFrame.from_dict(amort_schd_add, orient='columns')
        df = pd.DataFrame.from_dict(amort_schd, orient='columns')
        # getting values from dataframe
        value_pmi_cnt_add = len(df_add[df_add['PMI'] > 0])
        value_pmi_paid_add = round(df_add['PMI'].sum(), 2)
        value_loan_cnt_add = len(df_add.index)
        value_int_paid_add = round(df_add['INTEREST'].sum(), 2)
        value_tax_paid_add = round(df_add['TAX PAYMENT'].sum(), 2)
        value_ins_paid_add = round(df_add['MORTGAGE INSURANCE'].sum(), 2)

        value_pmi_cnt = len(df[df['PMI'] > 0])
        value_pmi_paid = round(df['PMI'].sum(), 2)
        value_loan_cnt = len(df.index)
        value_int_paid = round(df['INTEREST'].sum(), 2)
        value_tax_paid = round(df['TAX PAYMENT'].sum(), 2)
        value_ins_paid = round(df['MORTGAGE INSURANCE'].sum(), 2)
        value_tot_pay = round(df.at[0, 'TOTAL PAYMENT'], 2)

        #compare chart
        bar_chart = go.Figure(data=[
            go.Bar(name='Default Loan', x=['Interest Paid'], y=[value_int_paid]),
            go.Bar(name='With additional payment', x=['Interest Paid'], y=[value_int_paid_add])
        ])
        bar_chart.update_layout(barmode='group', bargap=0.15,  # gap between bars of adjacent location coordinates.
                                bargroupgap=0.1, title='Reduction to Interest Paid', title_y=.8,
                                xaxis_fixedrange=True,
                                yaxis_fixedrange=True)
        bar_chart.add_annotation(
            go.layout.Annotation(
                x=.1,
                y=(value_int_paid_add + value_int_paid) / 2,
                ax=40,
                ay=0,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                ),
                bgcolor="#F10000",
                showarrow=False,
                text=str(round((1 - (value_int_paid / value_int_paid_add)) * 100, 2)) + "%")
        )

        if value_pmi_cnt == 0:
            value_tot_cnt_save = value_loan_cnt - value_loan_cnt_add
            value_tot_time_save = str(math.trunc(value_tot_cnt_save / 12)) + ' Years and ' + str(
                value_tot_cnt_save % 12) + ' Months'
            value_int_save = value_int_paid - value_int_paid_add
            value_esc_save = (value_tax_paid - value_tax_paid_add) + (value_ins_paid - value_ins_paid_add)
            value_tot_paid_save = value_int_save + value_esc_save + value_tot_pay * value_tot_cnt_save

            # Convert to dollar values where required
            tot_save_dol = "${:,.2f}".format(value_tot_paid_save)
            int_save_dol = "${:,.2f}".format(value_int_save)
            esc_save_dol = "${:,.2f}".format(value_esc_save)

            tot_save_bottom = "Saved from " + str(round(value_tot_cnt_save, 0)) + " Payments"

            return 0, 0, 0, tot_save_dol, tot_save_bottom, value_tot_time_save, \
                   int_save_dol, esc_save_dol, bar_chart, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'none'}, {'display': 'none'}
        else:
            value_pmi_cnt_save = value_pmi_cnt - value_pmi_cnt_add
            value_pmi_time_save = str(math.trunc(value_pmi_cnt_save / 12)) + ' Years and ' + str(
                value_pmi_cnt_save % 12) + ' Months'
            value_pmi_paid_save = value_pmi_paid - value_pmi_paid_add
            value_tot_cnt_save = value_loan_cnt - value_loan_cnt_add
            value_tot_time_save = str(math.trunc(value_tot_cnt_save / 12)) + ' Years and ' + str(
                value_tot_cnt_save % 12) + ' Months'
            value_int_save = value_int_paid - value_int_paid_add
            value_esc_save = (value_tax_paid - value_tax_paid_add) + (value_ins_paid - value_ins_paid_add)
            value_tot_paid_save = value_int_save + value_esc_save + value_pmi_paid_save \
                                  + value_tot_pay * value_tot_cnt_save

            #Convert to dollar values where required
            paid_save_dol = "${:,.2f}".format(value_pmi_paid_save)
            tot_save_dol = "${:,.2f}".format(value_tot_paid_save)
            int_save_dol = "${:,.2f}".format(value_int_save)
            esc_save_dol = "${:,.2f}".format(value_esc_save)

            paid_save_bottom = "Saved from " + str(round(value_pmi_cnt_save, 0)) + " PMI Payments"
            tot_save_bottom = "Saved from " + str(round(value_tot_cnt_save, 0)) + " Payments"

            return paid_save_dol, paid_save_bottom, value_pmi_time_save, tot_save_dol, tot_save_bottom, value_tot_time_save, \
                   int_save_dol, esc_save_dol, bar_chart, {'display': 'flex'}, {'display': 'flex'}, \
                   {'display': 'flex'}, {'display': 'flex'}

    #return default loan box
    @app.callback(
        [Output(component_id='no-add-top-1', component_property='children'),
         Output(component_id='no-add-top-2', component_property='children'),
         Output(component_id='no-add-top-3', component_property='children'),
         Output(component_id='no-add-top-4', component_property='children'),
         Output(component_id='no-add-top-5', component_property='children'),
         Output(component_id='no-add-top-6', component_property='children'),
         Output(component_id='no-add-top-7', component_property='children'),
         Output(component_id='no-add-top-8', component_property='children'),
         Output(component_id='no-add-top-9', component_property='children'),
         Output(component_id='no-add-top-10', component_property='children'),
         Output(component_id='no-add-top-11', component_property='children'),
         Output(component_id='no-add-top-12', component_property='children'),
         Output(component_id='no-add-top-13', component_property='children'),
         Output(component_id='no-add-top-14', component_property='children'),
         Output(component_id='no-add-bottom-2', component_property='children'),
         Output(component_id='no-add-bottom-3', component_property='children'),
         Output(component_id='no-add-bottom-4', component_property='children'),
         Output(component_id='no-add-bottom-14', component_property='children'),

         Output(component_id='no-add-top-3', component_property='style'),
         Output(component_id='no-add-bottom-3', component_property='style'),
         Output(component_id='no-add-top-4', component_property='style'),
         Output(component_id='no-add-bottom-4', component_property='style'),
         Output(component_id='no-add-top-9', component_property='style'),
         Output(component_id='no-add-bottom-9', component_property='style'),
         Output(component_id='no-add-top-10', component_property='style'),
         Output(component_id='no-add-bottom-10', component_property='style'),
         ],
        [Input('amort_schd', 'data'),
         Input('amort_schd_add', 'data'),
         ],
        [State(component_id='row1', component_property='value'),
         State(component_id='loan_option', component_property='value')
         ]
    )
    def default_loan(amort_schd, amort_schd_add, home_price, loan_option):
        df = pd.DataFrame.from_dict(amort_schd, orient='columns')
        if home_price is None:
            home_price = home_price_default

        # getting values from dataframe
        value_tot_pay_esc_pmi = round(df.at[0, 'TOTAL PAYMENT W ESCROW'], 2)
        value_pmi_pay = round(df.at[0, 'PMI'], 2)
        value_tot_pay_esc = value_tot_pay_esc_pmi - value_pmi_pay
        value_tot_pay = round(df.at[0, 'TOTAL PAYMENT'], 2)
        value_ann_pay = value_tot_pay_esc_pmi * 12
        value_pmi_cnt = len(df[df['PMI'] > 0])
        value_pmi_paid = round(df['PMI'].sum(), 2)
        value_pmi_date = df.at[value_pmi_cnt, 'PAYMENT DATE']
        value_loan_date = df.at[len(df.index) - 1, 'PAYMENT DATE']
        value_loan_cnt = len(df.index)
        value_int_paid = round(df['INTEREST'].sum(), 2)
        value_tax_paid = round(df['TAX PAYMENT'].sum(), 2)
        value_ins_paid = round(df['MORTGAGE INSURANCE'].sum(), 2)
        value_tot_paid = value_int_paid + value_tax_paid + value_ins_paid + value_pmi_paid \
            + (value_tot_pay * value_loan_cnt)
        value_down_pay = home_price - round(df.at[0, 'BEGINNING BALANCE'], 2)
        value_percent_down = round(round(df.at[0, 'BEGINNING BALANCE'], 2) / home_price * 100, 2)

        #converting values to values to be seen on screen
        tot_pay_esc_pmi_dol = "${:,.2f}".format(value_tot_pay_esc_pmi) #total mth payment
        tot_pay_dol = "${:,.2f}".format(value_tot_pay)
        esc_pay_dol = "${:,.2f}".format(value_tot_pay_esc-value_tot_pay)
        ann_pay_dol = "${:,.2f}".format(value_ann_pay)
        loan_date_shown = datetime.strptime(value_loan_date, "%Y-%m-%d").strftime("%b %Y")
        int_paid_dol = "${:,.2f}".format(value_int_paid)
        tax_paid_dol = "${:,.2f}".format(value_tax_paid)
        ins_paid_dol = "${:,.2f}".format(value_ins_paid)
        tot_paid_dol = "${:,.2f}".format(value_tot_paid)
        bot_14 = "Total of " + str(value_loan_cnt) + " Payments"

        if value_pmi_cnt > 0 and loan_option == 'noloan':
            tot_pay_esc_dol = "${:,.2f}".format(value_tot_pay_esc)
            bot_2 = "After " + str(value_pmi_cnt) + " Months"
            pmi_pay_dol = "${:,.2f}".format(value_pmi_pay)
            bot_3 = str(value_pmi_cnt) + " PMI Payments"
            pmi_paid_dol = "${:,.2f}".format(value_pmi_paid)
            bot_4 = "Total PMI to " + datetime.strptime(value_pmi_date, "%Y-%m-%d").strftime("%b %Y")
            down_pay_dol = "${:,.2f}".format(value_down_pay)
            percent_down_per = "%{:,.0f}".format(value_percent_down)

            top_3_show = {'display': 'flex'}
            bot_3_show = {'display': 'flex'}
            top_4_show = {'display': 'flex'}
            bot_4_show = {'display': 'flex'}
            top_9_show = {'display': 'flex'}
            bot_9_show = {'display': 'flex'}
            top_10_show = {'display': 'flex'}
            bot_10_show = {'display': 'flex'}
        elif value_pmi_cnt > 0 and loan_option == 'loan':
            tot_pay_esc_dol = "${:,.2f}".format(value_tot_pay_esc)
            bot_2 = "After " + str(value_pmi_cnt) + " Months"
            pmi_pay_dol = "${:,.2f}".format(value_pmi_pay)
            bot_3 = str(value_pmi_cnt) + " PMI Payments"
            pmi_paid_dol = "${:,.2f}".format(value_pmi_paid)
            bot_4 = "Total PMI to " + datetime.strptime(value_pmi_date, "%Y-%m-%d").strftime("%b %Y")
            down_pay_dol = 0
            percent_down_per = 0

            top_3_show = {'display': 'flex'}
            bot_3_show = {'display': 'flex'}
            top_4_show = {'display': 'flex'}
            bot_4_show = {'display': 'flex'}
            top_9_show = {'display': 'none'}
            bot_9_show = {'display': 'none'}
            top_10_show = {'display': 'none'}
            bot_10_show = {'display': 'none'}
        elif value_pmi_cnt == 0 and loan_option == 'noloan':
            tot_pay_esc_dol = 0
            bot_2 = 0
            pmi_pay_dol = 0
            bot_3 = 0
            pmi_paid_dol = 0
            bot_4 = 0
            down_pay_dol = "${:,.2f}".format(value_down_pay)
            percent_down_per = "%{:,.0f}".format(value_percent_down)

            top_3_show = {'display': 'none'}
            bot_3_show = {'display': 'none'}
            top_4_show = {'display': 'none'}
            bot_4_show = {'display': 'none'}
            top_9_show = {'display': 'flex'}
            bot_9_show = {'display': 'flex'}
            top_10_show = {'display': 'flex'}
            bot_10_show = {'display': 'flex'}
        else:
            tot_pay_esc_dol = 0
            bot_2 = 0
            pmi_pay_dol = 0
            bot_3 = 0
            pmi_paid_dol = 0
            bot_4 = 0
            down_pay_dol = 0
            percent_down_per = 0

            top_3_show = {'display': 'none'}
            bot_3_show = {'display': 'none'}
            top_4_show = {'display': 'none'}
            bot_4_show = {'display': 'none'}
            top_9_show = {'display': 'none'}
            bot_9_show = {'display': 'none'}
            top_10_show = {'display': 'none'}
            bot_10_show = {'display': 'none'}

        return tot_pay_esc_pmi_dol, tot_pay_esc_dol, pmi_pay_dol, pmi_paid_dol, tot_pay_dol, \
               esc_pay_dol, ann_pay_dol, loan_date_shown, down_pay_dol, percent_down_per, \
               int_paid_dol, tax_paid_dol, ins_paid_dol, tot_paid_dol, bot_2, bot_3, bot_4, bot_14, \
               top_3_show, bot_3_show, top_4_show, bot_4_show, top_9_show, bot_9_show, top_10_show, \
               bot_10_show

    #return additional payment
    @app.callback(
        [Output(component_id='add-top-1', component_property='children'),
         Output(component_id='add-top-2', component_property='children'),
         Output(component_id='add-top-3', component_property='children'),
         Output(component_id='add-top-4', component_property='children'),
         Output(component_id='add-top-5', component_property='children'),
         Output(component_id='add-top-6', component_property='children'),
         Output(component_id='add-top-7', component_property='children'),
         Output(component_id='add-top-8', component_property='children'),
         Output(component_id='add-top-9', component_property='children'),
         Output(component_id='add-top-10', component_property='children'),
         Output(component_id='add-top-11', component_property='children'),
         Output(component_id='add-top-12', component_property='children'),
         Output(component_id='add-top-13', component_property='children'),
         Output(component_id='add-top-14', component_property='children'),
         Output(component_id='add-bottom-2', component_property='children'),
         Output(component_id='add-bottom-3', component_property='children'),
         Output(component_id='add-bottom-4', component_property='children'),
         Output(component_id='add-bottom-14', component_property='children'),

         Output(component_id='add-top-3', component_property='style'),
         Output(component_id='add-bottom-3', component_property='style'),
         Output(component_id='add-top-4', component_property='style'),
         Output(component_id='add-bottom-4', component_property='style'),
         Output(component_id='add-top-9', component_property='style'),
         Output(component_id='add-bottom-9', component_property='style'),
         Output(component_id='add-top-10', component_property='style'),
         Output(component_id='add-bottom-10', component_property='style'),
         ],
        [Input('amort_schd', 'data'),
         Input('amort_schd_add', 'data'),
         ],
        [State(component_id='row1', component_property='value'),
         State(component_id='loan_option', component_property='value'),
         State(component_id='row8', component_property='value'),
         ]
    )
    def default_loan_add(amort_schd, amort_schd_add, home_price, loan_option, additional_payment):
        df = pd.DataFrame.from_dict(amort_schd_add, orient='columns')
        df_no_add = pd.DataFrame.from_dict(amort_schd, orient='columns')
        compare_interest = round(df['INTEREST'].sum(), 2) - round(df_no_add['INTEREST'].sum(), 2)
        if compare_interest == 0:
            return 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

        if home_price is None:
            home_price = home_price_default
        if additional_payment is None:
            additional_payment = additional_payment_default

        # getting values from dataframe
        value_tot_pay_esc_pmi = round(df.at[0, 'TOTAL PAYMENT W ESCROW'], 2)
        value_pmi_pay = round(df.at[0, 'PMI'], 2)
        value_tot_pay_esc = value_tot_pay_esc_pmi - value_pmi_pay
        value_tot_pay = round(df.at[0, 'TOTAL PAYMENT'], 2)
        value_ann_pay = value_tot_pay_esc_pmi * 12
        value_pmi_cnt = len(df[df['PMI'] > 0])
        value_pmi_paid = round(df['PMI'].sum(), 2)
        value_pmi_date = df.at[value_pmi_cnt, 'PAYMENT DATE']
        value_loan_date = df.at[len(df.index) - 1, 'PAYMENT DATE']
        value_loan_cnt = len(df.index)
        value_int_paid = round(df['INTEREST'].sum(), 2)
        value_tax_paid = round(df['TAX PAYMENT'].sum(), 2)
        value_ins_paid = round(df['MORTGAGE INSURANCE'].sum(), 2)
        value_tot_paid = value_int_paid + value_tax_paid + value_ins_paid + value_pmi_paid \
            + ((value_tot_pay - additional_payment) * value_loan_cnt)
        value_down_pay = home_price - round(df.at[0, 'BEGINNING BALANCE'], 2)
        value_percent_down = round(round(df.at[0, 'BEGINNING BALANCE'], 2) / home_price * 100, 2)

        #converting values to values to be seen on screen
        tot_pay_esc_pmi_dol = "${:,.2f}".format(value_tot_pay_esc_pmi) #total mth payment
        tot_pay_dol = "${:,.2f}".format(value_tot_pay)
        esc_pay_dol = "${:,.2f}".format(value_tot_pay_esc-value_tot_pay)
        ann_pay_dol = "${:,.2f}".format(value_ann_pay)
        loan_date_shown = datetime.strptime(value_loan_date, "%Y-%m-%d").strftime("%b %Y")
        int_paid_dol = "${:,.2f}".format(value_int_paid)
        tax_paid_dol = "${:,.2f}".format(value_tax_paid)
        ins_paid_dol = "${:,.2f}".format(value_ins_paid)
        tot_paid_dol = "${:,.2f}".format(value_tot_paid)
        bot_14 = "Total of " + str(value_loan_cnt) + " Payments"

        if value_pmi_cnt > 0 and loan_option == 'noloan':
            tot_pay_esc_dol = "${:,.2f}".format(value_tot_pay_esc)
            bot_2 = "After " + str(value_pmi_cnt) + " Months"
            pmi_pay_dol = "${:,.2f}".format(value_pmi_pay)
            bot_3 = str(value_pmi_cnt) + " PMI Payments"
            pmi_paid_dol = "${:,.2f}".format(value_pmi_paid)
            bot_4 = "Total PMI to " + datetime.strptime(value_pmi_date, "%Y-%m-%d").strftime("%b %Y")
            down_pay_dol = "${:,.2f}".format(value_down_pay)
            percent_down_per = "%{:,.0f}".format(value_percent_down)

            top_3_show = {'display': 'flex'}
            bot_3_show = {'display': 'flex'}
            top_4_show = {'display': 'flex'}
            bot_4_show = {'display': 'flex'}
            top_9_show = {'display': 'flex'}
            bot_9_show = {'display': 'flex'}
            top_10_show = {'display': 'flex'}
            bot_10_show = {'display': 'flex'}
        elif value_pmi_cnt > 0 and loan_option == 'loan':
            tot_pay_esc_dol = "${:,.2f}".format(value_tot_pay_esc)
            bot_2 = "After " + str(value_pmi_cnt) + " Months"
            pmi_pay_dol = "${:,.2f}".format(value_pmi_pay)
            bot_3 = str(value_pmi_cnt) + " PMI Payments"
            pmi_paid_dol = "${:,.2f}".format(value_pmi_paid)
            bot_4 = "Total PMI to " + datetime.strptime(value_pmi_date, "%Y-%m-%d").strftime("%b %Y")
            down_pay_dol = 0
            percent_down_per = 0

            top_3_show = {'display': 'flex'}
            bot_3_show = {'display': 'flex'}
            top_4_show = {'display': 'flex'}
            bot_4_show = {'display': 'flex'}
            top_9_show = {'display': 'none'}
            bot_9_show = {'display': 'none'}
            top_10_show = {'display': 'none'}
            bot_10_show = {'display': 'none'}
        elif value_pmi_cnt == 0 and loan_option == 'noloan':
            tot_pay_esc_dol = 0
            bot_2 = 0
            pmi_pay_dol = 0
            bot_3 = 0
            pmi_paid_dol = 0
            bot_4 = 0
            down_pay_dol = "${:,.2f}".format(value_down_pay)
            percent_down_per = "%{:,.0f}".format(value_percent_down)

            top_3_show = {'display': 'none'}
            bot_3_show = {'display': 'none'}
            top_4_show = {'display': 'none'}
            bot_4_show = {'display': 'none'}
            top_9_show = {'display': 'flex'}
            bot_9_show = {'display': 'flex'}
            top_10_show = {'display': 'flex'}
            bot_10_show = {'display': 'flex'}
        else:
            tot_pay_esc_dol = 0
            bot_2 = 0
            pmi_pay_dol = 0
            bot_3 = 0
            pmi_paid_dol = 0
            bot_4 = 0
            down_pay_dol = 0
            percent_down_per = 0

            top_3_show = {'display': 'none'}
            bot_3_show = {'display': 'none'}
            top_4_show = {'display': 'none'}
            bot_4_show = {'display': 'none'}
            top_9_show = {'display': 'none'}
            bot_9_show = {'display': 'none'}
            top_10_show = {'display': 'none'}
            bot_10_show = {'display': 'none'}

        return tot_pay_esc_pmi_dol, tot_pay_esc_dol, pmi_pay_dol, pmi_paid_dol, tot_pay_dol, \
               esc_pay_dol, ann_pay_dol, loan_date_shown, down_pay_dol, percent_down_per, \
               int_paid_dol, tax_paid_dol, ins_paid_dol, tot_paid_dol, bot_2, bot_3, bot_4, bot_14, \
               top_3_show, bot_3_show, top_4_show, bot_4_show, top_9_show, bot_9_show, top_10_show, \
               bot_10_show

    #create pie charts and store them
    @app.callback(
        [Output('pie_one', 'data'),
         Output('pie_one_add', 'data'),
         Output('pie_two', 'data'),
         Output('pie_two_add', 'data'),
         ],
        [Input('amort_schd', 'data'),
         Input('amort_schd_add', 'data')
         ],
        [State(component_id='row8', component_property='value'),
         ]
    )
    def pie_charts(amort_schd, amort_schd_add, add_pay):
        df_add = pd.DataFrame.from_dict(amort_schd_add, orient='columns')
        df = pd.DataFrame.from_dict(amort_schd, orient='columns')
        # Create pie/bar charts to show to user
        # create labels for different scenarios for the pie charts
        chart_one_labels_add = ['Principal & Interest', 'Tax', 'Home Insurance', 'Additional Payment']
        chart_one_labels_pmi_add = ['Principal & Interest', 'Tax', 'Home Insurance', 'PMI', 'Additional Payment']
        chart_one_labels = ['Principal & Interest', 'Tax', 'Home Insurance']
        chart_one_labels_pmi = ['Principal & Interest', 'Tax', 'Home Insurance', 'PMI']
        chart_two_labels = ['Principal', 'Interest', 'Tax', 'Home Insurance']
        chart_two_labels_pmi = ['Principal', 'Interest', 'Tax', 'Home Insurance', 'PMI']

        value_pmi_cnt = len(df[df['PMI'] > 0])
        scheduled_pay = round(df.at[0, 'TOTAL PAYMENT'], 2)
        value_int_paid_add = round(df_add['INTEREST'].sum(), 2)
        value_tax_paid_add = round(df_add['TAX PAYMENT'].sum(), 2)
        value_ins_paid_add = round(df_add['MORTGAGE INSURANCE'].sum(), 2)
        value_pmi_paid_add = round(df_add['PMI'].sum(), 2)
        value_int_paid = round(df['INTEREST'].sum(), 2)
        value_tax_paid = round(df['TAX PAYMENT'].sum(), 2)
        value_ins_paid = round(df['MORTGAGE INSURANCE'].sum(), 2)
        value_pmi_paid = round(df['PMI'].sum(), 2)

        # differences in layout depending whether or not user has PMI for pie charts
        if value_pmi_cnt == 0:
            pie_one_labels_add = chart_one_labels_add
            pie_one_values_add = [round(scheduled_pay, 2), round(df_add.at[0, 'TAX PAYMENT'], 2),
                                  round(df_add.at[0, 'MORTGAGE INSURANCE'], 2), add_pay]
            pie_one_labels = chart_one_labels
            pie_one_values = [round(scheduled_pay, 2), round(df.at[0, 'TAX PAYMENT'], 2),
                              round(df.at[0, 'MORTGAGE INSURANCE'], 2)]
            pie_two_labels_add = chart_two_labels
            pie_two_values_add = [round(df_add.at[0, 'BEGINNING BALANCE'], 2), value_int_paid_add, value_tax_paid_add,
                                  value_ins_paid_add]
            pie_two_labels = chart_two_labels
            pie_two_values = [round(df.at[0, 'BEGINNING BALANCE'], 2), value_int_paid, value_tax_paid, value_ins_paid]
        else:
            pie_one_labels_add = chart_one_labels_pmi_add
            pie_one_values_add = [round(scheduled_pay, 2), round(df_add.at[0, 'TAX PAYMENT'], 2),
                                  round(df_add.at[0, 'MORTGAGE INSURANCE'], 2), round(df_add.at[0, 'PMI'], 2), add_pay]
            pie_one_labels = chart_one_labels_pmi
            pie_one_values = [round(scheduled_pay, 2), round(df.at[0, 'TAX PAYMENT'], 2),
                              round(df.at[0, 'MORTGAGE INSURANCE'], 2), round(df_add.at[0, 'PMI'], 2)]
            pie_two_labels_add = chart_two_labels_pmi
            pie_two_values_add = [round(df_add.at[0, 'BEGINNING BALANCE'], 2), value_int_paid_add, value_tax_paid_add,
                                  value_ins_paid_add, value_pmi_paid_add]
            pie_two_labels = chart_two_labels_pmi
            pie_two_values = [round(df.at[0, 'BEGINNING BALANCE'], 2), value_int_paid, value_tax_paid, value_ins_paid,
                              value_pmi_paid]

        # create pie charts with values and labels
        pie_one_add = go.Figure(data=[go.Pie(labels=pie_one_labels_add, values=pie_one_values_add, sort=False)])
        pie_one = go.Figure(data=[go.Pie(labels=pie_one_labels, values=pie_one_values, sort=False)])
        pie_two_add = go.Figure(data=[go.Pie(labels=pie_two_labels_add, values=pie_two_values_add, sort=False)])
        pie_two = go.Figure(data=[go.Pie(labels=pie_two_labels, values=pie_two_values, sort=False)])
        return pie_one, pie_one_add, pie_two, pie_two_add

    #Select between pie charts
    @app.callback(
        [Output('pie', 'figure'),
         Output('pie-add', 'figure'),
         ],
        [Input('add-pie-graph', 'value'),
         Input('no-add-pie-graph', 'value'),
         Input('pie_one', 'data'),
         Input('pie_one_add', 'data'),
         Input('pie_two', 'data'),
         Input('pie_two_add', 'data'),
         ],
    )
    def pie_charts_sel(option_add, option_no_add, pie_one, pie_one_add, pie_two, pie_two_add):
        if option_no_add == 'month':
            return_one = pie_one
        else:
            return_one = pie_two
        if option_add == 'month':
            return_two = pie_one_add
        else:
            return_two = pie_two_add

        return return_one, return_two