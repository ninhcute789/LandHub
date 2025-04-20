# LandHub/products/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage # Đảm bảo import đúng model

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug':('name',)}
    # Xóa nếu không dùng Category nữa
    
class ProductImageInline(admin.TabularInline): # Hoặc admin.StackedInline nếu muốn hiển thị dạng stack
    model = ProductImage
    extra = 1 # Số lượng form trống để thêm ảnh mới, mặc định là 3, đặt 1 cho gọn
    fields = ('image', 'alt_text') # Các trường hiển thị trong inline form

@admin.register(Product) # Hoặc tên model bạn đã đổi
class ProductAdmin(admin.ModelAdmin):
    # Chỉ cần dòng này để tự động điền slug
    prepopulated_fields = {'slug': ('tieu_de',)}

    # Các dòng dưới đây ảnh hưởng đến màn hình danh sách, không phải form thêm/sửa:
    list_display = ["tieu_de", "gia", "dien_tich", "tinh_thanh", "trang_thai", "available"]
    list_filter = ["trang_thai", "tinh_thanh", "loai_dat", "available"]
    search_fields = ["tieu_de", "mo_ta", "dia_chi"]
    list_editable = ["gia", "trang_thai", "available"]
    inlines = [ProductImageInline]

    # !!! QUAN TRỌNG: Đảm bảo không có dòng 'fields = [...]' hoặc 'fieldsets = [...]'
    # Nếu có, hãy thử xóa hoặc comment chúng đi để kiểm tra
    # fields = ['tieu_de', 'slug'] # <--- VÍ DỤ: Nếu có dòng này, chỉ 2 trường này hiện ra. HÃY XÓA HOẶC COMMENT NÓ.
    # fieldsets = (
    #    (None, {'fields': ('tieu_de', 'slug')}),
    # ) # <--- VÍ DỤ: fieldsets cũng giới hạn trường hiển thị. HÃY XÓA HOẶC COMMENT NÓ.