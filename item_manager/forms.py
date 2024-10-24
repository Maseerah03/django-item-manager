from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

class SearchForm(forms.Form):
    item_name = forms.CharField(required=False)
    item_code = forms.CharField(required=False)
    vendor_name = forms.CharField(required=False)
