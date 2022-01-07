from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import admin_thumbnails
from .models import Account, UserProfile
# Register your models here.


class AccountAdmin(UserAdmin):

    list_display = ('username', 'first_name', 'last_name',
                    'email', 'last_login', 'date_joined', 'is_active')
    list_display_link = ('username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ('last_login', 'is_active')
    fieldsets = ()


@admin_thumbnails.thumbnail('profilePicture')
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'user', 'city', 'state', 'country']
    list_display_link = ('image_tag', 'user')
    list_filter = ['user', 'city', 'state', 'country']
    search_fields = ['user', 'city', 'state', 'country']


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
