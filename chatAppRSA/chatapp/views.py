# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import *
from . models import *
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')  # Change 'home' to the name of your homepage URL pattern
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')
def home(request):
    return render(request, 'home.html')

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Get recipient and their public key
            recipient_username = form.cleaned_data['recipient']
            recipient = User.objects.get(username=recipient_username)
            recipient_profile = UserProfile.objects.get(user=recipient)
            recipient_public_key = RSA.import_key(recipient_profile.public_key)
            
            # Encrypt the message content
            content = form.cleaned_data['content']
            cipher = PKCS1_OAEP.new(recipient_public_key)
            encrypted_content = cipher.encrypt(content.encode())
            encrypted_content_base64 = base64.b64encode(encrypted_content)

            # Create the message instance with encrypted content
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                encrypted_content=encrypted_content_base64
            )
            
            return redirect('home')  # Redirect to the home page after sending the message
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})


def view_messages(request):
    # Retrieve all messages for the current user
    user_messages = Message.objects.filter(recipient=request.user)
    
    # Decrypt message content using the user's private key
    for message in user_messages:
        if message.encrypted_content:
            decrypted_content = message.decrypt_message(request.user.userprofile.private_key)
            message.content = decrypted_content
            message.save()
    
    return render(request, 'view_messages.html', {'user_messages': user_messages})

