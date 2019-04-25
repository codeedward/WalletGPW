from django.shortcuts import render
from .models import ExcelEntryRow
from .forms import CommonFilterForm
from .utils.excel_utils import FilterExcel, ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession
from .services.calculateService import GetCalculatedCurrentWallet
import datetime

initialAccountTypes = ['Normalny', 'IKE']
initialStartDate = datetime.datetime.now().date().replace(month=1, day=1)
initialEndDate = datetime.datetime.now()

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

    if request.method=='POST':
        form = CommonFilterForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            accountTypes = cleanedData.get('accountType')
            startDate = cleanedData.get('startDate')
            endDate = cleanedData.get('endDate')
            print(f"Start date={startDate}")
            print(f"End date={endDate}")
            listOfAllTransactionsForSpecificAccountType = FilterExcel(dataFromSession, accountTypes)
    else:
        form.fields['accountType'].initial = initialAccountTypes
        form.fields['startDate'].initial = initialStartDate
        form.fields['endDate'].initial = initialEndDate
        listOfAllTransactionsForSpecificAccountType = FilterExcel(dataFromSession, initialAccountTypes)

    walletShares = GetCalculatedCurrentWallet(listOfAllTransactionsForSpecificAccountType)
    return render(request, 'wallet/dashboard.html', {"listOfAllTransactionsForSpecificAccountType": listOfAllTransactionsForSpecificAccountType, 'form': form, 'walletShares': walletShares})
