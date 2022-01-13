from datetime import datetime
from datetime import date
from datetime import timedelta
import math
import numpy as np
import pandas as pd

current_day = datetime.now().day
current_month = datetime.now().month
current_year = datetime.now().year
current_date = date(current_year, current_month, 15)

#creating variables for defaults in my app
home_price_default = 200000
down_payment_default = 20000
loan_time_default = 30
interest_rate_default = 3.5
pmi_rate_default = .5
additional_payment_default = 0
loan_rem_default = 180000
loan_pay_default = 850
pmi_amt_default = 75
mort_amt_default = 100
tax_amt_default = 100
loan_start_default = current_date

loan_unknown = True

if loan_unknown:
    home_price = float(200000)
    down_pay = float(10000)
    loan_time = float(30)
    interest = float(3.5)
    pmi_rate = float(.5)
    mtg_ins_yr = float(0)
    tax_amt_yr = float(0)
    add_pay = float(100)
    loan_start = loan_start_default
else:
    home_price = float(200000)
    loan_rem = float(180000)
    loan_pay = float(832)
    interest = float(3.5)
    pmi_amt = float(75)
    mtg_ins_yr = float(0)
    tax_amt_yr = float(0)
    add_pay = float(0)

if loan_unknown:
    df_add = pd.read_csv('Mortgage.csv')
    df = pd.read_csv('Mortgage.csv')
    pmt_no = 1
    interest_mth = interest / 100 / 12
    discount = interest_mth / (1 + interest_mth)
    payment_date = current_date
    beginning_bal = home_price - down_pay
    scheduled_pay = beginning_bal * (interest_mth * math.pow((1 + interest_mth), loan_time*12)) / (math.pow((1 + interest_mth), loan_time*12)-1)
    extra_pay = add_pay
    total_pay = scheduled_pay + add_pay
    mort_ins = mtg_ins_yr/12
    tax_pay = tax_amt_yr/12
    lvt = (home_price - down_pay) / home_price
    months_left = round(math.log(-total_pay/((beginning_bal*interest_mth)-total_pay))/math.log(1+interest_mth), 0)
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
        df_add.loc[len(df_add.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2), round(extra_pay, 2), round(total_pay, 2),
                                 round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2), round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2), round(total_pay_w_esc, 2)]
        beginning_bal = ending_bal
        pmt_no = pmt_no + 1

#reframing for no additional payment dataframe
    pmt_no = 1
    beginning_bal = home_price - down_pay
    extra_pay = 0
    total_pay = scheduled_pay
    lvt = (home_price - down_pay) / home_price
    months_left = round(math.log(-total_pay/((beginning_bal*interest_mth)-total_pay))/math.log(1+interest_mth), 0)
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
        df.loc[len(df.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2), round(extra_pay, 2), round(total_pay, 2),
                                 round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2), round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2), round(total_pay_w_esc, 2)]
        beginning_bal = ending_bal
        pmt_no = pmt_no + 1
else:
    #inserting into dataframe with given information
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
    mort_ins = mtg_ins_yr/12
    tax_pay = tax_amt_yr / 12
    lvt = loan_rem / home_price
    months_left = round(math.log(-total_pay/((beginning_bal*interest_mth)-total_pay))/math.log(1+interest_mth), 0)
    while pmt_no <= months_left:
        ending_bal = beginning_bal - ((scheduled_pay + extra_pay) - beginning_bal * interest_mth)
        interest_pay = beginning_bal * interest_mth
        principal_pay = total_pay - interest_pay
        lvt = ending_bal/home_price
        if lvt > .8:
            pmi_pay = pmi_amt
        else:
            pmi_pay = 0
        total_pay_w_esc = scheduled_pay + extra_pay + mort_ins + pmi_pay + tax_pay
        payment_date_shown = current_date + timedelta(days=pmt_no/12*365.25)
        payment_date_shown = payment_date_shown.replace(day=1)
        df_add.loc[len(df_add.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2), round(extra_pay, 2), round(total_pay, 2),
                                 round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2), round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2), round(total_pay_w_esc, 2)]
        beginning_bal = ending_bal
        pmt_no = pmt_no + 1

    #reframing for no additional payment dataframe
    pmt_no = 1
    beginning_bal = loan_rem
    extra_pay = 0
    total_pay = scheduled_pay
    lvt = loan_rem / home_price
    months_left = round(math.log(-total_pay/((beginning_bal*interest_mth)-total_pay))/math.log(1+interest_mth), 0)
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
        df.loc[len(df.index)] = [pmt_no, payment_date_shown, round(beginning_bal, 2), round(scheduled_pay, 2), round(extra_pay, 2), round(total_pay, 2),
                                 round(principal_pay, 2), round(interest_pay, 2), round(ending_bal, 2), round(mort_ins, 2), round(pmi_pay, 2), round(tax_pay, 2), round(total_pay_w_esc, 2)]
        beginning_bal = ending_bal
        pmt_no = pmt_no + 1

#getting values from dataframe

value_tot_pay_esc_pmi_add = round(df_add.at[0, 'TOTAL PAYMENT W ESCROW'], 2)
value_pmi_pay_add = round(df_add.at[0, 'PMI'], 2)
value_tot_pay_esc_add = value_tot_pay_esc_pmi_add - value_pmi_pay_add
value_tot_pay_add = round(df_add.at[0, 'TOTAL PAYMENT'], 2)
value_ann_pay_add = value_tot_pay_esc_pmi_add * 12
value_pmi_cnt_add = len(df_add[df_add['PMI']>0])
value_pmi_paid_add = round(df_add['PMI'].sum(), 2)
value_pmi_date_add = df_add.at[value_pmi_cnt_add, 'PAYMENT DATE']
value_loan_date_add = df_add.at[len(df_add.index)-1, 'PAYMENT DATE']
value_loan_cnt_add = len(df_add.index)
value_int_paid_add = round(df_add['INTEREST'].sum(), 2)
value_tax_paid_add = round(df_add['TAX PAYMENT'].sum(), 2)
value_ins_paid_add = round(df_add['MORTGAGE INSURANCE'].sum(), 2)
value_tot_paid_add = round(df_add['TOTAL PAYMENT W ESCROW'].sum(), 2)

value_tot_pay_esc_pmi = round(df.at[0, 'TOTAL PAYMENT W ESCROW'], 2)
value_pmi_pay = round(df.at[0, 'PMI'], 2)
value_tot_pay_esc = value_tot_pay_esc_pmi - value_pmi_pay
value_tot_pay = round(df.at[0, 'TOTAL PAYMENT'], 2)
value_ann_pay = value_tot_pay_esc_pmi * 12
value_pmi_cnt = len(df[df['PMI']>0])
value_pmi_paid = round(df['PMI'].sum(), 2)
value_pmi_date = df.at[value_pmi_cnt, 'PAYMENT DATE']
value_loan_date = df.at[len(df.index)-1, 'PAYMENT DATE']
value_loan_cnt = len(df.index)
value_int_paid = round(df['INTEREST'].sum(), 2)
value_tax_paid = round(df['TAX PAYMENT'].sum(), 2)
value_ins_paid = round(df['MORTGAGE INSURANCE'].sum(), 2)
value_tot_paid = round(df['TOTAL PAYMENT W ESCROW'].sum(), 2)

value_down_pay = home_price - round(df.at[0, 'BEGINNING BALANCE'], 2)
value_percent_down = round(round(df.at[0, 'BEGINNING BALANCE'], 2) / home_price * 100, 2)
value_first_pay = df.at[0, 'PAYMENT DATE']

value_pmi_cnt_save = value_pmi_cnt - value_pmi_cnt_add
value_pmi_time_save = str(math.trunc(value_pmi_cnt_save/12)) + 'Years and ' + str(value_pmi_cnt_save % 12) + 'Months'
value_pmi_paid_save = value_pmi_paid - value_pmi_paid_add
value_tot_cnt_save = value_loan_cnt - value_loan_cnt_add
value_tot_time_save = str(math.trunc(value_tot_cnt_save/12)) + 'Years and ' + str(value_tot_cnt_save % 12) + 'Months'
value_tot_paid_save = value_tot_paid - value_tot_paid_add
value_int_save = value_int_paid - value_int_paid_add
value_esc_save = (value_tax_paid - value_tax_paid_add) + (value_ins_paid - value_ins_paid_add)

#convert to yearly dataframes
df_add_year = df_add
df_add_year['PAYMENT YEAR'] = pd.DatetimeIndex(df_add_year['PAYMENT DATE']).year
df_add_year_graph = df_add_year[pd.DatetimeIndex(df_add_year['PAYMENT DATE']).month == 12]
df_add_year = df_add_year.drop(columns=['PMT NO', 'PAYMENT DATE'])
df_add_year = df_add_year.groupby(['PAYMENT YEAR']).sum()

df_year = df
df_year['PAYMENT YEAR'] = pd.DatetimeIndex(df_year['PAYMENT DATE']).year
df_year_graph = df_year[pd.DatetimeIndex(df_year['PAYMENT DATE']).month == 12]
df_year = df_year.drop(columns=['PMT NO', 'PAYMENT DATE'])
df_year = df_year.groupby(['PAYMENT YEAR']).sum()
# df_year_graph.to_csv(path_or_buf='df_year.csv')
# df_add_year_graph.to_csv(path_or_buf='df_add_year.csv')

#Create pie/bar charts to show to user
#create labels for different scenarios for the pie charts
chart_one_labels_add = ['Principal & Interest', 'Tax', 'Home Insurance', 'Additional Payment']
chart_one_labels_pmi_add = ['Principal & Interest', 'Tax', 'Home Insurance', 'PMI', 'Additional Payment']
chart_one_labels = ['Principal & Interest', 'Tax', 'Home Insurance']
chart_one_labels_pmi = ['Principal & Interest', 'Tax', 'Home Insurance', 'PMI']
chart_two_labels = ['Principal', 'Interest', 'Tax', 'Home Insurance']
chart_two_labels_pmi = ['Principal', 'Interest', 'Tax', 'Home Insurance', 'PMI']

#differences in layout depending whether or not user has PMI for pie charts
if value_pmi_cnt == 0:
    pie_one_labels_add = chart_one_labels_add
    pie_one_values_add = [round(scheduled_pay, 2), round(df_add.at[0, 'TAX PAYMENT'], 2), round(df_add.at[0, 'MORTGAGE INSURANCE'], 2), add_pay]
    pie_one_labels = chart_one_labels
    pie_one_values = [round(scheduled_pay, 2), round(df.at[0, 'TAX PAYMENT'], 2), round(df.at[0, 'MORTGAGE INSURANCE'], 2)]
    pie_two_labels_add = chart_two_labels
    pie_two_values_add = [round(df_add.at[0, 'BEGINNING BALANCE'], 2), value_int_paid_add, value_tax_paid_add, value_ins_paid_add]
    pie_two_labels = chart_two_labels
    pie_two_values = [round(df.at[0, 'BEGINNING BALANCE'], 2), value_int_paid, value_tax_paid, value_ins_paid]
else:
    pie_one_labels_add = chart_one_labels_pmi_add
    pie_one_values_add = [round(scheduled_pay, 2), round(df_add.at[0, 'TAX PAYMENT'], 2),
                          round(df_add.at[0, 'MORTGAGE INSURANCE'], 2), round(df_add.at[0, 'PMI'], 2), add_pay]
    pie_one_labels = chart_one_labels_pmi
    pie_one_values = [round(scheduled_pay, 2), round(df.at[0, 'TAX PAYMENT'], 2), round(df.at[0, 'MORTGAGE INSURANCE'], 2), round(df_add.at[0, 'PMI'], 2)]
    pie_two_labels_add = chart_two_labels_pmi
    pie_two_values_add = [round(df_add.at[0, 'BEGINNING BALANCE'], 2), value_int_paid_add, value_tax_paid_add,
                          value_ins_paid_add, value_pmi_paid_add]
    pie_two_labels = chart_two_labels_pmi
    pie_two_values = [round(df.at[0, 'BEGINNING BALANCE'], 2), value_int_paid, value_tax_paid, value_ins_paid, value_pmi_paid]
