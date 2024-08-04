from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User  # Django User model
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Note, Comment, Like  # Import your models here


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON request body
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not (username and password and email):
            return JsonResponse({'error': 'Username, password, and email are required'}, status=400)

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Create new user
        new_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return JsonResponse({'message': 'User created successfully'}, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data.get('username')
        # email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(username=username)

        if not user:
            return JsonResponse({'error': 'User Does not exists'}, status=400)
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Incorrect password'}, status=400)
        return JsonResponse({'message': 'Login successfull'}, status=201)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
