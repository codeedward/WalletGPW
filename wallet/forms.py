from django import forms

accountTypes = (
('Normalny', 'Normalny'),
('IKE', 'IKE'),)

class CommonFilterForm(forms.Form):
    accountType = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                      choices=accountTypes, label='Selected account types:')
