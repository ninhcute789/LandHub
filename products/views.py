# LandHub/products/views.py
from django.shortcuts import render, get_object_or_404
# Bỏ Category nếu không dùng nữa
from .models import Product #, Category

def product_list(request):
    # Lấy tất cả các lựa chọn lọc từ models.py
    huong_choices = Product.HuongDatChoices.choices
    phap_ly_choices = Product.PhapLyChoices.choices
    loai_dat_choices = Product.LoaiDatChoices.choices
    # Thêm các choices khác nếu bạn muốn lọc theo chúng

    # Lấy các giá trị lọc người dùng đã chọn từ request GET
    # Dùng getlist nếu muốn cho phép chọn nhiều giá trị (ví dụ: checkboxes)
    selected_huong = request.GET.getlist('huong')
    selected_phap_ly = request.GET.getlist('phap_ly')
    selected_loai_dat = request.GET.getlist('loai_dat')
    # Lấy các giá trị lọc khác nếu có

    # Bắt đầu với queryset cơ bản
    products = Product.objects.filter(available=True)

    # Áp dụng bộ lọc nếu người dùng đã chọn
    if selected_huong:
        products = products.filter(huong__in=selected_huong)
    if selected_phap_ly:
        products = products.filter(phap_ly__in=selected_phap_ly)
    if selected_loai_dat:
        products = products.filter(loai_dat__in=selected_loai_dat)
    # Áp dụng các bộ lọc khác nếu có

    context = {
        'products': products,
        'huong_choices': huong_choices,
        'phap_ly_choices': phap_ly_choices,
        'loai_dat_choices': loai_dat_choices,
        # Gửi các giá trị đã chọn để giữ trạng thái form
        'selected_huong': selected_huong,
        'selected_phap_ly': selected_phap_ly,
        'selected_loai_dat': selected_loai_dat,
        # Thêm các choices và selected values khác nếu cần
    }
    return render(request, 'products/product/list.html', context)

# View product_detail giữ nguyên hoặc cập nhật nếu cần
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # Lấy tất cả ảnh chi tiết liên quan đến sản phẩm này
    # Sử dụng related_name 'images' đã định nghĩa trong ForeignKey của ProductImage
    detail_images = product.images.all()

    context = {
        'product': product,
        'detail_images': detail_images, # Truyền danh sách ảnh chi tiết vào context
    }
    return render(request, 'products/product/detail.html', context)