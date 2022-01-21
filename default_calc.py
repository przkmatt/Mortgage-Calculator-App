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
additional_payment_default = 100
loan_rem_default = 180000
loan_pay_default = 850
pmi_amt_default = 75
mort_amt_default = 100
tax_amt_default = 100
loan_start_default = current_date

loan_unknown = False

if loan_unknown:
    home_price = float(home_price_default)
    down_pay = float(down_payment_default)
    loan_time = float(loan_time_default)
    interest = float(interest_rate_default)
    pmi_rate = float(pmi_rate_default)
    mtg_ins_yr = float(mort_amt_default)
    tax_amt_yr = float(tax_amt_default)
    add_pay = float(additional_payment_default)
    loan_start = loan_start_default
else:
    home_price = float(home_price_default)
    loan_rem = float(loan_rem_default)
    loan_pay = float(loan_pay_default)
    interest = float(interest_rate_default)
    pmi_amt = float(pmi_amt_default)
    mtg_ins_yr = float(mort_amt_default)
    tax_amt_yr = float(tax_amt_default)
    add_pay = float(additional_payment_default)

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
value_pmi_cnt_add = len(df_add[df_add['PMI'] > 0])
value_pmi_paid_add = round(df_add['PMI'].sum(), 2)
value_pmi_date_add = df_add.at[value_pmi_cnt_add, 'PAYMENT DATE']
value_loan_date_add = df_add.at[len(df_add.index) - 1, 'PAYMENT DATE']
value_loan_cnt_add = len(df_add.index)
value_int_paid_add = round(df_add['INTEREST'].sum(), 2)
value_tax_paid_add = round(df_add['TAX PAYMENT'].sum(), 2)
value_ins_paid_add = round(df_add['MORTGAGE INSURANCE'].sum(), 2)
value_tot_paid_add = value_int_paid_add + value_tax_paid_add + value_ins_paid_add + value_pmi_paid_add \
    + (value_tot_pay_add * value_loan_cnt_add)

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

#output values that go into webpage NO ADD
tot_pay_esc_pmi_dol = "${:,.2f}".format(value_tot_pay_esc_pmi)  # total mth payment
tot_pay_dol = "${:,.2f}".format(value_tot_pay)
esc_pay_dol = "${:,.2f}".format(value_tot_pay_esc - value_tot_pay)
ann_pay_dol = "${:,.2f}".format(value_ann_pay)
loan_date_shown = value_loan_date.strftime("%b %Y")
int_paid_dol = "${:,.2f}".format(value_int_paid)
tax_paid_dol = "${:,.2f}".format(value_tax_paid)
ins_paid_dol = "${:,.2f}".format(value_ins_paid)
tot_paid_dol = "${:,.2f}".format(value_tot_paid)
bot_14 = "Total of " + str(value_loan_cnt) + " Payments"

if value_pmi_cnt > 0 and loan_unknown is True:
    tot_pay_esc_dol = "${:,.2f}".format(value_tot_pay_esc)
    bot_2 = "After " + str(value_pmi_cnt) + " Months"
    pmi_pay_dol = "${:,.2f}".format(value_pmi_pay)
    bot_3 = str(value_pmi_cnt) + " PMI Payments"
    pmi_paid_dol = "${:,.2f}".format(value_pmi_paid)
    bot_4 = "Total PMI to " + value_pmi_date.strftime("%b %Y")
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
elif value_pmi_cnt > 0 and loan_unknown is False:
    tot_pay_esc_dol = "${:,.2f}".format(value_tot_pay_esc)
    bot_2 = "After " + str(value_pmi_cnt) + " Months"
    pmi_pay_dol = "${:,.2f}".format(value_pmi_pay)
    bot_3 = str(value_pmi_cnt) + " PMI Payments"
    pmi_paid_dol = "${:,.2f}".format(value_pmi_paid)
    bot_4 = "Total PMI to " + value_pmi_date.strftime("%b %Y")
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
elif value_pmi_cnt == 0 and loan_unknown is True:
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

#output values that go into webpage ADDITIONAL PAYMENT
tot_pay_esc_pmi_dol_add = "${:,.2f}".format(value_tot_pay_esc_pmi_add)  # total mth payment
tot_pay_dol_add = "${:,.2f}".format(value_tot_pay_add)
esc_pay_dol_add = "${:,.2f}".format(value_tot_pay_esc_add - value_tot_pay_add)
ann_pay_dol_add = "${:,.2f}".format(value_ann_pay_add)
loan_date_shown_add = value_loan_date_add.strftime("%b %Y")
int_paid_dol_add = "${:,.2f}".format(value_int_paid_add)
tax_paid_dol_add = "${:,.2f}".format(value_tax_paid_add)
ins_paid_dol_add = "${:,.2f}".format(value_ins_paid_add)
tot_paid_dol_add = "${:,.2f}".format(value_tot_paid_add)
bot_14_add = "Total of " + str(value_loan_cnt_add) + " Payments"

if value_pmi_cnt > 0 and loan_unknown is True:
    tot_pay_esc_dol_add = "${:,.2f}".format(value_tot_pay_esc_add)
    bot_2_add = "After " + str(value_pmi_cnt_add) + " Months"
    pmi_pay_dol_add = "${:,.2f}".format(value_pmi_pay_add)
    bot_3_add = str(value_pmi_cnt_add) + " PMI Payments"
    pmi_paid_dol_add = "${:,.2f}".format(value_pmi_paid_add)
    bot_4_add = "Total PMI to " + value_pmi_date_add.strftime("%b %Y")
    down_pay_dol_add = "${:,.2f}".format(value_down_pay)
    percent_down_per_add = "%{:,.0f}".format(value_percent_down)

    top_3_show_add = {'display': 'flex'}
    bot_3_show_add = {'display': 'flex'}
    top_4_show_add = {'display': 'flex'}
    bot_4_show_add = {'display': 'flex'}
    top_9_show_add = {'display': 'flex'}
    bot_9_show_add = {'display': 'flex'}
    top_10_show_add = {'display': 'flex'}
    bot_10_show_add = {'display': 'flex'}
elif value_pmi_cnt > 0 and loan_unknown is False:
    tot_pay_esc_dol_add = "${:,.2f}".format(value_tot_pay_esc_add)
    bot_2_add = "After " + str(value_pmi_cnt_add) + " Months"
    pmi_pay_dol_add = "${:,.2f}".format(value_pmi_pay_add)
    bot_3_add = str(value_pmi_cnt_add) + " PMI Payments"
    pmi_paid_dol_add = "${:,.2f}".format(value_pmi_paid_add)
    bot_4_add = "Total PMI to " + value_pmi_date_add.strftime("%b %Y")
    down_pay_dol_add = 0
    percent_down_per_add = 0

    top_3_show_add = {'display': 'flex'}
    bot_3_show_add = {'display': 'flex'}
    top_4_show_add = {'display': 'flex'}
    bot_4_show_add = {'display': 'flex'}
    top_9_show_add = {'display': 'none'}
    bot_9_show_add = {'display': 'none'}
    top_10_show_add = {'display': 'none'}
    bot_10_show_add = {'display': 'none'}
elif value_pmi_cnt == 0 and loan_unknown is True:
    tot_pay_esc_dol_add = 0
    bot_2_add = 0
    pmi_pay_dol_add = 0
    bot_3_add = 0
    pmi_paid_dol_add = 0
    bot_4_add = 0
    down_pay_dol_add = "${:,.2f}".format(value_down_pay)
    percent_down_per_add = "%{:,.0f}".format(value_percent_down)

    top_3_show_add = {'display': 'none'}
    bot_3_show_add = {'display': 'none'}
    top_4_show_add = {'display': 'none'}
    bot_4_show_add = {'display': 'none'}
    top_9_show_add = {'display': 'flex'}
    bot_9_show_add = {'display': 'flex'}
    top_10_show_add = {'display': 'flex'}
    bot_10_show_add = {'display': 'flex'}
else:
    tot_pay_esc_dol_add = 0
    bot_2_add = 0
    pmi_pay_dol_add = 0
    bot_3_add = 0
    pmi_paid_dol_add = 0
    bot_4_add = 0
    down_pay_dol_add = 0
    percent_down_per_add = 0

    top_3_show_add = {'display': 'none'}
    bot_3_show_add = {'display': 'none'}
    top_4_show_add = {'display': 'none'}
    bot_4_show_add = {'display': 'none'}
    top_9_show_add = {'display': 'none'}
    bot_9_show_add = {'display': 'none'}
    top_10_show_add = {'display': 'none'}
    bot_10_show_add = {'display': 'none'}
