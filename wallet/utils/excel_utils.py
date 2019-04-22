import openpyxl
from ..models import ExcelEntryRow
import json
from django.core.serializers.json import DjangoJSONEncoder

def ReadExcel(excel_file):
    # you may put validations here to check extension or file size
    wb = openpyxl.load_workbook(excel_file)

    # getting a particular sheet by name out of many sheets
    worksheet = wb["Sheet1"]
    #print(worksheet)

    excel_data = list()
    # iterating over the rows and
    # getting value from each cell in row
    for row in worksheet.iter_rows():
        row_data = ExcelEntryRow(row)
        #print(row_data.date)
        #for cell in row:
            #row_data.append(str(cell.value))
        excel_data.append(row_data)
    return excel_data

def FilterExcel(listOfExcelRows, accountType):
    return filter(lambda x: filterExcel(x, accountType), listOfExcelRows)

def GetExcelDataFromSession(request):
    deserializedDataFromSession = []

    if('excelData' in request.session):
        excelDataFromSession = request.session['excelData']
        for r in excelDataFromSession:
            rowSet = json.loads(r)
            newExcelObj = ExcelEntryRow(rowSet)
            newDesObj = newExcelObj
            deserializedDataFromSession.append(newDesObj)

    return deserializedDataFromSession

def SaveExcelDataToSession(request, excelData):
    serializedData = [json.dumps(r.__dict__, cls=DjangoJSONEncoder) for r in excelData]
    request.session['excelData'] = serializedData

def filterExcel(excelEntryRow, accountType):
    if(excelEntryRow.accountType != accountType and accountType != ''):
        return False
    return True

class mySerializer(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
