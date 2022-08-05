from django import forms
from models import AdvUser


class ChangeInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='email')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
