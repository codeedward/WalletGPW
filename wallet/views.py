from django.shortcuts import render
from .models import ExcelEntryRow
from .utils.excel_utils import FilterExcel, ReadExcel

def Dashboard(request):
    myData = { 'dataTest': 'its just test'}
    if "GET" == request.method:
        return render(request, 'wallet/dashboard.html', {})
    else:
        excel_data = ReadExcel(request.FILES["excel_file"])
        modelData = FilterExcel(excel_data, 'Normalny')
        return render(request, 'wallet/dashboard.html', {"excel_data": modelData})
    #return render(request, 'wallet/dashboard.html', myData)

