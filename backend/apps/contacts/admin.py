from django.contrib import admin
from .models import Public_Contact

@admin.register(Public_Contact)
class PublicContactAdmin(admin.ModelAdmin):
    
    list_display = (
        'id', 'first_name', 'last_name', 'organization', 'phone_number_1', 'mobile_number_1', 'category', 'active'
    )
    list_display_links = ('id', 'organization')

    search_fields = (
        'first_name', 'last_name', 'organization', 'phone_number_1', 'phone_number_2', 'phone_number_3', 'phone_number_4', 'phone_number_5', 'phone_number_6',
        'mobile_number_1', 'mobile_number_2', 'mobile_number_3', 'mobile_number_4', 'category',
        'sex', 'customer_id'
    )

    list_filter = (
        'active', 'category', 'created_at', 'sex', 'business_type', 'owner'
    )

    ordering = ('-created_at',)

    list_per_page = 20

    readonly_fields = ('created_at', 'modified_at', 'owner', 'latest_editor')

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('first_name', 'last_name', 'organization', 'category_id', 'category', 'business_type', 'sex')
        }),
        ('اطلاعات تماس', {
            'fields': (
                'phone_number_1', 'phone_number_1_organizational_position', 'phone_number_1_name', 'phone_number_1_ex', 'phone_number_1_note', 
                'phone_number_2', 'phone_number_2_organizational_position', 'phone_number_2_name', 'phone_number_2_ex', 'phone_number_2_note', 
                'phone_number_3', 'phone_number_3_organizational_position', 'phone_number_3_name', 'phone_number_3_ex', 'phone_number_3_note', 
                'phone_number_4', 'phone_number_4_organizational_position', 'phone_number_4_name', 'phone_number_4_ex', 'phone_number_4_note', 
                'phone_number_5', 'phone_number_5_organizational_position', 'phone_number_5_name', 'phone_number_5_ex', 'phone_number_5_note', 
                'phone_number_6', 'phone_number_6_organizational_position', 'phone_number_6_name', 'phone_number_6_ex', 'phone_number_6_note', 
                'fax',
                'mobile_number_1', 'mobile_number_1_name', 'mobile_number_1_note', 'mobile_number_1_email',
                'mobile_number_2', 'mobile_number_2_name', 'mobile_number_2_note', 'mobile_number_2_email',
                'mobile_number_3', 'mobile_number_3_name', 'mobile_number_3_note', 'mobile_number_3_email',
                'mobile_number_4', 'mobile_number_4_name', 'mobile_number_4_note', 'mobile_number_4_email'
            )
        }),
        ('آدرس و موقعیت', {
            'fields': (
                'address_1', 'postal_code_1', 'address_2', 'postal_code_2', 
                'address_3', 'postal_code_3'
            )
        }),
        ('وضعیت', {
            'fields': ('description', 'customer_id', 'color', 'note', 'created_at',
                       'modified_at', 'owner', 'latest_editor',  'latest_editor_log', 
                       'deleted_data', 'active')
        }),
    )
