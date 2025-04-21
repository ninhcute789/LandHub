# LandHub/products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required # Yêu cầu đăng nhập
from django.http import HttpResponseForbidden # Trả lỗi nếu không có quyền
from django.urls import reverse_lazy
from django.db import transaction # Để đảm bảo lưu form và formset cùng lúc

from .models import Product, ProductImage #, Category
from .forms import ProductForm, ProductImageFormSet # Import form

# View product_list, product_detail giữ nguyên
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

def register_view(request):
    if request.method == 'POST':
        # form = RegistrationForm(request.POST) # Dùng form tùy chỉnh
        form = UserCreationForm(request.POST) # Dùng form mặc định
        if form.is_valid():
            user = form.save()
            # login(request, user) # Tùy chọn: tự động đăng nhập user mới
            return redirect('/') # Chuyển hướng về trang chủ hoặc trang đăng nhập
    else:
        # form = RegistrationForm() # Dùng form tùy chỉnh
        form = UserCreationForm() # Dùng form mặc định
    return render(request, 'registration/register.html', {'form': form})

# --- VIEW MỚI ---

@login_required # Chỉ user đã đăng nhập mới vào được
def create_listing(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # Thêm request.FILES cho ảnh đại diện
        formset = ProductImageFormSet(request.POST, request.FILES, prefix='images') # prefix quan trọng

        if form.is_valid() and formset.is_valid():
            try:
                # Dùng transaction để đảm bảo cả hai lưu thành công hoặc không lưu gì cả
                with transaction.atomic():
                    # Lưu product chính, nhưng chưa commit vào DB
                    product = form.save(commit=False)
                    # Gán owner là user đang đăng nhập
                    product.owner = request.user
                    # Lưu product vào DB để có ID cho ảnh chi tiết
                    product.save() # Hàm save() tùy chỉnh của bạn sẽ tự tạo slug

                    # Lưu ảnh chi tiết liên quan đến product vừa tạo
                    formset.instance = product
                    formset.save()

                # Chuyển hướng đến trang chi tiết hoặc trang quản lý tin
                return redirect(product.get_absolute_url())
            except Exception as e:
                # Xử lý lỗi nếu có (ví dụ: log lỗi)
                print(f"Error saving listing: {e}") # Log lỗi ra console server
                # Có thể thêm message lỗi cho người dùng
        else:
             print("Form errors:", form.errors)
             print("Formset errors:", formset.errors)

    else: # Nếu là request GET (lần đầu truy cập trang)
        form = ProductForm()
        formset = ProductImageFormSet(prefix='images')

    return render(request, 'products/listing_form.html', {
        'form': form,
        'formset': formset,
        'form_title': 'Đăng tin bất động sản mới'
    })

@login_required
def edit_listing(request, pk): # Dùng pk (primary key) thay vì id, slug cho đơn giản
    product = get_object_or_404(Product, pk=pk)

    # --- KIỂM TRA QUYỀN SỞ HỮU ---
    if product.owner != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền sửa tin đăng này.")
    # -----------------------------

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product, prefix='images')

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save() # Lưu thay đổi product
                    formset.save() # Lưu thay đổi ảnh (thêm/sửa/xóa)
                return redirect(product.get_absolute_url())
            except Exception as e:
                print(f"Error updating listing: {e}")

        else:
             print("Form errors:", form.errors)
             print("Formset errors:", formset.errors)

    else: # Request GET
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product, prefix='images')

    return render(request, 'products/listing_form.html', {
        'form': form,
        'formset': formset,
        'product': product, # Gửi product để biết đang sửa tin nào
        'form_title': f'Chỉnh sửa tin: {product.tieu_de}'
    })

@login_required
def delete_listing(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # --- KIỂM TRA QUYỀN SỞ HỮU ---
    if product.owner != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền xóa tin đăng này.")
    # -----------------------------

    if request.method == 'POST': # Chỉ xóa khi có xác nhận bằng POST
        product_title = product.tieu_de # Lưu lại tiêu đề trước khi xóa
        product.delete()
        # Có thể thêm message thành công
        # Chuyển hướng về trang quản lý tin
        return redirect('products:my_listings') # Giả sử có URL name 'my_listings'

    # Nếu là GET, hiển thị trang xác nhận xóa
    return render(request, 'products/listing_delete_confirm.html', {'product': product})


@login_required
def my_listings(request):
    # Lấy tất cả tin đăng của user đang đăng nhập
    user_listings = Product.objects.filter(owner=request.user).order_by('-ngay_dang')
    return render(request, 'products/my_listings.html', {'listings': user_listings})