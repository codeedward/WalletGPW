from django.shortcuts import render
from .models import ExcelEntryRow
from .forms import CommonFilterForm
from .utils.excel_utils import FilterExcel, ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession


def LoadData(request):

    if "GET" == request.method:
        print("HERE is GET")
        dataFromSession = GetExcelDataFromSession(request)
        modelData = FilterExcel(dataFromSession, ['Normalny', 'IKE'])
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})
    else:
        print("HERE is POST")
        excelData = ReadExcel(request.FILES["excel_file"])
        SaveExcelDataToSession(request, excelData)
        modelData = FilterExcel(excelData, ['Normalny', 'IKE'])
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
        initialAccountTypes = ['Normalny', 'IKE']
        form.fields['accountType'].initial = initialAccountTypes
        modelData = FilterExcel(dataFromSession, initialAccountTypes)

    walletShares = {}
    for transaction in modelData:
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

    return render(request, 'wallet/dashboard.html', {"excel_data": modelData, 'form': form, 'walletShares': walletShares})
