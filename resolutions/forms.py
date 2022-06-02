from django import forms


class ResolutionSearchForm(forms.Form):
    number = forms.CharField(label="Resolution No.", required=False)
    keyword = forms.CharField(label="Keyword", required=False)
    date_approved = forms.DateField(
        label="Date Approved:", required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))
