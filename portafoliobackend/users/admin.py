
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from portafoliobackend.users.models import Users, Profile

class CustomUserAdmin(UserAdmin):

    list_display = ('email','username','first_name','last_name','is_staff','country',)
    list_filter = ('is_staff','created','modified',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user',)
    search_fields = ('user__username','user__email','user__first_name','user__last_name',)

admin.site.register(Users, CustomUserAdmin)