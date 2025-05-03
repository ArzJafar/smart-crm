from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
import cowsay
import random
import jdatetime
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.shortcuts import redirect

def main(request):
    if not request.user.is_authenticated:
        return redirect('login')

    jdatetime.set_locale(jdatetime.FA_LOCALE)
    current_datetime = jdatetime.datetime.now().strftime('%Y/%m/%d')
    current_time = jdatetime.datetime.now().strftime('%H:%M')
    week_day = jdatetime.datetime.now().strftime('%A')
    username = request.user.first_name
    return render(request, 'main.html', {'firstname': username, 'time': current_time, 'date': current_datetime, 'week_day': week_day, 'version': settings.VERSION})


def logout_view(request):
    chars = ['beavis', 'cheese', 'cow', 'daemon', 'dragon', 'fox', 'ghostbusters', 'kitty',
'meow', 'miki', 'milk', 'octopus', 'pig', 'stegosaurus', 'stimpy', 'trex', 
'turkey', 'turtle', 'tux']
    char = random.choice(chars)
    cow_message = cowsay.get_output_string(f'{char}', '!بدرود')
    
    return render(request, 'registration/logout_page.html', {'cow_message': cow_message})


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']  


@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            if form.cleaned_data['first_name'] != request.user.first_name:
                request.user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name'] != request.user.last_name:
                request.user.last_name = form.cleaned_data['last_name']
            
            request.user.save()
            return redirect('/')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'profile/profile.html', {'form': form})

@api_view(['GET'])
def test_api(request):
    return Response({
        'message': 'API is working!',
        'status': 'success',
        'data': {
            'backend': 'Django',
            'frontend': 'React',
            'connection': 'successful'
        }
    })