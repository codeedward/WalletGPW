from django import forms
from django.forms.widgets import SelectDateWidget

accountTypes = (
('Normalny', 'Normalny'),
('IKE', 'IKE'),)

class CommonFilterForm(forms.Form):
    accountType = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=accountTypes, label='Selected account types:')
    startDate = forms.DateField(widget=SelectDateWidget(), label='Start Date:')
    endDate = forms.DateField(widget=SelectDateWidget(), label='End Date:')
