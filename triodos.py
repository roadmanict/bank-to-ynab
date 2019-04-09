import sys
import csv
from datetime import datetime

accounts = {
    'personal': 'NL61TRIO0379584190',
    'savings': 'NL32TRIO2017913936',
}


def convert(file):
    personal_list = list()
    shared_list = list()

    with open(file, encoding='iso-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            amount = float(row[2].replace('.', '').replace(',', '.'))
            outflow = ''
            inflow = ''
            if row[3] == "Debet":
                outflow = str(amount)
            else:
                inflow = str(amount)

            ynab_row = (convert_date(row[0]), row[7], row[4], outflow, inflow)

            if row[1] == accounts['personal']:
                personal_list.append(ynab_row)
            elif row[1] == accounts['shared']:
                shared_list.append(ynab_row)

    with open('triodos_personal.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(personal_list)

        # for row in ynab_values:
        #     writer.writerow([row[0], row[1], row[2], row[3], row[4]])

    with open('triodos_shared.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(shared_list)

        # for row in ynab_values:
        #     writer.writerow([row[0], row[1], row[2], row[3], row[4]])


def convert_date(date):
    return str(datetime.strptime(date, '%d-%m-%Y').strftime('%m/%d/%Y'))


if __name__ == '__main__':
    convert(sys.argv[1])
