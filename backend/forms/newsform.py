from django import forms
import datetime
class NewsForm(forms.Form):
    news_start_date     = forms.DateField(required=False, input_formats=['%Y/%m/%d','%Y-%m-%d'])
    news_end_date       = forms.DateField(required=False, input_formats=['%Y/%m/%d','%Y-%m-%d'])
    company_name        = forms.CharField(required=False)