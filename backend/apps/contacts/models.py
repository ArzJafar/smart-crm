from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Public_Contact(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True) 
    sex = models.CharField(max_length=10, choices=[('M', 'مرد'), ('F', 'زن')], blank=True, null=True)

    phone_number_1 = models.CharField(max_length=20, blank=True, null=True)
    phone_number_1_organizational_position = models.CharField(max_length=100, blank=True, null=True)
    phone_number_1_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_1_ex = models.CharField(max_length=10, blank=True, null=True)
    phone_number_1_note = models.TextField(blank=True, null=True)
    phone_number_2 = models.CharField(max_length=20, blank=True, null=True)
    phone_number_2_organizational_position = models.CharField(max_length=100, blank=True, null=True)
    phone_number_2_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_2_ex = models.CharField(max_length=10, blank=True, null=True)
    phone_number_2_note = models.TextField(blank=True, null=True)
    phone_number_3 = models.CharField(max_length=20, blank=True, null=True)
    phone_number_3_organizational_position = models.CharField(max_length=100, blank=True, null=True)
    phone_number_3_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_3_ex = models.CharField(max_length=10, blank=True, null=True)
    phone_number_3_note = models.TextField(blank=True, null=True)
    phone_number_4 = models.CharField(max_length=20, blank=True, null=True)
    phone_number_4_organizational_position = models.CharField(max_length=100, blank=True, null=True)
    phone_number_4_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_4_ex = models.CharField(max_length=10, blank=True, null=True)
    phone_number_4_note = models.TextField(blank=True, null=True)
    phone_number_5 = models.CharField(max_length=20, blank=True, null=True)
    phone_number_5_organizational_position = models.CharField(max_length=100, blank=True, null=True)
    phone_number_5_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_5_ex = models.CharField(max_length=10, blank=True, null=True)
    phone_number_5_note = models.TextField(blank=True, null=True)
    phone_number_6 = models.CharField(max_length=20, blank=True, null=True)
    phone_number_6_organizational_position = models.CharField(max_length=100, blank=True, null=True)
    phone_number_6_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_6_ex = models.CharField(max_length=10, blank=True, null=True)
    phone_number_6_note = models.TextField(blank=True, null=True)

    fax = models.CharField(max_length=20, blank=True, null=True)

    mobile_number_1 = models.CharField(max_length=20, blank=True, null=True)
    mobile_number_1_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number_1_note = models.TextField(blank=True, null=True)
    mobile_number_1_email = models.EmailField(null=True, blank=True)
    mobile_number_2 = models.CharField(max_length=20, blank=True, null=True)
    mobile_number_2_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number_2_note = models.TextField(blank=True, null=True)
    mobile_number_2_email = models.EmailField(null=True, blank=True)
    mobile_number_3 = models.CharField(max_length=20, blank=True, null=True)
    mobile_number_3_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number_3_note = models.TextField(blank=True, null=True)
    mobile_number_3_email = models.EmailField(null=True, blank=True)
    mobile_number_4 = models.CharField(max_length=20, blank=True, null=True)
    mobile_number_4_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number_4_note = models.TextField(blank=True, null=True)
    mobile_number_4_email = models.EmailField(null=True, blank=True)


    address_1 = models.TextField(blank=True, null=True)
    postal_code_1 = models.CharField(max_length=20, blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    postal_code_2 = models.CharField(max_length=20, blank=True, null=True)
    address_3 = models.TextField(blank=True, null=True)
    postal_code_3 = models.CharField(max_length=20, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    latest_editor = models.CharField(max_length=255, blank=True, null=True)
    latest_editor_log = models.TextField(blank=True, null=True)
    deleted_data = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        elif self.organization:
            return self.organization
        else:
            return "Unknown"
        
