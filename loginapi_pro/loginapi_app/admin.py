from django.contrib import admin
from .models import AyushUser
from django.contrib.auth.admin import UserAdmin

class AyushAdmin(UserAdmin):
    list_display = ('id','email','name','tc','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials',{'fields':('email','password')}),
        ('Personal info',{'fields':('name','tc')}),
        ('Permissions',{'fields':('is_admin',)}),
    )

    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','name','tc','password1','password2'),
        }),

    )
    search_fields  = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(AyushUser,AyushAdmin)

# Register your models here.
