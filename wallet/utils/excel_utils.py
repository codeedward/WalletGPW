import openpyxl
from ..models import ExcelEntryRow
import json
from django.core.serializers.json import DjangoJSONEncoder

def ReadExcel(excel_file):
    # you may put validations here to check extension or file size
    wb = openpyxl.load_workbook(excel_file)

    # getting a particular sheet by name out of many sheets
    worksheet = wb["Sheet1"]

    excel_data = list()
    for row in worksheet.iter_rows():
        row_data = ExcelEntryRow(row)
        excel_data.append(row_data)
    return list(reversed(excel_data))

def FilterExcel(listOfExcelRows, accountTypes):
    return list(filter(lambda x: filterExcel(x, accountTypes), listOfExcelRows))

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

def filterExcel(excelEntryRow, accountTypes):
    if(excelEntryRow.accountType in accountTypes):
        return True
    return False

class mySerializer(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
