from django.shortcuts import render

def Dashboard(request):
    myData = { 'dataTest': 'its just test'}
    return render(request, 'wallet/dashboard.html', myData)

