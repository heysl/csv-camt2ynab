import csv
from sys import argv
from datetime import datetime
import argparse


def csv2dicts(filename):
    csv_dict_list = []
    with open(filename, 'r') as input_file:
        reader = csv.DictReader(input_file, delimiter=';', quotechar='"')
        for row in reader:
            csv_dict_list.append(row)
    return csv_dict_list

def map_to_giro(input):
    result_list = []
    for d in input:
        date = d['Buchungstag'].replace('.', '/')
        payee = d['Beguenstigter/Zahlungspflichtiger'].replace(',', ' ')
        category = ''
        memo = d['Verwendungszweck'].replace(',', ' ')
        amount = d['Betrag'].replace(',', '.')
        if amount[0] == '-':
            outflow = amount.replace('-', '')
            inflow = ''
        else:
            outflow = ''
            inflow = amount
        result_list.append({'Date': date, 'Payee': payee, 'Category': category, 'Memo': memo, 'Outflow': outflow, 'Inflow': inflow})
    return result_list

def map_to_cc(input):
    result_list = []
    for d in input:
        date = d['Buchungsdatum'].replace('.', '/')
        payee = '{} {}'.format(d['Transaktionsbeschreibung'].replace(',', ' '), d['Transaktionsbeschreibung Zusatz'].replace(',', ' '))
        category = ''
        memo = ''
        amount = d['Buchungsbetrag'].replace(',', '.')
        if amount[0] == '-':
            outflow = amount.replace('-', '')
            inflow = ''
        else:
            outflow = ''
            inflow = amount
        result_list.append({'Date': date, 'Payee': payee, 'Category': category, 'Memo': memo, 'Outflow': outflow, 'Inflow': inflow})
    return result_list

def write_dict_to_csv(input, output_filename):
    with open(output_filename, 'w', newline='') as file:
        line_count = 0
        fieldnames = ['Date','Payee','Category','Memo','Outflow','Inflow']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for d in input:
            writer.writerow(d)
            line_count += 1
    return line_count

parser = argparse.ArgumentParser(description='Transform different csv-inputs for use with YNAB4')
parser.add_argument(
    dest='csv_input_filename',
    type=str,
    help='the csv file to be transformed'
)
parser.add_argument(
    '-c',
    dest='cc',
    action='store_true',
    help='input file is from credit card'
)

args = parser.parse_args()

# set filename for input
csv_input_filename = args.csv_input_filename
#csv_input_filename = './umsatz-5232________9563-20200106.csv'

# set filename for output
#csv_output_filename = "Import_{}.csv".format(datetime.strftime(datetime.now(), '%d-%m-%Y'))
csv_output_filename = 'test.csv'


input_list = csv2dicts(csv_input_filename)

if args.cc:
    csv_output_filename = 'cc_' + csv_output_filename
    mapped_csv_data = map_to_cc(input_list)
else:
    mapped_csv_data = map_to_giro(input_list)

line_count = write_dict_to_csv(mapped_csv_data, csv_output_filename)
print('Done! Wrote {} lines to file "{}".'.format(line_count, csv_output_filename))
