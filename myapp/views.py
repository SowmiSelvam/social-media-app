
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import JsonResponse,   response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User  # Django User model
import json
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Note, Comment, Like  # Import your models here
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        new_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return JsonResponse({'message': 'User created successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        tokens = get_tokens_for_user(user)
        return JsonResponse(tokens, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth_status(request):
    jwt_authentication = JWTAuthentication()
    try:

        validated_token = jwt_authentication.authenticate(request)
        if validated_token is not None:
            return Response({'authenticated': True}, status=200)
    except AuthenticationFailed:
        pass

    return Response({'authenticated': False}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_note(request):
    data = json.loads(request.body)
    content = data.get('content')
    date = None
    user = request.user
    if not content:
        return JsonResponse({'error': 'content cannot be empty'}, status=400)
    new_note = Note.objects.create(
        content=content,
        date=date,
        user=user)

    new_note_json = {
        'id': new_note.id,
        'content': new_note.content,
        'date': new_note.date.strftime('%Y-%m-%d %H:%M:%S') if new_note.date else None,
        'user': new_note.user.username  # Example, adjust based on your user model
    }

    return JsonResponse({'notes': new_note_json}, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)

    data = json.loads(request.body)
    new_content = data.get('content')

    if new_content:
        note.content = new_content
        note.save()
        return JsonResponse({'success': 'Note updated'}, status=200)
    else:
        return JsonResponse({'error': 'Content cannot be empty'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_notes(request):
    notes = Note.objects.filter(user=request.user)
    notes_data = list(notes.values())
    response_data = {'notes': notes_data}
    return JsonResponse(response_data, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    note.delete()
    return JsonResponse({'success': 'note deleted'}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    notes = Note.objects.all()  # Fetch all notes from the database
    notes_data = []

    for note in notes:
        user_id = note.user_id  # Assuming 'user_id' is the field in your Note model
        username = get_username(user_id)
        note_data = {
            'id': note.id,
            'content': note.content,
            'user_id': user_id,
            'username': username,  # Add the username to each note data
        }
        notes_data.append(note_data)

    response_data = {'notes': notes_data}
    return JsonResponse(response_data, status=200)


@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            refresh_token = data.get('refresh_token')
            if not refresh_token:
                return JsonResponse({'error': 'Refresh token is required'}, status=400)

            # Create a RefreshToken object
            try:
                token = RefreshToken(refresh_token)
            except TokenError as e:
                return JsonResponse({'error': str(e)}, status=400)

            try:

                outstanding_token = OutstandingToken.objects.get(token=token)

                BlacklistedToken.objects.create(token=outstanding_token)
            except OutstandingToken.DoesNotExist:
                return JsonResponse({'error': 'Token not found'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            return JsonResponse({'message': 'Logout successful'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_username(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user.username
    except User.DoesNotExist:
        return None
