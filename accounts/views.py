from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import HttpResponse
from .models import Profile

# Đăng ký người dùng
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Đảm bảo profile được tạo
            Profile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo thành công!')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Đăng nhập người dùng
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Kiểm tra nếu user là superuser thì redirect sang admin
            if user.is_superuser:
                return redirect('admin:index')
            return redirect('products:product_list')
        else:
            messages.error(request, 'Thông tin đăng nhập không đúng!')
    return render(request, 'accounts/login.html', {
        'messages': messages.get_messages(request)
    })

# Đăng xuất người dùng
def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Thêm namespace