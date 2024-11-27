from django.contrib import admin
from django.contrib.auth.models import Group
from rbac.models import File


admin.site.register(File)
admin.site.unregister(Group)