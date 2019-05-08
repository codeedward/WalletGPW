from .transactionFilterService import GetTransactionsSplitByShares,FilterTransactions
import copy
from dateutil import parser
from ..models import TransactionBuyTakenToRealizeSell, ExcelEntryRow
from ..utils.excel_utils import GetExcelDataFromSession
import datetime
from .rateService import getRate
import json

def GetCalculatedCurrentWallet(listOfTransactions):
    walletShares = {}
    for transaction in listOfTransactions:
        if(transaction.name not in walletShares):
            if(transaction.transactionType == 'K'):
                walletShares[transaction.name] = transaction.quantity
        else:
            if(transaction.transactionType == 'K'):
                walletShares[transaction.name] += float(transaction.quantity);
            elif(transaction.transactionType == 'S'):
                walletShares[transaction.name] -= float(transaction.quantity);
                if(walletShares[transaction.name] == 0):
                    del walletShares[transaction.name]
    return walletShares


def GetAmountPutInSoFar(listOfTransactions):
    sum = 0
    for transaction in listOfTransactions:
     if(transaction.transactionType == 'Wplata'):
        sum += float(transaction.balanceChange.replace(",", "."));
    return sum

def GetGroupedTransactionsByShares(listOfAllTransactionsForSpecificAccountType):
    transactionsGoupedBySharesOriginal = GetTransactionsSplitByShares(listOfAllTransactionsForSpecificAccountType)
    transactionsGoupedByShares = copy.deepcopy(transactionsGoupedBySharesOriginal)

    sum = 0
    for shareName, transactionList in transactionsGoupedByShares.items():
        currentList = transactionsGoupedByShares[shareName]
        for transactionSell in currentList:
            transactionSell.listOfBuyTransactions = []
            if(transactionSell.transactionType == 'S'):
                #if(startDate <= parser.parse(transactionSell.date).date() <= endDate):
                    #print(f"-----For {shareName} - sell:{transactionSell.date} amount:{transactionSell.quantity}")
                temporarySumForBatchOfBuyTransactions = 0
                for transactionBuy in currentList:
                    if(transactionBuy.transactionType == 'K' and
                        transactionBuy.quantityForCalculation > 0 and
                        transactionBuy.accountType == transactionSell.accountType):

                        amountToMultiply = 0

                        if(transactionSell.quantityForCalculation > transactionBuy.quantityForCalculation):
                            amountToMultiply = transactionBuy.quantityForCalculation
                            transactionSell.quantityForCalculation -= amountToMultiply
                            transactionBuy.quantityForCalculation = 0
                        else:
                            amountToMultiply = transactionSell.quantityForCalculation
                            transactionBuy.quantityForCalculation -= amountToMultiply
                            transactionSell.quantityForCalculation = 0

                        #print(f"buy:{transactionBuy.date} amount deducted:{amountToMultiply}")
                        temporarySumForBatchOfBuyTransactions += amountToMultiply * (float(transactionSell.price.replace(",", ".")) - float(transactionBuy.price.replace(",", ".")))
                        transactionBuyToRealizeGain = TransactionBuyTakenToRealizeSell(transactionBuy, amountToMultiply)
                        transactionSell.listOfBuyTransactions.append(transactionBuyToRealizeGain)

                        if(transactionSell.quantityForCalculation == 0):
                            #print(f"::Total result of Sell:{temporarySumForBatchOfBuyTransactions}")
                            #sum += temporarySumForBatchOfBuyTransactions;
                            transactionSell.realizedQuantity = temporarySumForBatchOfBuyTransactions;
                            transactionSell.realizedGain = temporarySumForBatchOfBuyTransactions
                            #print(len(transactionSell.listOfBuyTransactions))
                            break

    return transactionsGoupedByShares


def GetRealizedGain(listOfAllTransactionsForSpecificAccountType, startDate, endDate):
    transactionsGoupedByShares = GetGroupedTransactionsByShares(listOfAllTransactionsForSpecificAccountType)
    sum = 0
    for shareName, transactionList in transactionsGoupedByShares.items():
        currentList = transactionsGoupedByShares[shareName]
        for transactionSell in currentList:
            if(transactionSell.transactionType == 'S' and startDate <= transactionSell.date <= endDate):
                sum += transactionSell.realizedGain
    return sum


def GetGainAlreadyRealizedWithCurrentShares(dataFromSession, listOfAllTransactionsForSpecificAccountType, shareName, currentRate):
    listOfAllTransactionsForSpecificAccountTypeNormal = FilterTransactions(dataFromSession, ['Normalny'])
    listOfAllTransactionsForSpecificAccountTypeIKE = FilterTransactions(dataFromSession, ['IKE'])
    listOfAllTransactionsForSpecificAccountTypeWithCurrentWalletShares = copy.deepcopy(listOfAllTransactionsForSpecificAccountType)

    currentWalletNormal = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountTypeNormal)
    currentWalletIKE = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountTypeIKE)

    if(shareName in currentWalletNormal):
        listOfAllTransactionsForSpecificAccountTypeWithCurrentWalletShares.append(ExcelEntryRow({
        'date' : datetime.date.today(),
        'transactionType' : 'S',
        'name' : shareName,
        'price' : str(currentRate),
        'quantity' : currentWalletNormal[shareName],
        'accountType' : 'Normalny',
        'transactionValue' : currentRate*currentWalletNormal[shareName],
        'fee': 0,
        'balanceChange': 0,
        'isRealTransaction' : 0
        }, False))

    if(shareName in currentWalletIKE):
        listOfAllTransactionsForSpecificAccountTypeWithCurrentWalletShares.append(ExcelEntryRow({
        'date' : datetime.date.today(),
        'transactionType' : 'S',
        'name' : shareName,
        'price' : str(currentRate),
        'quantity' : currentWalletIKE[shareName],
        'accountType' : 'IKE',
        'transactionValue' : currentRate*currentWalletIKE[shareName],
        'fee': 0,
        'balanceChange': 0,
        }, False))

        transactionsGoupedBySharesWithCurrentWalletShares = GetGroupedTransactionsByShares(listOfAllTransactionsForSpecificAccountTypeWithCurrentWalletShares)
        currentShareTransactionListWithCurrentWalletShares = transactionsGoupedBySharesWithCurrentWalletShares[shareName]
        currentShareTransactionListOnlySellWithCurrentWalletShares = list(filter(lambda x: x.transactionType == 'S', currentShareTransactionListWithCurrentWalletShares))
        realizedGainWithCurrentWalletShares = sum(transaction.realizedGain for transaction in currentShareTransactionListOnlySellWithCurrentWalletShares)
        return realizedGainWithCurrentWalletShares


def GetIkeIncomeBalance(listOfTransactionsForIke):
    sum = 0
    for entry in listOfTransactionsForIke:
        sum += entry.quantity;
    return sum

def GetCashBalanceForTheAccount(listOfTransactions, amountPutInSoFar, ikePutInValue, accountTypes):
    sum = 0
    for transaction in listOfTransactions:
        if(transaction.transactionType != 'Wplata' and transaction.accountType in accountTypes):
            sum += float(transaction.balanceChange.replace(",", "."));

    if(all(accountType == 'Normalny' for accountType in accountTypes)):
        sum += (amountPutInSoFar - ikePutInValue)
    elif(all(accountType == 'IKE' for accountType in accountTypes)):
        sum += ikePutInValue
    else:
        sum += amountPutInSoFar

    return sum


def GetDataForWalletChart(walletShares):
    walletChartData = []
    for index, (rowName, quantity) in enumerate(walletShares.items()):
        walletChartData.append({
                'name' : rowName,
                'y' : int(quantity * getRate(rowName))
            })
    walletChartObj = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Wallet engagement'},
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'series': [{
            'name': 'Engagement',
            'data': walletChartData
        }]
    }
    chartInJsonFormat = json.dumps(walletChartObj)
    return chartInJsonFormat


def AddTheoreticalTransaction(listOfTransactions, shareName, quantity, currentRate, accountType = 'Normalny'):

    listOfTransactions.append(ExcelEntryRow({
    'date' : datetime.date.today(),
    'transactionType' : 'S',
    'name' : shareName,
    'price' : str(currentRate),
    'quantity' : quantity,
    'accountType' : accountType,
    'transactionValue' : currentRate*quantity,
    'fee': 0,
    'balanceChange': 0,
    'isRealTransaction' : 0
    }, False))

    return listOfTransactions
