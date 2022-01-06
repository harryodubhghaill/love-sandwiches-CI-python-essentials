import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():

    """
    Gets sales figures from user. While loop will run the 
    function until user enters valid data. This should be 
    a list of 6 ints separated by commas.
    """
    while True:
        print("Please enter sales data from last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50.60\n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is Valid!")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all values to ints, raises 
    ValueError if string cant be converted or if there 
    arent exactly 6 value points.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with data
    list provided by user.
    """
    print("Updating sales worksheet... \n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data... \n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    """
    Calls main functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome to Love Sandwiches data Automation")
main()
