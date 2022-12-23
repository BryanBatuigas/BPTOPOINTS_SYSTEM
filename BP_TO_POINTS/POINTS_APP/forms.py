from re import A
from django.db.models import fields
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import *
from django.core.mail import send_mail


class Userreg(UserCreationForm):
    class Meta:
        model = Useraccount
        fields = ['username', 'email', 'first_name', 'last_name', 'Usertype', 'password1', 'password2']
        widgets = {
            
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'Usertype' : forms.Select(attrs={'class':'form-control'}),
            'password1' : forms.PasswordInput(attrs={'class':'form-control'}),
            'password2' : forms.PasswordInput(attrs={'class':'form-control'}),
            
        }

        # or fields = __all__'

class AddRewardsSettings(ModelForm):
    class Meta:
        model = Rewards_Settings
        fields = '__all__'
        widgets = {
            'Product_Name' : forms.TextInput(attrs={'class':'form-control'}),
            'Stocks' : forms.TextInput(attrs={'onkeypress':'return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57'}),
            'Color' : forms.TextInput(attrs={'class':'form-control'}),
            'Value_Points' : forms.TextInput(attrs={'onkeypress':'return isNumberKey(this, event)'}),
        }

class PaperForm(ModelForm): 
    class Meta:
        model = PaperModel
        fields = '__all__'

class PaperPointsForm(ModelForm):
    class Meta:
        model = PaperPointsEquivalent
        fields = '__all__'
        widgets = {
            'paper_weight' : forms.NumberInput(attrs={'class':'form-control', 'value':'0.00'}),
            'paper_points' : forms.NumberInput(attrs={'class':'form-control', 'value':'0.00'}),
        }

class BottlePointsForm(ModelForm):
    class Meta:
        model = BottlePointsEquivalent
        fields = '__all__'
        widgets = {
            'bottle_count' : forms.NumberInput(attrs={'class':'form-control', 'value':'0.00'}),
            'bottle_points' : forms.NumberInput(attrs={'class':'form-control', 'value':'0.00'}),
        }