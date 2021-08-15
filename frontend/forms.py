from django import forms
from django.forms import ModelForm, widgets
from django.forms import fields
from warehouse.models import *

class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('pretty.css',)
        }
        js = ('animations.js', 'actions.js')

class CheckinForm(ModelForm):
    class Meta:
        model = Checkin
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Category Name'}),
            'code': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Category Code'}),
           
            }

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Name'}),
            'phone': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Phone'}),           
            }


class TransferForm(ModelForm):
    # date = forms.DateField()
    # to_warehouse = forms.ChoiceField()
    # reference = forms.CharField()    
    class Meta:
        model = Transfer
        fields = '__all__'
        widgets = {
            'from_warehouse':forms.Select(),
            'date':CalendarWidget(),
        }

class ItemForm(ModelForm):
    # date = forms.DateField()
    # to_warehouse = forms.ChoiceField()
    # reference = forms.CharField()    
   class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Name'}),
            'code': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Code'}),   
            'rack_location': forms.TextInput(attrs={
                'class':'form_input',
                'placeholder': 'Code'}),
            'SKU': forms.TextInput(attrs={
                'class':'form_input',
                'placeholder': 'SKU'}),
            'details': forms.Textarea(attrs={
                'class':'form_input',
                'placeholder': ''}),
            },        
            
           

class WarehouseForm(ModelForm):
    # date = forms.DateField()
    # to_warehouse = forms.ChoiceField()
    # reference = forms.CharField()    
    class Meta:
        model = Warehouse
        fields = '__all__'
        # widgets = {
        #     'name': forms.TextInput(attrs={'class':'ui input'}),
        #     'category': forms.TextInput(attrs={'class':'ui dropdown'}),
        # }
    