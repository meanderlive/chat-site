from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import *
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .forms import UserRegistrationForm,UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UserProfile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Message, UserProfile
from django.db.models import Q


def business_register(request):
    return render(request,'chat_tem/demo-it-business-register.html')


def business_home(request):
    return render(request,'chat_tem/demo-it-business.html')

def business_about(request):
    return render(request,'chat_tem/demo-it-business-about.html')

def business_blog(request):
    return render(request,'chat_tem/demo-it-business-blog.html')

def business_case_studies(request):
    return render(request,'chat_tem/demo-it-business-case-studies.html')

def business_contact(request):
    return render(request,'chat_tem/demo-it-business-contact.html')

def business_services(request):
    return render(request,'chat_tem/demo-it-business-services.html')

def business_services_detail(request):
    return render(request,'chat_tem/demo-it-business-services-details.html')

User = get_user_model()

def home(request):
    return render(request, 'home.html')

@login_required
def user_list_view(request):
    users = User.objects.exclude(username=request.user.username)
    #return render(request, 'user_list.html', {'users': users})
    return render(request,"chat_tem/demo-it-business-views.html",{'users': users})


# work correct


@login_required
def chat_view(request, username):
    receiver = User.objects.get(username=username)
    receiver_profile = receiver.userprofile
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'chat.html', {'receiver': receiver, 'receiver_profile': receiver_profile, 'messages': messages})


@login_required
def chat_room(request, room_name):
    receiver = get_object_or_404(User, username=room_name)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) |
        (Q(receiver=request.user) & Q(sender=receiver))
    ).order_by('timestamp')

    try:
        receiver_profile = get_object_or_404(UserProfile, user=receiver)
    except UserProfile.DoesNotExist:
        receiver_profile = None

    return render(request, 'chat_tem/demo-it-business-chat.html', {
        'room_name': room_name,
        'messages': messages,
        'receiver_profile': receiver_profile,
    })

"""def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create(username=username, password=make_password(password))
        user.save()
        customer = Customer.objects.create(user=user)
        customer.save()
        login(request, user)
        return redirect('user_list')
    return render(request, 'register.html')"""

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login')  # Redirect to the user list or any other page
    else:
        form = UserRegistrationForm()
    #return render(request, 'register.html', {'form': form})
    return render(request,'chat_tem/demo-it-business-register.html',{'form': form})

"""def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request,'login.html')"""

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'chat_tem/demo-it-business-login.html', {'form': form})


@login_required
def create_or_update_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            #return redirect('user_list')
            return  redirect('get_profile')
    else:
        form = UserProfileForm(instance=profile)

    #return render(request, 'profile.html', {'form': form})
    return render(request, 'chat_tem/demo-it-business-profile.html', {'form': form})

@login_required
def get_profile(request):

    '''user = request.user
    try:
        user_profile = UserProfileForm.objects.get(user=user)
    except UserProfileForm.DoesNotExist:
        user_profile = None
    con={'profile': user_profile}'''
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    con={'profile': profile}

    return render(request, 'chat_tem/demo-it-business-get-profile.html', con)

@login_required
def delete_profile(request):

    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
        messages.success(request, 'Profile deleted successfully.')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile does not exist.')

    return redirect('get_profile')  # Redirect to a suitable page after deletion
