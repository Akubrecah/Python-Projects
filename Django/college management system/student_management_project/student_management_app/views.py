# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .models import CustomUser, Staffs, Students, AdminHOD
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def loginUser(request):
    return render(request, 'login_page.html')

def doLogin(request):
    if request.method != 'POST':
        messages.error(request, "Invalid request method!")
        return redirect('login')
    
    email_id = request.POST.get('email')
    password = request.POST.get('password')

    if not (email_id and password):
        messages.error(request, "Please provide all the details!")
        return render(request, 'login_page.html')

    user = authenticate(request, username=email_id, password=password)

    if not user:
        messages.error(request, 'Invalid Login Credentials!')
        return render(request, 'login_page.html')

    login(request, user)

    if user.user_type == CustomUser.STUDENT:
        return redirect('student_home')
    elif user.user_type == CustomUser.STAFF:
        return redirect('staff_home')
    elif user.user_type == CustomUser.HOD:
        return redirect('admin_home')

    return redirect('home')

def registration(request):
    return render(request, 'registration.html')

def doRegistration(request):
    if request.method != 'POST':
        messages.error(request, "Invalid request method!")
        return redirect('registration')
    
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirmPassword')

    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details!')
        return render(request, 'registration.html')
    
    if password != confirm_password:
        messages.error(request, 'Passwords do not match!')
        return render(request, 'registration.html')

    if CustomUser.objects.filter(email=email_id).exists():
        messages.error(request, 'Email already registered. Please login.')
        return render(request, 'registration.html')

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(request, "Invalid email format! Use: 'name.student@domain', 'name.staff@domain' or 'name.hod@domain'")
        return render(request, 'registration.html')

    username = email_id.split('@')[0]
    if '.' in username:
        username = username.split('.')[0]

    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists. Please use a different email.')
        return render(request, 'registration.html')

    try:
        user = CustomUser.objects.create_user(
            username=username,
            email=email_id,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )
        
        if user_type == CustomUser.STAFF:
            Staffs.objects.create(admin=user)
        elif user_type == CustomUser.STUDENT:
            Students.objects.create(admin=user)
        elif user_type == CustomUser.HOD:
            AdminHOD.objects.create(admin=user)
            
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
        
    except Exception as e:
        messages.error(request, f'Registration failed: {str(e)}')
        return render(request, 'registration.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def get_user_type_from_email(email_id):
    try:
        email_user_type = email_id.split('@')[0].split('.')[-1]
        return {
            'student': CustomUser.STUDENT,
            'staff': CustomUser.STAFF,
            'hod': CustomUser.HOD
        }.get(email_user_type)
    except Exception:
        return None

# urls.py
from django.contrib import admin
from django.urls import path
from . import views
from . import HodViews, StaffViews, StudentViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('registration/', views.registration, name="registration"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('doRegistration/', views.doRegistration, name="doRegistration"),
    
    # Student URLs
    path('student_home/', StudentViews.student_home, name="student_home"),
    
    # Staff URLs
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    
    # Admin URLs
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    
    # Other paths remain the same as in original...
    # Include all other paths from original without modification
]