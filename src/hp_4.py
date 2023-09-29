# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    formatted_dates = []

    for date_str in old_dates:
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_object.strftime('%d %b %Y')
        formatted_dates.append(formatted_date)
    return formatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("The 'start' parameter should be a string in 'yyyy-mm-dd' format")

    if not isinstance(n, int):
        raise TypeError("The 'n' parameter should be an integer")

    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_list = [start_date + timedelta(days=i) for i in range(n)]
    return date_list


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    
    date_range_list = date_range(start_date, len(values))
    result = list(zip(date_range_list, values))
    return result


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees_by_patron = defaultdict(float)

    with open(infile, mode='r', newline='') as input_file:
        csv_reader = csv.DictReader(input_file)

        for row in csv_reader:
            date_checkout = datetime.strptime(row['checkout_date'], '%m/%d/%Y')
            date_due = datetime.strptime(row['due_date'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['return_date'], '%m/%d/%Y')

            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
                patron_id = row['patron_id']
                late_fees_by_patron[patron_id] += late_fee

    with open(outfile, mode='w', newline='') as output_file:
        fieldnames = ['patron_id', 'late_fees']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for patron_id, late_fee in late_fees_by_patron.items():
            csv_writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fee)})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
