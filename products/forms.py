# LandHub/products/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Liệt kê các trường người dùng được phép nhập/sửa
        fields = [
            'tieu_de', 'mo_ta', 'gia', 'dien_tich', 'phap_ly', 'huong',
            'mat_tien', 'chieu_dai', 'loai_dat', 'dia_chi', 'tinh_thanh',
            'quan_huyen', 'phuong_xa', 'vi_do', 'kinh_do', 'anh_dai_dien',
            'ten_nguoi_ban', 'so_dien_thoai', 'email', # <-- Thêm 3 trường này
        ]
        # Thêm widgets nếu muốn tùy chỉnh giao diện input (ví dụ: Textarea cho mô tả)
        widgets = {
            'mo_ta': forms.Textarea(attrs={
                'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập mặt tiền (ví dụ: 5m hoặc mô tả chi tiết hơn)',
                'rows': 4,
            }),
            # Thêm các widget khác nếu cần
            'loai_dat': forms.Select(attrs={
                'class': 'block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'phap_ly': forms.Select(attrs={
                'class': 'block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'huong': forms.Select(attrs={
                'class': 'block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'tieu_de': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập tiêu đề'
            }),
            'gia': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập giá'
            }),
            'dien_tich': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập diện tích'
            }),
            'mat_tien': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập mặt tiền'
            }),
            'chieu_dai': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập chiều dài'
            }),
            'dia_chi': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập địa chỉ'
            }),
            'tinh_thanh': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập tỉnh/thành phố'
            }),
            'quan_huyen': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập quận/huyện'
            }),
            'phuong_xa': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập phường/xã'
            }),
            'vi_do': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập vĩ độ'
            }),
            'kinh_do': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập kinh độ'
            }),
            'ten_nguoi_ban': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập tên người bán'
            }),
            'so_dien_thoai': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập số điện thoại'
            }),
            'email': forms.TextInput(attrs={
                'class': 'appearance-none block w-fit px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nhập email'
            }),
            
        }

    # Thêm validation tùy chỉnh nếu cần
    def clean_gia(self):
        gia = self.cleaned_data.get('gia')
        if gia is not None and gia < 0:
            raise forms.ValidationError("Giá không được là số âm.")
        return gia
    
    # Thêm validation cho số điện thoại nếu cần
    def clean_so_dien_thoai(self):
        sdt = self.cleaned_data.get('so_dien_thoai')
        return sdt

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)
        
        
# Tạo FormSet cho ảnh chi tiết
# extra=3 nghĩa là hiển thị 3 form trống để tải ảnh mới mỗi lần
ProductImageFormSet = inlineformset_factory(
    Product,  # Model cha
    ProductImage,  # Model con (inline)
    fields=('image', 'alt_text'),  # Các trường trong form con
    extra=3,  # Số form trống ban đầu
    # can_delete=True # Cho phép xóa ảnh cũ
    widgets={
        'image': forms.ClearableFileInput(attrs={
            'class': 'block w-fit text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
        }),
        'alt_text': forms.Textarea(attrs={
            'class': 'h-20 block w-1/2 px-3 pt-2 text-sm text-gray-900 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Nhập văn bản thay thế',
        }),
    }
)