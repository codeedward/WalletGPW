from django.shortcuts import render
from .models import ExcelEntryRow
from .forms import CommonFilterForm
from .utils.excel_utils import FilterExcel, ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession
from .services.calculateService import GetCalculatedCurrentWallet
import datetime

initialAccountTypes = ['Normalny', 'IKE']
initialStartDate = datetime.datetime.now().date().replace(month=1, day=1)
initialEndDate = datetime.datetime.now().date()

def LoadData(request):

    if "GET" == request.method:
        dataFromSession = GetExcelDataFromSession(request)
        modelData = FilterExcel(dataFromSession, initialAccountTypes)
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})
    else:
        excelData = ReadExcel(request.FILES["excel_file"])
        SaveExcelDataToSession(request, excelData)
        modelData = FilterExcel(excelData, initialAccountTypes)
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
            print(f"Start date={startDate}")
            print(f"End date={endDate}")
    else:
        form.fields['accountType'].initial = accountTypes
        form.fields['startDate'].initial = startDate
        form.fields['endDate'].initial = endDate

    listOfAllTransactionsForSpecificAccountType = FilterExcel(dataFromSession, accountTypes)
    listOfAllTransactionsFiltered = FilterExcel(dataFromSession, accountTypes, startDate, endDate)
    walletShares = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountType)
    viewModel = {
        'form': form,
        "listOfAllTransactionsForSpecificAccountType": listOfAllTransactionsForSpecificAccountType,
        'walletShares': walletShares,
        'listOfAllTransactionsFiltered': listOfAllTransactionsFiltered
        }
    return render(request, 'wallet/dashboard.html', viewModel)
