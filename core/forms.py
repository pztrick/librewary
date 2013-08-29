from django import forms
from core.models import *


class BrewerForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Brewer
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        # Override #1- We need to hash the password before saving
        brewer = super(BrewerForm, self).save(commit=False)
        brewer.set_password(self.cleaned_data["password"])
        if commit:
            brewer.save()
        return brewer


class EquipmentOfferForm(forms.ModelForm):

    class Meta:
        model = EquipmentOffer
        exclude = ['owner']


class AcceptEquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        exclude = ['contributor']
        #widgets = {
        #    'description': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        #}


class BrewerEquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        exclude = ['contributor', 'contributed', 'p2p_is_checked_out']
        #widgets = {
        #    'description': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        #}
