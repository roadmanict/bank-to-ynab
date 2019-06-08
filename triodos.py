import sys
import csv
from datetime import datetime

accounts = {
    'personal': 'NL61TRIO0379584190',
    'savings': 'NL32TRIO2017913936',
    'gezamelijk': 'NL23TRIO0379565668',
    'gezamelijk_savings': 'NL08TRIO2017900303',
}


def convert(file):
    personal_list = list()
    savings_list = list()
    gezamelijk_list = list()
    gezamelijk_savings_list = list()

    with open(file, encoding='iso-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            amountValue = row[2]
            isDebet = row[3] == "Debet"
            dateValue = row[0]
            description = row[7]
            payee = row[4]

            if not payee:
                payee = description
                description = ""
            
            amount = float(amountValue.replace('.', '').replace(',', '.'))
            outflow = ''
            inflow = ''
            if isDebet:
                outflow = str(amount)
            else:
                inflow = str(amount)

            ynab_row = (convert_date(dateValue), payee, description, outflow, inflow)

            if row[1] == accounts['personal']:
                personal_list.append(ynab_row)
            elif row[1] == accounts['savings']:
                savings_list.append(ynab_row)
            elif row[1] == accounts['gezamelijk']:
                gezamelijk_list.append(ynab_row)
            elif row[1] == accounts['gezamelijk_savings']:
                gezamelijk_savings_list.append(ynab_row)

    with open('triodos_personal.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(personal_list)

        # for row in ynab_values:
        #     writer.writerow([row[0], row[1], row[2], row[3], row[4]])

    with open('triodos_savings.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(savings_list)

    with open('gezamelijk.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(gezamelijk_list)

    with open('gezamelijk_savings.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])

        writer.writerows(gezamelijk_savings_list)

        # for row in ynab_values:
        #     writer.writerow([row[0], row[1], row[2], row[3], row[4]])


def convert_date(date):
    return str(datetime.strptime(date, '%d-%m-%Y').strftime('%m/%d/%Y'))


if __name__ == '__main__':
    convert(sys.argv[1])
