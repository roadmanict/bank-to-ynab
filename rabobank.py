import sys
import csv
from datetime import datetime

accounts = {
    'personal': 'NL58RABO0315527595',
    'shared': 'NL12RABO0166481327',
}


def convert(file):
    personal_list = list()
    shared_list = list()

    with open(file, encoding='iso-8859-1') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            amount = float(row[6].replace(',', '.'))
            outflow = ''
            inflow = ''
            if amount < 0:
                outflow = str(abs(amount))
            else:
                inflow = str(amount)

            ynab_row = (convert_date(row[5]), row[9], row[19], outflow, inflow)

            if row[0] == accounts['personal']:
                personal_list.append(ynab_row)
            elif row[0] == accounts['shared']:
                shared_list.append(ynab_row)

    with open('personal.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(personal_list)

        # for row in ynab_values:
        #     writer.writerow([row[0], row[1], row[2], row[3], row[4]])

    with open('shared.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(shared_list)

        # for row in ynab_values:
        #     writer.writerow([row[0], row[1], row[2], row[3], row[4]])


def convert_date(date):
    return str(datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y'))


if __name__ == '__main__':
    convert(sys.argv[1])
