from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Group)
class GroupInitializeAdmin(admin.ModelAdmin):
    list_display= ('group', 'agent', 'is_admin')
    
admin.site.register(GroupInitialize,GroupInitializeAdmin)