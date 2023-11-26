from django.contrib import admin
from .models import User, Profile
from to_do.models import Todo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):

    list_display = ["id", "email", "name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


class ProfileAdmin(admin.ModelAdmin):
    # list_editable = ['verified']
    list_display = ['id','user', 'full_name' ,'verified']
    search_fields = ["user"]
    ordering = ["user", "id"]


class TodoAdmin(admin.ModelAdmin):
    # list_editable = ['verified']
    list_display = ['id','user', 'title', 'date','completed']
    search_fields = ["user"]
    ordering = ["user", "id"]


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Todo, TodoAdmin)
