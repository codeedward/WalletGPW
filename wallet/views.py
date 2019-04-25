from django.shortcuts import render
from .models import ExcelEntryRow
from .forms import CommonFilterForm
from .utils.excel_utils import FilterExcel, ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession
from .services.calculateService import GetCalculatedCurrentWallet

initialAccountTypes = ['Normalny', 'IKE']

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
    modelData = []
    dataFromSession = GetExcelDataFromSession(request)

    if request.method=='POST':
        form = CommonFilterForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            accountTypes = cleanedData.get('accountType')
            print(accountTypes)
            modelData = FilterExcel(dataFromSession, accountTypes)
    else:
        form.fields['accountType'].initial = initialAccountTypes
        modelData = FilterExcel(dataFromSession, initialAccountTypes)

    walletShares = GetCalculatedCurrentWallet(modelData)

    return render(request, 'wallet/dashboard.html', {"excel_data": modelData, 'form': form, 'walletShares': walletShares})
