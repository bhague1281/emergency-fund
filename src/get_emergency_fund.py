from dotenv import load_dotenv, find_dotenv
from functools import reduce
from mintapi import Mint

import json
import os

def get_user_data_path():
    """Return the file path for the user data"""
    current_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_directory, 'emergency_fund_info.json')


def get_user_data():
    """
    Return a dictionary containing user data
    (emergency fund account id and expenses per month)
    """

    file_path = get_user_data_path()

    if os.path.isfile(file_path):
        try:
            with open(file_path) as data:
                return json.load(data)
        except:
            return None
    else:
        return None


def write_user_data(accounts, budget):
    """
    Ask the user to select an emergency fund account and a monthly expense budget,
    then write that user data to a JSON file. Return the user data that was written
    """

    print('Your current expense budget (from Mint): {0}\n\n'.format(int(get_expenses(budget))))
    print('Your Accounts\n------------------------\n\n')

    for idx, account in enumerate(accounts):
        account_values = {
            'idx': idx,
            'name': account['accountName'],
            'display_name': account['fiLoginDisplayName'],
            'currentBalance': account['currentBalance']
        }
        print('{idx}: {name} ({display_name}) {currentBalance}'.format_map(account_values))

    account_idx = input('\n\nSelect an account (by number): ')
    monthly_expenses = input('\nInput your monthly expenses: ')
    account_idx = int(account_idx)
    monthly_expenses = float(monthly_expenses)

    user_data = {
        'account_id': accounts[account_idx]['accountId'],
        'monthly_expenses': monthly_expenses
    }

    with open(get_user_data_path(), 'w') as outfile:
        json.dump(user_data, outfile)

    return user_data


def get_expenses(budget):
    """Return the sum of expenses from a budget"""
    return sum(expense['bgt'] for expense in budget['spend'])


def valid_user_data(user_data):
    """Return if the dictionary has the required data to calculate runway"""
    return 'account_id' in user_data and 'monthly_expenses' in user_data


def emergency_fund_runway(accounts, account_id, monthly_expenses):
    """
    Calculate the "runway", or number of months that the emergency fund
    will last with the given expenses. Return a message to print to the user
    """

    account = [a for a in accounts if a['accountId'] == account_id]
    if len(account) == 1:
        runway_amount = int(account[0]['currentBalance'] / monthly_expenses)
        return 'Your emergency fund has a runway of {0} months.'.format(runway_amount)
    else:
        return 'That account cannot be found'


def main():
    """
    Login to Mint, get accounts and emergency fund info (if available),
    and calculate the emergency runway. If no info is available, ask the
    user to select one of their accounts and list their monthly expenses.
    """

    # load environment variables from .env file
    load_dotenv(find_dotenv())

    # get email and password from environment and log in
    email = os.environ.get('MINT_EMAIL')
    password = os.environ.get('MINT_PASSWORD')

    mint = Mint(email, password)
    accounts = mint.get_accounts()
    budget = mint.get_budgets()

    user_data = get_user_data()

    if not user_data or not valid_user_data(user_data):
        print('You need to select an account and your emergency fund info')
        user_data = write_user_data(accounts, budget)
        print('Your information has been saved for future use.')

    print(emergency_fund_runway(accounts, **user_data))

main()
