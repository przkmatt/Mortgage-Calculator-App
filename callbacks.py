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
        [Input(component_id='loan_option', component_property='value')]
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