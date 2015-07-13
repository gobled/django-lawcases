from django.contrib import admin
from lawcases.apps.core.models import Case
from lawcases.apps.core.models import Matter
from lawcases.apps.core.models import Client
from lawcases.apps.core.models import File
from lawcases.apps.core.models import CaseState, KeyDate
from lawcases.apps.core.models import Entry, EntryState, Payment

# Register your models here.

admin.site.register(Client)
admin.site.register(Case)
admin.site.register(Matter)
admin.site.register(File)
admin.site.register(CaseState)
admin.site.register(Entry)
admin.site.register(EntryState)
admin.site.register(Payment)
admin.site.register(KeyDate)