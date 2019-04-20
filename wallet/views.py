from django.shortcuts import render
import openpyxl
from .models import ExcelEntryRow
from .utils.excel_utils import FilterExcel

def Dashboard(request):
    myData = { 'dataTest': 'its just test'}
    if "GET" == request.method:
        return render(request, 'wallet/dashboard.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        # you may put validations here to check extension or file size
        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = ExcelEntryRow(row)
            print(row_data.date)
            #for cell in row:
                #row_data.append(str(cell.value))
            excel_data.append(row_data)

        modelData = FilterExcel(excel_data, 'Normalny')
        return render(request, 'wallet/dashboard.html', {"excel_data": modelData})
    #return render(request, 'wallet/dashboard.html', myData)

