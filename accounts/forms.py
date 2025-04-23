from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập email',
        }))
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập tên',
        }))
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập họ',
        }))
    phone_number = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập số điện thoại',
        }))
    password1 = forms.CharField(
        max_length=30, required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập mật khẩu',
            'autocomplete': 'new-password',  # Ngăn tự động điền
        })
    )
    password2 = forms.CharField(
        max_length=30, required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập lại mật khẩu',
            'autocomplete': 'new-password',  # Ngăn tự động điền
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập tên đăng nhập',
                # 'autocomplete': 'username',  # Gợi ý tự động điền
                'autocomplete': 'off',  # Ngăn tự động điền
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập mật khẩu',
                # 'autocomplete': 'username',  # Gợi ý tự động điền
                'autocomplete': 'off',  # Ngăn tự động điền
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập lại mật khẩu',
                # 'autocomplete': 'username',  # Gợi ý tự động điền
                'autocomplete': 'off',  # Ngăn tự động điền
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

class EmailRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'example@email.com',
            'required': 'required',
        }),
        required=True
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Mật khẩu',
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Nhập lại mật khẩu',
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh thông báo lỗi
        self.fields['password1'].help_text = 'Mật khẩu của bạn phải chứa ít nhất 8 ký tự'
        self.fields['password2'].help_text = 'Nhập lại mật khẩu để xác nhận'
        # Không cần username trong form
        if 'username' in self.fields:
            del self.fields['username']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Sử dụng email làm username
        user.username = self.cleaned_data.get('email')
        user.email = self.cleaned_data.get('email')
        user.is_active = False  # Tài khoản chưa được kích hoạt
        
        if commit:
            user.save()
            # Tạo profile cho user
            Profile.objects.get_or_create(user=user)
        
        return user

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'birth_date', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
