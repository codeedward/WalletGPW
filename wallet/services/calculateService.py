from .transactionFilterService import GetTransactionsSplitByShares
import copy
from dateutil import parser

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


def GetRealizedGain(listOfAllTransactionsForSpecificAccountType, startDate, endDate):
    transactionsGoupedBySharesOriginal = GetTransactionsSplitByShares(listOfAllTransactionsForSpecificAccountType)
    transactionsGoupedByShares = copy.deepcopy(transactionsGoupedBySharesOriginal)

    sum = 0
    for shareName, transactionList in transactionsGoupedByShares.items():
        currentList = transactionsGoupedByShares[shareName]
        for transactionSell in currentList:
            if(transactionSell.transactionType == 'S'):
                if(startDate <= parser.parse(transactionSell.date).date() <= endDate):
                    print(f"-----For {shareName} - sell:{transactionSell.date} amount:{transactionSell.quantity}")
                temporarySumForBatchOfBuyTransactions = 0
                for transactionBuy in currentList:
                    if(transactionBuy.transactionType == 'K' and transactionBuy.quantity > 0):
                        amountToMultiply = 0

                        if(transactionSell.quantity > transactionBuy.quantity):
                            amountToMultiply = transactionBuy.quantity
                            transactionSell.quantity -= amountToMultiply
                            transactionBuy.quantity = 0
                        else:
                            amountToMultiply = transactionSell.quantity
                            transactionBuy.quantity -= amountToMultiply
                            transactionSell.quantity = 0

                        if(startDate <= parser.parse(transactionSell.date).date() <= endDate):
                            print(f"buy:{transactionBuy.date} amount deducted:{amountToMultiply}")
                            temporarySumForBatchOfBuyTransactions += amountToMultiply * (float(transactionSell.price.replace(",", ".")) - float(transactionBuy.price.replace(",", ".")))

                        if(transactionSell.quantity == 0 and startDate <= parser.parse(transactionSell.date).date() <= endDate):
                            print(f"::Total result of Sell:{temporarySumForBatchOfBuyTransactions}")
                            sum += temporarySumForBatchOfBuyTransactions;
                        if(transactionSell.quantity == 0):
                            break

    return sum


