from django.db import models
import json
import datetime
from dateutil import parser

class ExcelEntryRow():
    date = datetime.datetime.now()
    transactionType = '' #{S,K}
    name = ''
    quantity = ''
    price = ''
    transactionValue = ''
    fee = ''
    balanceChange = ''
    accountType = '' #{Normalny,IKE}

    realizedGain = 0
    quantityForCalculation = 0
    listOfBuyTransactions = []
    isRealTransaction = True

    def __init__(self, row = None, isRealTransaction = True):
        if type(row) is tuple:
            self.date = TryParseDate(row[0].value)
            self.transactionType = row[1].value
            self.name = row[2].value
            self.quantity = row[3].value
            self.price = row[4].value
            self.transactionValue = row[5].value
            self.fee = row[6].value
            self.balanceChange = row[7].value
            self.accountType = row[10].value

        elif type(row) is dict:
            self.date = TryParseDate(row['date'])
            self.transactionType = row['transactionType']
            self.name = row['name']
            self.quantity = row['quantity']
            self.price = row['price']
            self.transactionValue = row['transactionValue']
            self.fee = row['fee']
            self.balanceChange = row['balanceChange']
            self.accountType = row['accountType']

        self.quantityForCalculation = self.quantity
        self.isRealTransaction = isRealTransaction

class TransactionBuyTakenToRealizeSell():
    date = ''
    transactionType = '' #{S,K}
    name = ''
    quantity = 0
    quantityRealized = 0
    price = 0

    def __init__(self, transactionBuy, quantityRealized):
        self.date = transactionBuy.date
        self.transactionType = transactionBuy.transactionType
        self.name = transactionBuy.name
        self.quantity = transactionBuy.quantity
        self.quantityRealized = quantityRealized
        self.price = transactionBuy.price


class ExcelEntryIkeRow():
    date = datetime.datetime.now()
    quantity = ''

    def __init__(self, row = None):
        if type(row) is tuple:
            self.date = row[0].value
            self.quantity = row[2].value

        elif type(row) is dict:
            self.date = row['date']
            self.quantity = row['quantity']


def TryParseDate(value):
    try:
        return parser.parse(value).date()
    except:
        return value
