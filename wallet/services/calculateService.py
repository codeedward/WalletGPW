

def GetCalculatedCurrentWallet(listOfTransactions):
    walletShares = {}
    for transaction in listOfTransactions:
        #print(f"Processing {transaction.name} with value {transaction.quantity}")
        if(transaction.name not in walletShares):
            if(transaction.transactionType == 'K'):
                walletShares[transaction.name] = transaction.quantity
                #print(f"Created {transaction.name} with value {transaction.quantity}")
        else:
            if(transaction.transactionType == 'K'):
                #print(f"Trying to add {transaction.name} with value {transaction.quantity}")
                walletShares[transaction.name] += float(transaction.quantity);
            elif(transaction.transactionType == 'S'):
                #print(f"Trying to substract {transaction.name} with value {transaction.quantity}")
                walletShares[transaction.name] -= float(transaction.quantity);
                if(walletShares[transaction.name] == 0):
                    del walletShares[transaction.name]
    return walletShares


def GetAmountPutInSoFar(listOfTransactions):
    sum = 0
    for transaction in listOfTransactions:
     if(transaction.transactionType == 'Wplata'):
        print(f"Trying to add {transaction.transactionType} {transaction.date} with value {transaction.balanceChange}")
        sum += float(transaction.balanceChange.replace(",", "."));
    return sum
