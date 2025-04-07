from django.contrib import admin
from .models import UserActivityLog
from django.contrib.auth.models import User, Group


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'jalali_timestamp', 'timestamp')
    search_fields = ('user__username', 'action')
    list_filter = ('timestamp',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_group_members')
    search_fields = ('name',)

    def get_group_members(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])
    get_group_members.short_description = "اعضای گروه"

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
