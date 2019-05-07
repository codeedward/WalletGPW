import openpyxl
from ..models import ExcelEntryIkeRow
import json
from django.core.serializers.json import DjangoJSONEncoder

def ReadExcelIke(excel_file):
    # you may put validations here to check extension or file size
    wb = openpyxl.load_workbook(excel_file)

    # getting a particular sheet by name out of many sheets
    worksheet = wb["Sheet2"]

    excel_data = list()
    for row in worksheet.iter_rows():
        row_data = ExcelEntryIkeRow(row)
        excel_data.append(row_data)
    return list(reversed(excel_data))

def GetExcelDataIkeFromSession(request):
    deserializedDataFromSession = []

    if('excelData' in request.session):
        excelDataFromSession = request.session['excelDataIke']
        for r in excelDataFromSession:
            rowSet = json.loads(r)
            newExcelObj = ExcelEntryIkeRow(rowSet)
            newDesObj = newExcelObj
            deserializedDataFromSession.append(newDesObj)

    return deserializedDataFromSession

def SaveExcelDataIkeToSession(request, excelData):
    serializedData = [json.dumps(r.__dict__, cls=DjangoJSONEncoder) for r in excelData]
    request.session['excelDataIke'] = serializedData

class mySerializer(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
