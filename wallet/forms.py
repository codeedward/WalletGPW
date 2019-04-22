from django import forms
class CommonFilterForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    normal = forms.CharField(max_length=20)
    #All my attributes here
