from django.db import models
from django.contrib.auth.models import User
import jdatetime

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    jalali_timestamp = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        self.jalali_timestamp = jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        super().save(*args, **kwargs)

    def __str__(self):
        username = self.user.username if self.user else "Deleted User"
        return f'{username} - {self.action} - {self.jalali_timestamp}'
