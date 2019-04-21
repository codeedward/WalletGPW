from django.shortcuts import render
from .models import ExcelEntryRow
from .utils.excel_utils import FilterExcel, ReadExcel
import json
from django.core.serializers.json import DjangoJSONEncoder

def Dashboard(request):

    if "GET" == request.method:
        #request.session['dataTest'] = 'someSessionData'

        if('excelData' in request.session):

            excelDataFromSession = request.session['excelData']

            deserializedDataFromSession = []
            for r in excelDataFromSession:
                #print(type(r))
                rowSet = json.loads(r)
                newExcelObj = ExcelEntryRow(rowSet)
                #newExcelObj.name = rowSet['name']
                newDesObj = newExcelObj #json.loads(r, ExcelEntryRow)

                deserializedDataFromSession.append(newDesObj)
            #serializers.deserialize("xml", , cls=HandleMyClass)
            #print("Zdeserializowane dane:")
            #print(deserializedDataFromSession)
            modelData = FilterExcel(deserializedDataFromSession, 'Normalny')
            return render(request, 'wallet/dashboard.html', {"excel_data": modelData})

        return render(request, 'wallet/dashboard.html', {})
    else:
        #print("Session value is here:"+request.session['dataTest'])
        excel_data = ReadExcel(request.FILES["excel_file"])
        #print(type(excel_data))
        #excelRow = excel_data[0]
        serializedData = [json.dumps(r.__dict__, cls=DjangoJSONEncoder) for r in excel_data]
        #print(serializedData)
        #serializedData = [json.dumps(r, cls=mySerializer)  for r in excel_data]
        request.session['excelData'] = serializedData
        modelData = FilterExcel(excel_data, 'Normalny')
        return render(request, 'wallet/dashboard.html', {"excel_data": modelData})
    #return render(request, 'wallet/dashboard.html', myData)


'''class HandleMyClass(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ExcelEntryRow):
            return obj.__dict__
        return simplejson.JSONEncoder.default(self, obj)'''
class mySerializer(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
