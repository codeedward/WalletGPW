from django.shortcuts import render
from .models import ExcelEntryRow, ExcelEntryIkeRow
from .forms import CommonFilterForm
from .utils.excel_utils import ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession
from .utils.excel_utilsForIke import ReadExcelIke, GetExcelDataIkeFromSession, SaveExcelDataIkeToSession
from .services.transactionFilterService import FilterTransactions
from .services.calculateService import (
    GetCalculatedCurrentWallet,
    GetAmountPutInSoFar,
    GetRealizedGain,
    GetGroupedTransactionsByShares,
    GetGainAlreadyRealizedWithCurrentShares,
    GetIkeIncomeBalance,
    GetCashBalanceForTheAccount,
    GetDataForWalletChart,
    AddTheoreticalTransaction)
import datetime
from .services.rateService import getRate
import copy

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
        excelDataIke = ReadExcelIke(request.FILES["excel_file"])
        SaveExcelDataIkeToSession(request, excelDataIke)
        modelData = FilterTransactions(excelData, initialAccountTypes)
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})


def Dashboard(request):
    form = CommonFilterForm()
    listOfAllTransactionsForSpecificAccountType = []
    dataFromSession = GetExcelDataFromSession(request)
    dataFromSessionIke = GetExcelDataIkeFromSession(request)

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
    ikePutInValue = GetIkeIncomeBalance(dataFromSessionIke)
    walletShares = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountType)
    amountPutInSoFar = GetAmountPutInSoFar(listOfAllTransactionsForSpecificAccountType)
    cashBalanceForTheAccount = GetCashBalanceForTheAccount(listOfAllTransactionsForSpecificAccountType, amountPutInSoFar, ikePutInValue, accountTypes)
    print(f"Cash balance aprox:{cashBalanceForTheAccount}")
    realizedGain = GetRealizedGain(listOfAllTransactionsForSpecificAccountType, startDate, endDate)
    stats = {
        'putInSoFar' : "{0:.0f}".format(amountPutInSoFar),
        'realizedGain': "{0:.0f}".format(realizedGain),
        'feeFromRealizedGain': "{0:.0f}".format(realizedGain * 0.19)
    }
    chartInJsonFormat = GetDataForWalletChart(walletShares)
    viewModel = {
        'form': form,
        'listOfAllTransactionsForSpecificAccountType': listOfAllTransactionsForSpecificAccountType,
        'walletShares': walletShares,
        'listOfAllTransactionsFiltered': listOfAllTransactionsFiltered,
        'stats': stats,
        'chartData': chartInJsonFormat
        }
    return render(request, 'wallet/dashboard.html', viewModel)


def ShareDetails(request, shareName):
    dataFromSession = GetExcelDataFromSession(request)
    listOfAllTransactionsForSpecificAccountType = FilterTransactions(dataFromSession, initialAccountTypes)
    currentRate = getRate(shareName)

    if "POST" == request.method:
        accountTypeForTheoreticalTransaction = ''
        newTransactionQuantity = int(request.POST.get("newTransactionQuantity", 0))
        isTheoreticalIkeType = bool(request.POST.get("isTheoreticalIkeType", False))
        if(isTheoreticalIkeType):
            accountTypeForTheoreticalTransaction = 'IKE'
        else:
            accountTypeForTheoreticalTransaction = 'Normalny'
        listOfAllTransactionsForSpecificAccountType = AddTheoreticalTransaction(listOfAllTransactionsForSpecificAccountType, shareName, newTransactionQuantity, currentRate, accountTypeForTheoreticalTransaction)

    transactionsGoupedByShares = GetGroupedTransactionsByShares(listOfAllTransactionsForSpecificAccountType)
    currentWallet = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountType)

    if(shareName in transactionsGoupedByShares):
        currentShareTransactionList = list(reversed(transactionsGoupedByShares[shareName]))
        for transaction in currentShareTransactionList:
            transaction.listOfBuyTransactions = list(reversed(transaction.listOfBuyTransactions))

        currentShareTransactionListOnlySell = list(filter(lambda x: x.transactionType == 'S', currentShareTransactionList))
        gainAlreadyRealized = sum(transaction.realizedGain for transaction in currentShareTransactionListOnlySell)

        if(shareName in currentWallet):
            gainAlreadyRealizedWithCurrentShares = GetGainAlreadyRealizedWithCurrentShares(dataFromSession,
                listOfAllTransactionsForSpecificAccountType, shareName, currentRate)
            shareQuantity = currentWallet[shareName]
        else:
            gainAlreadyRealizedWithCurrentShares = 0
            shareQuantity = 0

        return render(request, 'wallet/shareDetails.html', {
            'shareTransactions': currentShareTransactionListOnlySell,
            'shareName': shareName,
            'shareQuantity': shareQuantity,
            'gainAlreadyRealized': gainAlreadyRealized,
            'currentRate': currentRate,
            'gainAlreadyRealizedWithCurrentShares': gainAlreadyRealizedWithCurrentShares
            })
    return redirect('wallet-dashboard')


