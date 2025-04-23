from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import Profile
from .tokens import account_activation_token  # Di chuyển import này sau models
from .forms import EmailRegistrationForm, ProfileUpdateForm  # Di chuyển sau tokens
import uuid

def register(request):
    if request.method == 'POST':
        form = EmailRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Tạo token xác thực
            token = str(uuid.uuid4())
            user.profile.email_token = token
            user.profile.save()
            
            # Gửi email xác nhận
            current_site = get_current_site(request)
            mail_subject = 'Xác nhận tài khoản LandHub'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': '127.0.0.1:8000',  # Cố định domain thành localhost
                'token': token,
            })
            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.content_subtype = "html"
            email.send()
            
            # Thông báo cho người dùng
            messages.success(request, 'Vui lòng kiểm tra email của bạn để hoàn tất đăng ký.')
            return redirect('accounts:verification_sent')
    else:
        form = EmailRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verification_sent(request):
    return render(request, 'accounts/verification_sent.html')

def verify_email(request, token):
    try:
        profile = Profile.objects.get(email_token=token)
        if profile:
            # Kích hoạt tài khoản
            user = profile.user
            user.is_active = True
            user.save()
            
            # Đánh dấu email đã xác minh
            profile.email_verified = True
            profile.email_token = None  # Xóa token để không thể dùng lại
            profile.save()
            
            # Đăng nhập người dùng
            login(request, user)
            
            # Chuyển hướng đến trang cập nhật thông tin
            messages.success(request, 'Xác minh email thành công! Vui lòng cập nhật thông tin cá nhân của bạn.')
            return redirect('accounts:update_profile')
        else:
            messages.error(request, 'Link xác nhận không hợp lệ!')
            return redirect('accounts:login')
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        messages.error(request, 'Link xác nhận không hợp lệ!')
        return redirect('accounts:login')

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if 'first_name' in request.POST:
            request.user.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            request.user.last_name = request.POST['last_name']
        
        if profile_form.is_valid():
            request.user.save()
            profile_form.save()
            messages.success(request, 'Thông tin cá nhân đã được cập nhật!')
            return redirect('products:product_list')  # Chuyển về trang chính
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        # Thêm first_name, last_name từ user model
        profile_form.fields['first_name'].initial = request.user.first_name
        profile_form.fields['last_name'].initial = request.user.last_name
        
    return render(request, 'accounts/update_profile.html', {
        'profile_form': profile_form,
    })

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

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Thêm namespace