from django.shortcuts import render
from .models import ExcelEntryRow
from .forms import CommonFilterForm
from .utils.excel_utils import FilterExcel, ReadExcel, GetExcelDataFromSession, SaveExcelDataToSession


def LoadData(request):

    if "GET" == request.method:
        dataFromSession = GetExcelDataFromSession(request)
        modelData = FilterExcel(dataFromSession, 'Normalny')
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})
    else:
        excelData = ReadExcel(request.FILES["excel_file"])
        SaveExcelDataToSession(request, excelData)
        modelData = FilterExcel(excelData, 'Normalny')
        return render(request, 'wallet/loadData.html', {"excel_data": modelData})


def Dashboard(request):
    form = CommonFilterForm()
    modelData = []
    form.accountType = ['ike']
    if request.method=='POST':
        form = CommonFilterForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            accountType = cleanedData.get('accountType')
            print(accountType)
    else:
        dataFromSession = GetExcelDataFromSession(request)
        modelData = FilterExcel(dataFromSession, 'Normalny')

    return render(request, 'wallet/dashboard.html', {"excel_data": modelData, 'form': form})
