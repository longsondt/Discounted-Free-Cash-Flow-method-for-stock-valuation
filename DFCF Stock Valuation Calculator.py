import yfinance as yf
while True:
    while True:
        # Asking for user's input until a correct ticker is inputted
        try:
            ticker = input("Type in the ticker symbol: ")
            ticker_object = yf.Ticker(ticker)
            print(ticker_object.info['longBusinessSummary'])
            break
        except KeyError:
            print("Please enter a valid ticker symbol")

    # The set of codes below is to check whether the ticker has the required line items generated using yfinance
    # Generate a set of row names for the line items we must have:
    must_have_items = {'Total Cash From Operating Activities', 'Capital Expenditures',
                       'Total Revenue', 'Net Income'}

    # Generate a set of row names available of the current ticker's financial statements:
    cashflow_items = set(ticker_object.cashflow.index)
    incomestatement_items = set(ticker_object.financials.index)
    available_items = cashflow_items | incomestatement_items

    # If an item in the set of items we need is not present, we should re run the calculator with a different ticker
    if len(must_have_items.intersection(available_items)) < len(must_have_items):
        print(
            'The ticker does not meet the requirement for this calculator. '
            'Please re run the calculator with a new ticker')
    else:
        break

# ### Generate a list of number of years
NUM_OF_YEARS = len(list(ticker_object.financials.columns.values))


# # Step 1. Getting historical FCF
def get_historical_FCF():
    # ### i. Accessing the cash flow statement
    cashflow_df = ticker_object.cashflow

    # ### ii. Getting net operating cash flow
    net_OP_CF = list(cashflow_df.loc['Total Cash From Operating Activities'])

    # ### iii. Getting capital expenditures
    cap_ex = list(cashflow_df.loc['Capital Expenditures'])

    # ### iv. Calculate historical FCF
    hist_FCF = []
    len(list(cashflow_df.columns.values))
    for i in range(NUM_OF_YEARS):
        hist_FCF.append(net_OP_CF[i] + cap_ex[i])

    # Rearrange from oldest to latest year because Yahoo! Finance year column is newest to oldest
    hist_FCF = hist_FCF[::-1]

    return hist_FCF


hist_FCF = get_historical_FCF()

# # Step 2. Getting forecasted FCF
# ## 2.1 Find average revenue growth rate
# ### i. Accessing the financial statement
financials_df = ticker_object.financials

# ### ii. Accessing the Total Revenue
hist_total_revenue = list(financials_df.loc['Total Revenue'])

# Again, rearranging the order so it's easier to calculate the historical revenue growth
hist_total_revenue = hist_total_revenue[::-1]


# ### iii. Find average historical revenue growth rate
def avg_rev_growth(hist_total_revenue):
    past_rev_growth = []
    for i in range(1, NUM_OF_YEARS):
        growth = (hist_total_revenue[i] - hist_total_revenue[i - 1]) / hist_total_revenue[i - 1]
        past_rev_growth.append(growth)

    return sum(past_rev_growth) / len(past_rev_growth)


avg_rev_growth = avg_rev_growth(hist_total_revenue)

# ## 2.2 Find average net income/total revenue margin
# ### i. Accessing historical net income
hist_net_income = list(financials_df.loc['Net Income'])
# Again, rearranging the order so it's easier to calculate the net income margin per past year
hist_net_income = hist_net_income[::-1]


# ### ii. Find average historical net income margin per year
def avg_netincome_margin(hist_net_income, hist_total_revenue):
    past_netincome_margin = []
    for i in range(NUM_OF_YEARS):
        netincome_margin = hist_net_income[i] / hist_total_revenue[i]
        past_netincome_margin.append(netincome_margin)

    return sum(past_netincome_margin) / len(past_netincome_margin)


avg_netincome_margin = avg_netincome_margin(hist_net_income, hist_total_revenue)


# ## 2.3 Find average FCF/net income margin
def avg_FCF_margin(hist_FCF, hist_net_income):
    FCF_margin = []
    for i in range(NUM_OF_YEARS):
        margin = hist_FCF[i] / hist_net_income[i]
        FCF_margin.append(margin)

    return sum(FCF_margin) / len(FCF_margin)


avg_FCF_margin = avg_FCF_margin(hist_FCF, hist_net_income)


# ## 2.4 Find forecasted FCF
# ### i. Find forecasted Total Revenue
def future_revenues(hist_total_revenue, avg_rev_growth):
    future_revenues = []

    for i in range(NUM_OF_YEARS):
        future_rev = hist_total_revenue[-1] * (1 + avg_rev_growth) ** (i + 1)
        future_revenues.append(future_rev)

    return future_revenues


future_revenues = future_revenues(hist_total_revenue, avg_rev_growth)


# ### ii. Find forecasted Net Income
def future_netincomes(future_revenues, avg_netincome_margin):
    future_netincomes = []

    for i in range(NUM_OF_YEARS):
        future_NI = future_revenues[i] * avg_netincome_margin
        future_netincomes.append(future_NI)

    return future_netincomes


future_netincomes = future_netincomes(future_revenues, avg_netincome_margin)


# ### ii. Find forecasted FCF
def future_FCFs(future_netincomes, avg_FCF_margin):
    future_FCFs = []

    for i in range(NUM_OF_YEARS):
        future_fcf = future_netincomes[i] * avg_FCF_margin
        future_FCFs.append(future_fcf)

    return future_FCFs


future_FCFs = future_FCFs(future_netincomes, avg_FCF_margin)


# # Step 3. Find the required rate of return WACC
# ## 3.1 Find the cost of equity
def capm_calculator():
    # Get beta 
    beta = ticker_object.info['beta']
    if beta is None:
        while True:
            try:
                beta = float(input("There is no beta available for this ticker\nPlease input your own beta: "))
                beta_test = beta / 1
                break
            except ValueError:
                continue

                # Get expected market return
    while True:
        r_m = input(
            "Would you like to use your own expected market return?\nIf no, the default rate will be 10%\nType in "
            "'Y' or 'N': ")
        if r_m.lower() == 'y' or r_m.lower() == 'n':
            break
        else:
            continue

    if r_m.lower() == 'y':
        while True:
            try:
                r_m = input("Please input your preferred expected market return in %: ")
                r_m = float(r_m) / 100
                break
            except ValueError:
                print('Please enter a valid number')
    elif r_m.lower() == 'n':
        r_m = 0.10

    # Get risk free rate
    bond = yf.Ticker('^TNX')
    r_f = bond.info['regularMarketPrice'] / 100

    # Calculate cost of equity
    r_e = r_f + beta * (r_m - r_f)

    print(f'\nbeta is:  {beta:.2f}')
    print(f'risk-free rate based on US 10 Treasury Yield is: {(r_f * 100):.2f}%')
    print(f'expected market return is: {(r_m * 100):.2f}%')

    return r_e


while True:
    r_e = input(
        "\nWould you like to use your own cost of equity?\n"
        "If no, the default rate will be calculated based on CAPM\n"
        "Type  in 'Y' or 'N': ")
    if r_e.lower() == 'y' or r_e.lower() == 'n':
        break
    else:
        continue

if r_e.lower() == 'y':
    while True:
        try:
            r_e = input("Please input your custom cost of equity in %: ")
            r_e = float(r_e) / 100
            break
        except ValueError:
            print('Please enter a valid number')
elif r_e.lower() == 'n':
    print(f"\nCalculating cost of equity using CAPM...\n")
    print('With CAPM, cost of equity = risk-free rate + (expected market return - risk-free rate)*beta')
    r_e = capm_calculator()

print(f'Therefore, cost of equity is: {(r_e * 100):.2f}%\n')


# ## 3.2 Find cost of debt
def cost_of_debt_calculator():
    # Accessing the balance sheet
    balancesheet_df = ticker_object.balancesheet

    # Find the historial total debt
    hist_total_debt = list(balancesheet_df.loc['Short Long Term Debt'] + balancesheet_df.loc['Long Term Debt'])

    # Find the historical interest expense
    hist_interest_exp = list(financials_df.loc['Interest Expense'])

    # Find the average cost of debt
    hist_r_d = [abs(hist_interest_exp[i] / hist_total_debt[i]) for i in range(NUM_OF_YEARS)]
    avg_hist_r_d = sum(hist_r_d) / len(hist_r_d)

    return avg_hist_r_d


# Getting cost of debt
while True:
    r_d = input(
        "Would you like to use your own cost of debt?\n"
        "If no, the default rate will be calculated based on historical income statement and balance sheet values\n"
        "Type  in 'Y' or 'N': ")
    if r_d.lower() == 'y' or r_d.lower() == 'n':
        break
    else:
        continue

if r_d.lower() == 'y':
    while True:
        try:
            r_d = input("Please input your custom cost of debt in %: ")
            r_d = float(r_d) / 100
            break
        except ValueError:
            print('Please enter a valid number')
elif r_d.lower() == 'n':
    r_d = cost_of_debt_calculator()

print(f'\nCost of debt is: {(r_d * 100):.2f}%\n')


# ## 3.3 Find the effective tax rate
def effective_tax_calculator():
    hist_incomeb4_tax = list(financials_df.loc['Income Before Tax'])
    hist_tax_expense = list(financials_df.loc['Income Tax Expense'])

    hist_eff_tax_rate = [abs(hist_tax_expense[i]) / abs(hist_incomeb4_tax[i]) for i in range(NUM_OF_YEARS)]
    avg_eff_tax_rate = sum(hist_eff_tax_rate) / len(hist_eff_tax_rate)

    return avg_eff_tax_rate


# Getting effective tax rate
while True:
    tax_rate = input(
        "Would you like to use your own effective tax rate?\n"
        "If no, the default rate will be calculated based on historical income statement values\n"
        "Type  in 'Y' or 'N': ")
    if tax_rate.lower() == 'y' or tax_rate.lower() == 'n':
        break
    else:
        continue

if tax_rate.lower() == 'y':
    while True:
        try:
            tax_rate = input("Please input your custom tax rate in %: ")
            tax_rate = float(tax_rate) / 100
            break
        except ValueError:
            print('Please enter a valid number')
elif tax_rate.lower() == 'n':
    tax_rate = effective_tax_calculator()

print(f'\nEffective tax rate is: {(tax_rate * 100):.2f}%')


# ## 3.4 Find WACC
def wacc_calculator(r_e, r_d, tax_rate):
    # Getting the weight of debt and equity
    equity_value = ticker_object.info['marketCap']
    debt_value = ticker_object.info['totalDebt']
    total_value = equity_value + debt_value

    weight_of_equity = equity_value / total_value
    weight_of_debt = debt_value / total_value

    WACC = weight_of_debt * r_d * (1 - tax_rate) + weight_of_equity * r_e

    return WACC


cost_of_capital = wacc_calculator(r_e, r_d, tax_rate)
print(f'The cost of capital (WACC) is: {(cost_of_capital * 100):.2f}%\n')


# # Step 4. Find the present value of all future FCF
# ## 4.1 Find the discount factor
def discount_factors(cost_of_capital):
    """
    Returns a list of discount factors
    """

    discount_factors = []
    for i in range(NUM_OF_YEARS):
        d_factor = 1 / (1 + cost_of_capital) ** (i + 1)
        discount_factors.append(d_factor)

    return discount_factors


discount_factors = discount_factors(cost_of_capital)

# ## 4.2 Find the PV of forecasted FCF
def pv_forecasted_FCF(future_FCFs, discount_factors):
    pv_forecasted_FCF = []
    for i in range(NUM_OF_YEARS):
        pv_forecasted_FCF.append(future_FCFs[i] * discount_factors[i])

    return pv_forecasted_FCF


pv_forecasted_FCF = pv_forecasted_FCF(future_FCFs, discount_factors)


# ## 4.3 Find the terminal value and its PV
def pv_terminal_value(future_FCFs, cost_of_capital, discount_factors):
    # First, we need to determine the growth rate
    # Default growth rate will be 2.5%
    while True:
        growth_rate = input(
            "Would you like to use your own perpetual growth rate?\n"
            "If no, the default rate will be 2.5%\n"
            "Type  in 'Y' or 'N': ")
        if growth_rate.lower() == 'y' or growth_rate.lower() == 'n':
            break
        else:
            continue

    if growth_rate.lower() == 'y':
        while True:
            try:
                growth_rate = input("Please input your custom tax rate in %: ")
                growth_rate = float(growth_rate) / 100
                break
            except ValueError:
                print('Please enter a valid number')
    elif growth_rate.lower() == 'n':
        growth_rate = 0.025

    # Calculate terminal value 
    terminal_value = (future_FCFs[-1] * (1 + growth_rate)) / (cost_of_capital - growth_rate)

    # Calculate the PV of terminal value
    pv_terminal_value = terminal_value * discount_factors[-1]

    return pv_terminal_value


pv_terminal_value = pv_terminal_value(future_FCFs, cost_of_capital, discount_factors)

# ## 4.4 Find the sum of the PV of all future FCF
pv_forecasted_FCF.append(pv_terminal_value)
pv_all_future_FCF = pv_forecasted_FCF


# # Step 5 (FINAL STEP). Find the intrinsic value of the stock
def intrinsic_value(pv_all_future_FCF):
    # Get the number of shares outstanding
    num_shares_outstanding = ticker_object.info['sharesOutstanding']

    intrinsic_value = sum(pv_all_future_FCF) / num_shares_outstanding

    return intrinsic_value


intrinsic_value = intrinsic_value(pv_all_future_FCF)

print(f'\nThe intrinsic value of the ticker {(ticker).upper()}, based '
      f'on the discounted free cash flow analysis is: ${intrinsic_value:.2f}')
