from django.shortcuts import render
from .models import ExcelEntryRow
from .forms import CommonFilterForm
from .utils.excel_utils import ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession
from .services.transactionFilterService import FilterTransactions
from .services.calculateService import (
    GetCalculatedCurrentWallet,
    GetAmountPutInSoFar,
    GetRealizedGain,
    GetGroupedTransactionsByShares)
import datetime

initialAccountTypes = ['Normalny', 'IKE']
initialStartDate = datetime.datetime.now().date().replace(month=1, day=1)
initialEndDate = datetime.datetime.now().date()

def LoadData(request):
    if "GET" == request.method:
        dataFromSession = GetExcelDataFromSession(request)
        modelData = FilterTransactions(dataFromSession, initialAccountTypes)
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})
    else:
        excelData = ReadExcel(request.FILES["excel_file"])
        SaveExcelDataToSession(request, excelData)
        modelData = FilterTransactions(excelData, initialAccountTypes)
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})


def Dashboard(request):
    form = CommonFilterForm()
    listOfAllTransactionsForSpecificAccountType = []
    dataFromSession = GetExcelDataFromSession(request)

    accountTypes = initialAccountTypes
    startDate = initialStartDate
    endDate = initialEndDate

    if request.method=='POST':
        form = CommonFilterForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            accountTypes = cleanedData.get('accountType')
            startDate = cleanedData.get('startDate')
            endDate = cleanedData.get('endDate')
    else:
        form.fields['accountType'].initial = accountTypes
        form.fields['startDate'].initial = startDate
        form.fields['endDate'].initial = endDate

    listOfAllTransactionsForSpecificAccountType = FilterTransactions(dataFromSession, accountTypes)
    listOfAllTransactionsFiltered = FilterTransactions(dataFromSession, accountTypes, startDate, endDate)
    walletShares = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountType)
    amountPutInSoFar = GetAmountPutInSoFar(listOfAllTransactionsForSpecificAccountType)
    realizedGain = GetRealizedGain(listOfAllTransactionsForSpecificAccountType, startDate, endDate)
    stats = {
        'putInSoFar' : "{0:.0f}".format(amountPutInSoFar),
        'realizedGain': "{0:.0f}".format(realizedGain),
        'feeFromRealizedGain': "{0:.0f}".format(realizedGain * 0.19)
    }
    viewModel = {
        'form': form,
        'listOfAllTransactionsForSpecificAccountType': listOfAllTransactionsForSpecificAccountType,
        'walletShares': walletShares,
        'listOfAllTransactionsFiltered': listOfAllTransactionsFiltered,
        'stats': stats
        }
    return render(request, 'wallet/dashboard.html', viewModel)


def ShareDetails(request, shareName):
    dataFromSession = GetExcelDataFromSession(request)
    listOfAllTransactionsForSpecificAccountType = FilterTransactions(dataFromSession, initialAccountTypes)

    if "GET" == request.method:
        transactionsGoupedByShares = GetGroupedTransactionsByShares(listOfAllTransactionsForSpecificAccountType)
        if(shareName in transactionsGoupedByShares):
            currentShareTransactionList = list(reversed(transactionsGoupedByShares[shareName]))
            for transaction in currentShareTransactionList:
                transaction.listOfBuyTransactions = list(reversed(transaction.listOfBuyTransactions))
            currentShareTransactionListOnlySell = list(filter(lambda x: x.transactionType == 'S', currentShareTransactionList))
            gainAlreadyRealized = sum(transaction.realizedGain for transaction in currentShareTransactionListOnlySell)
            return render(request, 'wallet/shareDetails.html', {
                'shareTransactions': currentShareTransactionListOnlySell,
                'shareName': shareName,
                'gainAlreadyRealized': gainAlreadyRealized
                })
        return redirect('wallet-dashboard')
