from django import forms


class ResolutionSearchForm(forms.Form):
    number = forms.CharField(label="Resolution No.", required=False)
    title = forms.CharField(label="Title", required=False)
    date_approved = forms.DateField(
        label="Date Approved:", required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))
