from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    middle = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    phone_home = models.CharField(max_length=100)
    phone_work = models.CharField(max_length=100)
    phone_mobile = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    birth_date = models.DateField('client birth date')
    email = models.CharField(max_length=100)

    add_date = models.DateTimeField('client add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='client added user')
    upd_date = models.DateTimeField('client upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, null=True, blank=True, related_name='client updated user')

    def __str__(self):
        return '%s %s' % (self.surname, self.name)


class Matter(models.Model):
    title = models.CharField(max_length=255)
    add_date = models.DateTimeField('add date')
    add_user = models.ForeignKey(User, related_name='matter added user')
    upd_date = models.DateTimeField('upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, null=True, blank=True, related_name='matter updated user')

    def __str__(self):
        return self.title


class EntryState(models.Model):
    title = models.CharField(max_length=100)
    add_date = models.DateTimeField('entrystate add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='entrystate added user')
    upd_date = models.DateTimeField('entrystate upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, blank=True, null=True, related_name='entrystate updated user')

    def __str__(self):
        return self.title


class CaseState(models.Model):
    title = models.CharField(max_length=100)
    add_date = models.DateTimeField('casestate add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='casestate added user')
    upd_date = models.DateTimeField('casestate upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, blank=True, null=True, related_name='casestate updated user')

    def __str__(self):
        return self.title


class Case(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField('due date')
    number = models.TextField(null=True, blank=True)
    matter = models.ForeignKey(Matter)
    client = models.ForeignKey(Client)
    description = models.TextField(max_length=500)
    status = models.ForeignKey(CaseState, related_name='case status')
    add_date = models.DateTimeField('case add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='case added user')
    upd_date = models.DateTimeField('case upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, blank=True, null=True, related_name='case updated user')

    def __str__(self):
        return self.title


class KeyDate(models.Model):
    date = models.DateField()
    case = models.ForeignKey(Case)
    description = models.TextField(max_length=500)
    completed = models.BooleanField()
    add_date = models.DateTimeField('keydate add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='keydate added user')
    upd_date = models.DateTimeField('keydate upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, blank=True, null=True, related_name='keydate updated user')

    def __str__(self):
        return self.date


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    client = models.ForeignKey(Client, related_name='payment client')
    case = models.ForeignKey(Case)
    add_date = models.DateTimeField('payment add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='payment added user')
    upd_date = models.DateTimeField('payment upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, blank=True, null=True, related_name='payment updated user')

    def __str__(self):
        return self.description


class Entry(models.Model):
    description = models.TextField(max_length=500)
    entry_time = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    case = models.ForeignKey(Case)
    state = models.ForeignKey(EntryState)
    add_date = models.DateTimeField('entry add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='entry added user')
    upd_date = models.DateTimeField('entry upd date', null=True, blank=True)
    upd_user = models.ForeignKey(User, blank=True, null=True, related_name='entry updated user')

    def __str__(self):
        return self.description


def test_name(a, b):
    return 'documents/%s/%s' % (a.case.number, b)


class File(models.Model):
    name = models.CharField(max_length=100)
    case = models.ForeignKey(Case)
    add_date = models.DateTimeField('add date', default=datetime.now, blank=True)
    add_user = models.ForeignKey(User, related_name='file added user', )
    upd_date = models.DateTimeField('upd date', null=True, blank=True, )
    upd_user = models.ForeignKey(User, null=True, blank=True, related_name='file updated user')
    docfile = models.FileField(upload_to=test_name)

    def __str__(self):
        return self.docfile     
