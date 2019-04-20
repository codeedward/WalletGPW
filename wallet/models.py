from django.db import models

class ExcelEntryRow():
    date = ''
    transactionType = '' #{Normalny,IKE}
    name = ''
    quantity = ''
    price = ''
    transactionValue = ''
    fee = ''
    balanceChange = ''
    accountType = ''

    def __init__(self, row):
        self.date = row[0].value
        self.transactionType = row[1].value
        self.name = row[2].value
        self.quantity = row[3].value
        self.price = row[4].value
        self.transactionValue = row[5].value
        self.fee = row[6].value
        self.balanceChange = row[9].value
        self.accountType = row[10].value
