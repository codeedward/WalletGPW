from django import forms
from django.forms.widgets import SelectDateWidget
import datetime

accountTypes = (
('Normalny', 'Normalny'),
('IKE', 'IKE'),)

class CommonFilterForm(forms.Form):
    accountType = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=accountTypes, label='Selected account types:')
    startDate = forms.DateField(widget=SelectDateWidget(years=range(2018, datetime.date.today().year+1)), label='Start Date:')
    endDate = forms.DateField(widget=SelectDateWidget(years=range(2018, datetime.date.today().year+1)), label='End Date:')
