from dateutil import parser

def FilterTransactions(listOfExcelRows, accountTypes, startDate = None, endDate = None):
    return list(filter(lambda x: filterTransactions(x, accountTypes, startDate, endDate), listOfExcelRows))

def filterTransactions(excelEntryRow, accountTypes, startDate, endDate):
    if(excelEntryRow.accountType in accountTypes and
        ((startDate is None and endDate is None) or
            (startDate is not None and endDate is not None and startDate <= excelEntryRow.date <= endDate))
        ):
        return True
    return False

def GetTransactionsSplitByShares(listOfAllTransactions):
    groupedShares = {}
    for transaction in listOfAllTransactions:
        if(transaction.name not in groupedShares):
            groupedShares[transaction.name] = []
        groupedShares[transaction.name].append(transaction)
    return groupedShares
