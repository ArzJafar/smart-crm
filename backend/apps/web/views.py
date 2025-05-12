from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.utils import timezone
import json

def main(request):
    return render(request, 'web/main.html')

@login_required
def profile(request):
    return render(request, 'web/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    try:
        # Delete the token
        request.user.auth_token.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'خروج موفقیت‌آمیز بود'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
@csrf_exempt
def login_api(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Delete any existing tokens
            Token.objects.filter(user=user).delete()
            # Create a new token
            token = Token.objects.create(user=user)
            
            return JsonResponse({
                'status': 'success',
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'نام کاربری یا رمز عبور اشتباه است'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    if request.method == 'GET':
        return JsonResponse({
            'status': 'success',
            'user': UserSerializer(request.user).data
        })
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            
            # Update user fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']
            
            user.save()
            
            return JsonResponse({
                'status': 'success',
                'user': UserSerializer(user).data
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def main_api(request):
    current_time = timezone.now()
    return JsonResponse({
        'status': 'success',
        'date': current_time.strftime('%Y-%m-%d'),
        'time': current_time.strftime('%H:%M:%S'),
        'user': UserSerializer(request.user).data
    })