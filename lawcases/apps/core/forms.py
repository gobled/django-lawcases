# -*- coding: utf-8 -*-
from django import forms
from lawcases.apps.core.models import File, Case, Entry, Payment, Client, KeyDate
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class KeydateForm(forms.ModelForm):
    class Meta:
        model = KeyDate
        fields = ('date', 'description', 'completed', 'case', 'add_user', 'add_date')
        widgets = {
            'add_user': forms.widgets.HiddenInput(),
            'add_date': forms.widgets.HiddenInput(),
            'case': forms.widgets.HiddenInput(),
            'description': forms.widgets.Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('description', 'client', 'amount', 'case', 'add_user', 'add_date')
        widgets = {
            'add_user': forms.widgets.HiddenInput(),
            'add_date': forms.widgets.HiddenInput(),
            'case': forms.widgets.HiddenInput(),
            'description': forms.widgets.Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('description', 'entry_time', 'cost', 'state', 'case', 'add_user', 'add_date')
        labels = {
            'entry_time': _('Enter the time in minutes'),
        }
        widgets = {
            'add_user': forms.widgets.HiddenInput(),
            'add_date': forms.widgets.HiddenInput(),
            'description': forms.widgets.Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('case', 'name', 'docfile', 'add_user')
        widgets = {
            'add_user': forms.widgets.HiddenInput(),
            'add_date': forms.widgets.HiddenInput(),
            'case': forms.widgets.HiddenInput(),
        }


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ('upd_user', 'upd_date', 'number')
        labels = {
            'matter': _('Matter of the case'),
        }
        widgets = {
            'due_date': forms.widgets.TextInput(attrs={'class': 'imdate'}),
            'add_user': forms.widgets.HiddenInput(),
            'status': forms.widgets.HiddenInput(attrs={'value': 1}),
            'add_date': forms.widgets.HiddenInput(),
            'description': forms.widgets.Textarea(attrs={'rows': 2, 'cols': 60}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('upd_user', 'upd_date')
        labels = {
            'name': _('Name'),
            'middle': _('Middle'),
            'surname': _('Surname'),
            'phone_home': _('Home Phone Number'),
            'phone_work': _('Work Phone Number'),
            'phone_mobile': _('Mobile Phone Number'),
            'email': _('Email Address'),
            'city': _('Current City'),
            'state': _('State'),
            'country': _('Country'),
            'address': _('Address'),
            'unit': _('Unit'),
            'postal_code': _('Postal Code'),
            'birth_date': _('Birth Date'),
        }
        widgets = {
            'add_user': forms.widgets.HiddenInput(),
            'add_date': forms.widgets.HiddenInput(),
        }
