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
            'mo_ta': forms.Textarea(attrs={'rows': 4}),
            # Thêm các widget khác nếu cần
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
    can_delete=True # Cho phép xóa ảnh cũ
)