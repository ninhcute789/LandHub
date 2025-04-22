from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập tên đăng nhập',
                'autocomplete': 'username',  # Gợi ý tự động điền
            }),
            'email': forms.EmailInput(attrs={
                'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập email',
                'autocomplete': 'email',  # Gợi ý tự động điền
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Tên',
                'autocomplete': 'first_name',  # Gợi ý tự động điền
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Họ'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Mật khẩu'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Xác nhận mật khẩu'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Nhập số điện thoại'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh thông báo lỗi
        self.fields['password1'].help_text = 'Mật khẩu của bạn phải chứa ít nhất 8 ký tự'
        self.fields['password2'].help_text = 'Nhập lại mật khẩu để xác nhận'
        
        # Thêm class cho các trường password
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })

    def save(self, commit=True):
        user = super().save(commit=True)
        # Lưu số điện thoại vào profile
        user.profile.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.profile.save()
        return user
