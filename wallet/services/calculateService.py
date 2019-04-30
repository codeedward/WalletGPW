from .transactionFilterService import GetTransactionsSplitByShares
import copy
from dateutil import parser
from ..models import TransactionBuyTakenToRealizeSell

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
            if(transactionSell.transactionType == 'S' and startDate <= parser.parse(transactionSell.date).date() <= endDate):
                sum += transactionSell.realizedGain
    return sum

