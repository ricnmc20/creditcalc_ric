import math
import argparse
import os
import sys
from contextlib import redirect_stderr


def credit_interest(number_months):
    if number_months is None:
        return 0
    else:
        return number_months / (12 * 100)


def credit_payment(principal, periods, interest):
    if principal is None:
        return 0
    else:
        return principal * ((interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1))


def credit_principal(payment, periods, interest):
    if payment is None:
        return 0
    else:
        return payment / ((interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1))


def credit_periods(principal, payment, interest):
    if principal is None:
        return 0
    else:
        return math.log(payment / (payment - interest * principal), 1 + interest)


def credit_diff(principal, periods, interest, month):
    if principal is None:
        return 0
    else:
        return (principal / periods) + interest * (principal - (principal * (month - 1) / periods))


def credit_diff_month1(principal, periods, interest):
    if principal is None:
        return 0
    else:
        return (principal / periods) + interest * principal


parser = argparse.ArgumentParser(prog="Credit Calculator", description="Calculate credit payment")
parser.add_argument("--type", type=str)
parser.add_argument("--principal", type=float)
parser.add_argument("--payment", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)

try:
    with open(os.devnull, 'w') as f, redirect_stderr(f):
        args = parser.parse_args()
except SystemExit:
    print("Incorrect parameters")
    sys.exit()


if len(sys.argv) < 4 or args.interest is None or args.interest <= 0 or args.type is None:
    print("Incorrect parameters")
    exit()

type_ = args.type   # annuity or diff calculation
payment_ = args.payment   # monthly payment
principal_ = args.principal   # credit principal
periods_ = args.periods   # number of payments
interest_ = credit_interest(args.interest)

# Calculate annuity payment
if type_ == "annuity":
    if periods_ is None and args.principal > 0 and args.payment > 0:
        calculate_periods_months = math.ceil(credit_periods(principal_, payment_, interest_))
        if calculate_periods_months % 12 == 0:
            print(f'It will take {calculate_periods_months//12}  years to repay this loan!')
            print(f'Overpayment = {calculate_periods_months * payment_ - principal_:.0f}')
        else:
            print(f'It will take {calculate_periods_months//12} years and {calculate_periods_months % 12} '
                  f'months to repay this loan!')
            print(f'Overpayment = {calculate_periods_months * payment_ - principal_:.0f}')

    elif payment_ is None and args.principal > 0 and args.periods > 0:
        calculate_payment = math.ceil(credit_payment(principal_, periods_, interest_))
        print(f'Your monthly payment = {calculate_payment}!')
        print(f'Overpayment = {calculate_payment * periods_ - principal_:.0f}')

    elif principal_ is None and args.periods > 0 and args.payment > 0:
        calculate_principal = math.floor(credit_principal(payment_, periods_, interest_))
        print(f'Your load principal = {calculate_principal}!')
        print(f'Overpayment = {payment_ * periods_ - calculate_principal:.0f}')
    else:
        print("Incorrect parameters")
        exit()


# Calculate differentiated payment
if type_ == "diff" and (principal_ > 0 and periods_ > 0):
    calculate_diff = []
    for m in range(1, periods_ + 1):
        if m == 1:
            calculate_diff.append(math.ceil(credit_diff_month1(principal_, periods_, interest_)))
        else:
            calculate_diff.append(math.ceil(credit_diff(principal_, periods_, interest_, m)))
        print(f'Month {m}: payment is {calculate_diff[m - 1]}')
    print(f'\nOverpayment = {sum(calculate_diff) - principal_:.0f}')
else:
    print("Incorrect parameters")
    exit()


