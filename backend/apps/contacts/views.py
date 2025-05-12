from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import Public_ContactForm
from .models import Public_Contact
from django.contrib.auth.decorators import login_required
from django.db import transaction
import csv
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
import jdatetime
from apps.web.models import UserActivityLog
from rest_framework.viewsets import ModelViewSet
from .models import Public_Contact
from .serializers import ContactSerializer

jdatetime.set_locale(jdatetime.FA_LOCALE)


class ContactViewSet(ModelViewSet):
    queryset = Public_Contact.objects.all()
    serializer_class = ContactSerializer


def is_admin(user):
    return user.is_staff


# For add contacts, we have two different forms for personal and public contacts
def process_contact(request, contact_form_class, template_name, url):
    if request.method == 'POST':    
        contact_form = contact_form_class(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.save()

            messages.success(request, "مخاطب با موفقیت اضافه شد!")
            return redirect(f'contacts:{url}')
        else:
            messages.error(request, "خطا در فرم. لطفاً مجدداً تلاش کنید.")
    else:
        contact_form = contact_form_class()

    return render(request, template_name, {
        'contact_form': contact_form,
    })



def process_to_home(request, contact_form_class, template_name, url):
    if request.method == 'POST':
        contact_form = contact_form_class(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.owner = request.user
            contact.latest_editor = f"{request.user}"
            contact.latest_editor_log = f'{request.user} added this contact.'
            contact.modified_at = jdatetime.datetime.now()
            contact.save()
            UserActivityLog.objects.create(user=request.user, action=f"Aded contact {contact.last_name or contact.first_name or contact.organization} ({contact.id})  (new contact)")

            messages.success(request, "مخاطب با موفقیت اضافه شد!")
            return redirect(f'{url}')
        else:
            messages.error(request, "خطا در فرم. لطفاً مجدداً تلاش کنید.")
    else:
        contact_form = contact_form_class()

    return render(request, template_name, {
        'contact_form': contact_form,
    })


# Add public contact
@login_required
@transaction.atomic
def add_public_contact(request):
    return process_to_home(
        request,
        contact_form_class=Public_ContactForm,
        template_name='contacts/Public/add_public_contact.html',
        url='main'
    )


@user_passes_test(is_admin)
@login_required
def public_contacts_list(request):
    contacts = Public_Contact.objects.filter(active=True).order_by('-created_at')
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages
    page_range = range(max(current_page - 2, 1), min(current_page + 3, total_pages + 1))

    return render(request, 'contacts/Public/public_contacts_list.html', {
        'contacts': page_obj,
        'page_obj': page_obj,
        'page_range': page_range,
        'total_pages': total_pages,
        'is_staff': request.user.is_staff,
    })


# Delete public contact
@login_required
@user_passes_test(is_admin)
def delete_public_contact(request, pk):
    contact = get_object_or_404(Public_Contact, pk=pk)
    if request.method == 'POST':
        contact.active = False
        contact.latest_editor = f"{request.user}"
        contact.latest_editor_log = f'{request.user} deleted this contact.'
        contact.deleted_data = (contact.deleted_data or '') + f'{request.user} deleted this contact.\n'
        contact.modified_at = jdatetime.datetime.now()
        contact.save()
        UserActivityLog.objects.create(user=request.user, action=f"Deleted contact {contact.last_name or contact.first_name  or contact.organization} ({contact.id})  (deactive)")
        return redirect('contacts:public_contacts_list')
    return render(request, 'contacts/Public/delete_Public_contact.html', {'contact': contact})


@login_required
def search_public_contacts(request):
    try:
        query = request.GET.get('q', '')
        contacts = Public_Contact.objects.all()

        if query:
            contacts = contacts.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(organization__icontains=query) |
                Q(category__icontains=query) |
                Q(business_type__icontains=query) |
                Q(sex__icontains=query) |

                Q(phone_number_1__icontains=query) |
                Q(phone_number_1_name__icontains=query) |
                Q(phone_number_1_ex__icontains=query) |
                Q(phone_number_1_note__icontains=query) |
                Q(phone_number_1_organizational_position__icontains=query) |
                Q(phone_number_2__icontains=query) |
                Q(phone_number_2_name__icontains=query) |
                Q(phone_number_2_ex__icontains=query) |
                Q(phone_number_2_note__icontains=query) |
                Q(phone_number_2_organizational_position__icontains=query) |
                Q(phone_number_3__icontains=query) |
                Q(phone_number_3_name__icontains=query) |
                Q(phone_number_3_ex__icontains=query) |
                Q(phone_number_3_note__icontains=query) |
                Q(phone_number_3_organizational_position__icontains=query) |
                Q(phone_number_4__icontains=query) |
                Q(phone_number_4_name__icontains=query) |
                Q(phone_number_4_ex__icontains=query) |
                Q(phone_number_4_note__icontains=query) |
                Q(phone_number_4_organizational_position__icontains=query) |
                Q(phone_number_5__icontains=query) |
                Q(phone_number_5_name__icontains=query) |
                Q(phone_number_5_ex__icontains=query) |
                Q(phone_number_5_note__icontains=query) |
                Q(phone_number_5_organizational_position__icontains=query) |
                Q(phone_number_6__icontains=query) |
                Q(phone_number_6_name__icontains=query) |
                Q(phone_number_6_ex__icontains=query) |
                Q(phone_number_6_note__icontains=query) |
                Q(phone_number_6_organizational_position__icontains=query) |

                Q(fax__icontains=query) |

                Q(mobile_number_1__icontains=query) |
                Q(mobile_number_1_name__icontains=query) |
                Q(mobile_number_1_note__icontains=query) |
                Q(mobile_number_1_email__icontains=query) |
                Q(mobile_number_2__icontains=query) |
                Q(mobile_number_2_name__icontains=query) |
                Q(mobile_number_2_note__icontains=query) |
                Q(mobile_number_2_email__icontains=query) |
                Q(mobile_number_3__icontains=query) |
                Q(mobile_number_3_name__icontains=query) |
                Q(mobile_number_3_note__icontains=query) |
                Q(mobile_number_3_email__icontains=query) |
                Q(mobile_number_4__icontains=query) |
                Q(mobile_number_4_name__icontains=query) |
                Q(mobile_number_4_note__icontains=query) |
                Q(mobile_number_4_email__icontains=query) |

                Q(address_1__icontains=query) |
                Q(postal_code_1__icontains=query) |
                Q(address_2__icontains=query) |
                Q(postal_code_2__icontains=query) |
                Q(address_3__icontains=query) |
                Q(postal_code_3__icontains=query) |

                Q(description__icontains=query) |
                Q(customer_id__icontains=query) |
                Q(color__icontains=query) |

                Q(owner__icontains=query),
                active=True
            )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            paginator = Paginator(contacts, 10)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            data = [
                {
                    "id": contact.id,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "organization": contact.organization,
                    "phone_number": contact.phone_number_1,
                    "category": contact.category,
                    "is_staff": request.user.is_staff,
                }
                for contact in page_obj.object_list
            ]
            return JsonResponse({
                'contacts': data,
                'is_staff': request.user.is_staff,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'total_pages': paginator.num_pages,
                'current_page': page_obj.number,
            })

        paginator = Paginator(contacts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'contacts/Public/public_contacts_list.html', {'page_obj': page_obj})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred.'}, status=500)


# Export contacts base function
@user_passes_test(is_admin)
def export_contacts_base(queryset, filename, extra_field_model, phone_number_model):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)

    base_fields = ['Name', 'Phone', 'Address', 'Email']

    extra_fields = extra_field_model.objects.filter(contact__in=queryset).values_list('field_name', flat=True).distinct()

    extra_phone_fields = phone_number_model.objects.filter(contact__in=queryset).values_list('label', flat=True).distinct()

    writer.writerow(base_fields + list(extra_fields) + [f"Phone ({label})" for label in extra_phone_fields])

    for contact in queryset:
        base_data = [contact.name, contact.phone, contact.address, contact.email]

        extra_data = [
            extra_field_model.objects.filter(contact=contact, field_name=field).first().field_value
            if extra_field_model.objects.filter(contact=contact, field_name=field).exists() else ''
            for field in extra_fields
        ]

        phone_data = [
            phone_number_model.objects.filter(contact=contact, label=label).first().number
            if phone_number_model.objects.filter(contact=contact, label=label).exists() else ''
            for label in extra_phone_fields
        ]

        writer.writerow(base_data + extra_data + phone_data)

    return response


# Export public contacts
@login_required
@user_passes_test(is_admin)
def public_export_contacts_csv(request):
    contacts = Public_Contact.objects.all()
    return export_contacts_base(
        queryset=contacts,
        filename="public_contacts",
    )

import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
# Import contacts base function
@user_passes_test(is_admin)
def import_contacts_base(request, contact_model):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            return render(request, 'contacts/Public/public_contacts_list.html', {
                'error': 'لطفا یک فایل CSV معتبر بارگذاری کنید.'
            })

        try:
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file)
            
            contacts_to_create = []
            
            for row in reader:
                contact_data = {
                    'first_name': row.get('first_name', '').strip(),
                    'last_name': row.get('last_name', '').strip(),
                    'organization': row.get('organization', '').strip(),
                    'category_id': row.get('category_id', '').strip(),
                    'category': row.get('category', '').strip(),
                    'business_type': row.get('business_type', '').strip(),
                    'sex': row.get('sex', '').strip(),

                    'phone_number_1': row.get('phone_number_1', '').strip(),
                    'phone_number_1_name': row.get('phone_number_1_name', '').strip(),
                    'phone_number_1_ex': row.get('phone_number_1_ex', '').strip(),
                    'phone_number_1_note': row.get('phone_number_1_note', '').strip(),
                    'phone_number_1_organizational_position': row.get('phone_number_1_organizational_position', '').strip(),
                    
                    'phone_number_2': row.get('phone_number_2', '').strip(),
                    'phone_number_2_name': row.get('phone_number_2_name', '').strip(),
                    'phone_number_2_ex': row.get('phone_number_2_ex', '').strip(),
                    'phone_number_2_note': row.get('phone_number_2_note', '').strip(),
                    'phone_number_2_organizational_position': row.get('phone_number_2_organizational_position', '').strip(),
                    
                    'phone_number_3': row.get('phone_number_3', '').strip(),
                    'phone_number_3_name': row.get('phone_number_3_name', '').strip(),
                    'phone_number_3_ex': row.get('phone_number_3_ex', '').strip(),
                    'phone_number_3_note': row.get('phone_number_3_note', '').strip(),
                    'phone_number_3_organizational_position': row.get('phone_number_3_organizational_position', '').strip(),
                    
                    'phone_number_4': row.get('phone_number_4', '').strip(),
                    'phone_number_4_name': row.get('phone_number_4_name', '').strip(),
                    'phone_number_4_ex': row.get('phone_number_4_ex', '').strip(),
                    'phone_number_4_note': row.get('phone_number_4_note', '').strip(),
                    'phone_number_4_organizational_position': row.get('phone_number_4_organizational_position', '').strip(),
                    
                    'phone_number_5': row.get('phone_number_5', '').strip(),
                    'phone_number_5_name': row.get('phone_number_5_name', '').strip(),
                    'phone_number_5_ex': row.get('phone_number_5_ex', '').strip(),
                    'phone_number_5_note': row.get('phone_number_5_note', '').strip(),
                    'phone_number_5_organizational_position': row.get('phone_number_5_organizational_position', '').strip(),
                    
                    'phone_number_6': row.get('phone_number_6', '').strip(),
                    'phone_number_6_name': row.get('phone_number_6_name', '').strip(),
                    'phone_number_6_ex': row.get('phone_number_6_ex', '').strip(),
                    'phone_number_6_note': row.get('phone_number_6_note', '').strip(),
                    'phone_number_6_organizational_position': row.get('phone_number_6_organizational_position', '').strip(),

                    'fax': row.get('fax', '').strip(),

                    'mobile_number_1': row.get('mobile_number_1', '').strip(),
                    'mobile_number_1_name': row.get('mobile_number_1_name', '').strip(),
                    'mobile_number_1_note': row.get('mobile_number_1_note', '').strip(),
                    'mobile_number_1_email': row.get('mobile_number_1_email', '').strip(),

                    'mobile_number_2': row.get('mobile_number_2', '').strip(),
                    'mobile_number_2_name': row.get('mobile_number_2_name', '').strip(),
                    'mobile_number_2_note': row.get('mobile_number_2_note', '').strip(),
                    'mobile_number_2_email': row.get('mobile_number_2_email', '').strip(),

                    'mobile_number_3': row.get('mobile_number_3', '').strip(),
                    'mobile_number_3_name': row.get('mobile_number_3_name', '').strip(),
                    'mobile_number_3_note': row.get('mobile_number_3_note', '').strip(),
                    'mobile_number_3_email': row.get('mobile_number_3_email', '').strip(),

                    'mobile_number_4': row.get('mobile_number_4', '').strip(),
                    'mobile_number_4_name': row.get('mobile_number_4_name', '').strip(),
                    'mobile_number_4_note': row.get('mobile_number_4_note', '').strip(),
                    'mobile_number_4_email': row.get('mobile_number_4_email', '').strip(),


                    'address_1': row.get('address_1', '').strip(),
                    'postal_code_1': row.get('postal_code_1', '').strip(),
                    'address_2': row.get('address_2', '').strip(),
                    'postal_code_2': row.get('postal_code_2', '').strip(),
                    'address_3': row.get('address_3', '').strip(),
                    'postal_code_3': row.get('postal_code_3', '').strip(),

                    'description': row.get('description', '').strip(),
                    'customer_id': row.get('customer_id', '').strip(),
                    'color': row.get('color', '').strip(),
                    'note': row.get('note', '').strip(),

                    'created_at': row.get('created_at', '').strip(),
                    'modified_at': row.get('modified_at', '').strip(),
                    'owner': request.user.username.strip(),
                    'latest_editor': row.get('latest_editor', '').strip(),
                    'latest_editor_log': row.get('latest_editor_log', '').strip(),
                    'deleted_data': row.get('deleted_data', '').strip(),
                }
                
                
                contact = contact_model(**contact_data)
                contacts_to_create.append(contact)
                
            contact_model.objects.bulk_create(contacts_to_create)
            
        except Exception as e:
            return render(request, 'contacts/Public/public_contacts_list.html', {
                'error': f'خطایی در پردازش فایل رخ داد: {str(e)}'
            })

        return redirect('contacts:public_contacts_list')
    
    return redirect('contacts:public_contacts_list')


# Import public contacts
@user_passes_test(is_admin)
@login_required
def public_import_contacts_csv(request):
    return import_contacts_base(
        request=request,
        contact_model=Public_Contact,
    )


# Public contact details
@login_required
def public_contact_details(request, pk):
    contact = get_object_or_404(Public_Contact, pk=pk)

    return render(request, 'contacts/Public/public_contact_details.html', {
        'contact': contact,
    })


@login_required
def search_contacts(request):
    query = request.GET.get('query', '').strip()
    parts = query.split()
    
    first_name_part = ''
    last_name_part = ''
    
    if len(parts) == 2:
        first_name_part = parts[0]
        last_name_part = parts[1]
    
    if query:
        contacts = Public_Contact.objects.filter(
            (Q(first_name__icontains=first_name_part) & Q(last_name__icontains=last_name_part))  |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(organization__icontains=query) |
            Q(category__icontains=query) |
            Q(business_type__icontains=query) |
            Q(sex__icontains=query) |
            Q(phone_number_1__icontains=query) |
            Q(phone_number_1_name__icontains=query) |
            Q(phone_number_1_ex__icontains=query) |
            Q(phone_number_1_note__icontains=query) |
            Q(phone_number_1_organizational_position__icontains=query) |
            Q(phone_number_2__icontains=query) |
            Q(phone_number_2_name__icontains=query) |
            Q(phone_number_2_ex__icontains=query) |
            Q(phone_number_2_note__icontains=query) |
            Q(phone_number_2_organizational_position__icontains=query) |
            Q(phone_number_3__icontains=query) |
            Q(phone_number_3_name__icontains=query) |
            Q(phone_number_3_ex__icontains=query) |
            Q(phone_number_3_note__icontains=query) |
            Q(phone_number_3_organizational_position__icontains=query) |
            Q(phone_number_4__icontains=query) |
            Q(phone_number_4_name__icontains=query) |
            Q(phone_number_4_ex__icontains=query) |
            Q(phone_number_4_note__icontains=query) |
            Q(phone_number_4_organizational_position__icontains=query) |
            Q(phone_number_5__icontains=query) |
            Q(phone_number_5_name__icontains=query) |
            Q(phone_number_5_ex__icontains=query) |
            Q(phone_number_5_note__icontains=query) |
            Q(phone_number_5_organizational_position__icontains=query) |
            Q(phone_number_6__icontains=query) |
            Q(phone_number_6_name__icontains=query) |
            Q(phone_number_6_ex__icontains=query) |
            Q(phone_number_6_note__icontains=query) |
            Q(phone_number_6_organizational_position__icontains=query) |

            Q(fax__icontains=query) |

            Q(mobile_number_1__icontains=query) |
            Q(mobile_number_1_name__icontains=query) |
            Q(mobile_number_1_note__icontains=query) |
            Q(mobile_number_1_email__icontains=query) |
            Q(mobile_number_2__icontains=query) |
            Q(mobile_number_2_name__icontains=query) |
            Q(mobile_number_2_note__icontains=query) |
            Q(mobile_number_2_email__icontains=query) |
            Q(mobile_number_3__icontains=query) |
            Q(mobile_number_3_name__icontains=query) |
            Q(mobile_number_3_note__icontains=query) |
            Q(mobile_number_3_email__icontains=query) |
            Q(mobile_number_4__icontains=query) |
            Q(mobile_number_4_name__icontains=query) |
            Q(mobile_number_4_note__icontains=query) |
            Q(mobile_number_4_email__icontains=query) |


            Q(address_1__icontains=query) |
            Q(postal_code_1__icontains=query) |
            Q(address_2__icontains=query) |
            Q(postal_code_2__icontains=query) |
            Q(address_3__icontains=query) |
            Q(postal_code_3__icontains=query) |

            Q(description__icontains=query) |
            Q(customer_id__icontains=query) |
            Q(color__icontains=query) |

            Q(owner__icontains=query),
            active=True
        )[:]

        results = [{
            'id': contact.id,
            'first_name': contact.first_name or "-",
            'last_name': contact.last_name or "-",
            'category': contact.category or "-",
            'mobile_number_1': contact.mobile_number_1 or contact.mobile_number_2 or contact.mobile_number_3 or contact.mobile_number_4 or "-",
            'phone_number_1': contact.phone_number_1 or contact.phone_number_2 or contact.phone_number_3 or contact.phone_number_4 or contact.phone_number_5 or contact.phone_number_6 or "-",
            'organization': contact.organization or "-"
        } for contact in contacts]
    else:
        results = []

    return JsonResponse(results, safe=False)


@login_required
def colleagues(request):
    return render(request, 'contacts/Local/main.html')
@login_required
def guide(request):
    return render(request, 'contacts/guide.html')


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Public_Contact, id=contact_id)
    return render(request, "contacts/Public/edit_public_contact.html", {"contact": contact})
@staff_member_required
def update_contact(request, contact_id):
    contact = get_object_or_404(Public_Contact, id=contact_id)
    if request.method == "POST":
        old_values = {
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'organization': contact.organization,
            'category': contact.category,
            'business_type': contact.business_type,
            'sex': contact.sex,
            'phone_number_1': contact.phone_number_1,
            'phone_number_1_name': contact.phone_number_1_name,
            'phone_number_1_organizational_position': contact.phone_number_1_organizational_position,
            'phone_number_1_ex': contact.phone_number_1_ex,
            'phone_number_1_note': contact.phone_number_1_note,
            'phone_number_2': contact.phone_number_2,
            'phone_number_2_name': contact.phone_number_2_name,
            'phone_number_2_organizational_position': contact.phone_number_2_organizational_position,
            'phone_number_2_ex': contact.phone_number_2_ex,
            'phone_number_2_note': contact.phone_number_2_note,
            'phone_number_3': contact.phone_number_3,
            'phone_number_3_name': contact.phone_number_3_name,
            'phone_number_3_organizational_position': contact.phone_number_3_organizational_position,
            'phone_number_3_ex': contact.phone_number_3_ex,
            'phone_number_3_note': contact.phone_number_3_note,
            'phone_number_4': contact.phone_number_4,
            'phone_number_4_name': contact.phone_number_4_name,
            'phone_number_4_organizational_position': contact.phone_number_4_organizational_position,
            'phone_number_4_ex': contact.phone_number_4_ex,
            'phone_number_4_note': contact.phone_number_4_note,
            'phone_number_5': contact.phone_number_5,
            'phone_number_5_name': contact.phone_number_5_name,
            'phone_number_5_organizational_position': contact.phone_number_5_organizational_position,
            'phone_number_5_ex': contact.phone_number_5_ex,
            'phone_number_5_note': contact.phone_number_5_note,
            'phone_number_6': contact.phone_number_6,
            'phone_number_6_name': contact.phone_number_6_name,
            'phone_number_6_organizational_position': contact.phone_number_6_organizational_position,
            'phone_number_6_ex': contact.phone_number_6_ex,
            'phone_number_6_note': contact.phone_number_6_note,
            'mobile_number_1': contact.mobile_number_1,
            'mobile_number_1_name': contact.mobile_number_1_name,
            'mobile_number_1_note': contact.mobile_number_1_note,
            'mobile_number_1_email': contact.mobile_number_1_email,
            'mobile_number_2': contact.mobile_number_2,
            'mobile_number_2_name': contact.mobile_number_2_name,
            'mobile_number_2_note': contact.mobile_number_2_note,
            'mobile_number_2_email': contact.mobile_number_2_email,
            'mobile_number_3': contact.mobile_number_3,
            'mobile_number_3_name': contact.mobile_number_3_name,
            'mobile_number_3_note': contact.mobile_number_3_note,
            'mobile_number_3_email': contact.mobile_number_3_email,
            'mobile_number_4': contact.mobile_number_4,
            'mobile_number_4_name': contact.mobile_number_4_name,
            'mobile_number_4_note': contact.mobile_number_4_note,
            'mobile_number_4_email': contact.mobile_number_4_email,
            'address_1': contact.address_1,
            'postal_code_1': contact.postal_code_1,
            'address_2': contact.address_2,
            'postal_code_2': contact.postal_code_2,
            'address_3': contact.address_3,
            'postal_code_3': contact.postal_code_3,
            'description': contact.description,
            'fax': contact.fax,
        }

        contact.first_name = request.POST.get("first_name") or ""
        contact.last_name = request.POST.get("last_name") or ""
        contact.organization = request.POST.get("organization") or ""
        contact.category = request.POST.get("category") or ""
        contact.business_type = request.POST.get("business_type") or ""
        contact.sex = request.POST.get("sex") or ""
        contact.phone_number_1 = request.POST.get("phone_number_1") or ""
        contact.phone_number_1_name = request.POST.get("phone_number_1_name") or ""
        contact.phone_number_1_organizational_position = request.POST.get("phone_number_1_organizational_position") or ""
        contact.phone_number_1_ex = request.POST.get("phone_number_1_ex") or ""
        contact.phone_number_1_note = request.POST.get("phone_number_1_note") or ""
        contact.phone_number_2 = request.POST.get("phone_number_2") or ""
        contact.phone_number_2_name = request.POST.get("phone_number_2_name") or ""
        contact.phone_number_2_organizational_position = request.POST.get("phone_number_2_organizational_position") or ""
        contact.phone_number_2_ex = request.POST.get("phone_number_2_ex") or ""
        contact.phone_number_2_note = request.POST.get("phone_number_2_note") or ""
        contact.phone_number_3 = request.POST.get("phone_number_3") or ""
        contact.phone_number_3_name = request.POST.get("phone_number_3_name") or ""
        contact.phone_number_3_organizational_position = request.POST.get("phone_number_3_organizational_position") or ""
        contact.phone_number_3_ex = request.POST.get("phone_number_3_ex") or ""
        contact.phone_number_3_note = request.POST.get("phone_number_3_note") or ""
        contact.phone_number_4 = request.POST.get("phone_number_4") or ""
        contact.phone_number_4_name = request.POST.get("phone_number_4_name") or ""
        contact.phone_number_4_organizational_position = request.POST.get("phone_number_4_organizational_position") or ""
        contact.phone_number_4_ex = request.POST.get("phone_number_4_ex") or ""
        contact.phone_number_4_note = request.POST.get("phone_number_4_note") or ""
        contact.phone_number_5 = request.POST.get("phone_number_5") or ""
        contact.phone_number_5_name = request.POST.get("phone_number_5_name") or ""
        contact.phone_number_5_organizational_position = request.POST.get("phone_number_5_organizational_position") or ""
        contact.phone_number_5_ex = request.POST.get("phone_number_5_ex") or ""
        contact.phone_number_5_note = request.POST.get("phone_number_5_note") or ""
        contact.phone_number_6 = request.POST.get("phone_number_6") or ""
        contact.phone_number_6_name = request.POST.get("phone_number_6_name") or ""
        contact.phone_number_6_organizational_position = request.POST.get("phone_number_6_organizational_position") or ""
        contact.phone_number_6_ex = request.POST.get("phone_number_6_ex") or ""
        contact.phone_number_6_note = request.POST.get("phone_number_6_note") or ""
        contact.mobile_number_1 = request.POST.get("mobile_number_1") or ""
        contact.mobile_number_1_name = request.POST.get("mobile_number_1_name") or ""
        contact.mobile_number_1_note = request.POST.get("mobile_number_1_note") or ""
        contact.mobile_number_1_email = request.POST.get("mobile_number_1_email") or ""
        contact.mobile_number_2 = request.POST.get("mobile_number_2") or ""
        contact.mobile_number_2_name = request.POST.get("mobile_number_2_name") or ""
        contact.mobile_number_2_note = request.POST.get("mobile_number_2_note") or ""
        contact.mobile_number_2_email = request.POST.get("mobile_number_2_email") or ""
        contact.mobile_number_3 = request.POST.get("mobile_number_3") or ""
        contact.mobile_number_3_name = request.POST.get("mobile_number_3_name") or ""
        contact.mobile_number_3_note = request.POST.get("mobile_number_3_note") or ""
        contact.mobile_number_3_email = request.POST.get("mobile_number_3_email") or ""
        contact.mobile_number_4 = request.POST.get("mobile_number_4") or ""
        contact.mobile_number_4_name = request.POST.get("mobile_number_4_name") or ""
        contact.mobile_number_4_note = request.POST.get("mobile_number_4_note") or ""
        contact.mobile_number_4_email = request.POST.get("mobile_number_4_email") or ""
        contact.address_1 = request.POST.get("address_1") or ""
        contact.postal_code_1 = request.POST.get("postal_code_1") or ""
        contact.address_2 = request.POST.get("address_2") or ""
        contact.postal_code_2 = request.POST.get("postal_code_2") or ""
        contact.address_3 = request.POST.get("address_3") or ""
        contact.postal_code_3 = request.POST.get("postal_code_3") or ""
        contact.description = request.POST.get("description") or ""
        contact.fax = request.POST.get("fax") or ""

        changes = []
        new_values = {
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'organization': contact.organization,
            'category': contact.category,
            'business_type': contact.business_type,
            'sex': contact.sex,
            'phone_number_1': contact.phone_number_1,
            'phone_number_1_name': contact.phone_number_1_name,
            'phone_number_1_organizational_position': contact.phone_number_1_organizational_position,
            'phone_number_1_ex': contact.phone_number_1_ex,
            'phone_number_1_note': contact.phone_number_1_note,
            'phone_number_2': contact.phone_number_2,
            'phone_number_2_name': contact.phone_number_2_name,
            'phone_number_2_organizational_position': contact.phone_number_2_organizational_position,
            'phone_number_2_ex': contact.phone_number_2_ex,
            'phone_number_2_note': contact.phone_number_2_note,
            'phone_number_3': contact.phone_number_3,
            'phone_number_3_name': contact.phone_number_3_name,
            'phone_number_3_organizational_position': contact.phone_number_3_organizational_position,
            'phone_number_3_ex': contact.phone_number_3_ex,
            'phone_number_3_note': contact.phone_number_3_note,
            'phone_number_4': contact.phone_number_4,
            'phone_number_4_name': contact.phone_number_4_name,
            'phone_number_4_organizational_position': contact.phone_number_4_organizational_position,
            'phone_number_4_ex': contact.phone_number_4_ex,
            'phone_number_4_note': contact.phone_number_4_note,
            'phone_number_5': contact.phone_number_5,
            'phone_number_5_name': contact.phone_number_5_name,
            'phone_number_5_organizational_position': contact.phone_number_5_organizational_position,
            'phone_number_5_ex': contact.phone_number_5_ex,
            'phone_number_5_note': contact.phone_number_5_note,
            'phone_number_6': contact.phone_number_6,
            'phone_number_6_name': contact.phone_number_6_name,
            'phone_number_6_organizational_position': contact.phone_number_6_organizational_position,
            'phone_number_6_ex': contact.phone_number_6_ex,
            'phone_number_6_note': contact.phone_number_6_note,
            'mobile_number_1': contact.mobile_number_1,
            'mobile_number_1_name': contact.mobile_number_1_name,
            'mobile_number_1_note': contact.mobile_number_1_note,
            'mobile_number_1_email': contact.mobile_number_1_email,
            'mobile_number_2': contact.mobile_number_2,
            'mobile_number_2_name': contact.mobile_number_2_name,
            'mobile_number_2_note': contact.mobile_number_2_note,
            'mobile_number_2_email': contact.mobile_number_2_email,
            'mobile_number_3': contact.mobile_number_3,
            'mobile_number_3_name': contact.mobile_number_3_name,
            'mobile_number_3_note': contact.mobile_number_3_note,
            'mobile_number_3_email': contact.mobile_number_3_email,
            'mobile_number_4': contact.mobile_number_4,
            'mobile_number_4_name': contact.mobile_number_4_name,
            'mobile_number_4_note': contact.mobile_number_4_note,
            'mobile_number_4_email': contact.mobile_number_4_email,
            'address_1': contact.address_1,
            'postal_code_1': contact.postal_code_1,
            'address_2': contact.address_2,
            'postal_code_2': contact.postal_code_2,
            'address_3': contact.address_3,
            'postal_code_3': contact.postal_code_3,
            'description': contact.description,
            'fax': contact.fax,
        }

        for field, old_value in old_values.items():
            new_value = new_values[field]
            old_value = "" if old_value is None else old_value
            new_value = "" if new_value is None else new_value
            if old_value != new_value:
                changes.append(f'{request.user} changed {field} from "{old_value}" to "{new_value}"')

        if changes:
            contact.deleted_data = (contact.deleted_data or '') + '\n'.join(changes) + '\n'

        contact.latest_editor = f"{request.user}"
        contact.latest_editor_log = f'{request.user} Edited this contact.'
        contact.modified_at = jdatetime.datetime.now()

        contact.save()
        UserActivityLog.objects.create(user=request.user, action=f"Edited contact {contact.last_name or contact.first_name  or contact.organization} ({contact.id})")
        messages.success(request, "اطلاعات مخاطب با موفقیت بروزرسانی شد")
        return redirect("contacts:public_contact_details", pk=contact.id)
    return redirect("contacts:edit_contact", contact_id=contact.id)