from django import forms
from sales.models import Sale
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"