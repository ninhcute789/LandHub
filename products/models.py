# LandHub/products/models.py (đã cập nhật với default)

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# --- Model Category (giữ nguyên hoặc xóa/sửa tùy ý) ---
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

# --- Model Product (hoặc Property) với các trường đã thêm default ---
class Product(models.Model):

    # --- Các lớp Choices (giữ nguyên) ---
    class PhapLyChoices(models.TextChoices):
        SO_DO_SO_HONG = 'SDSH', _('Sổ đỏ/Sổ hồng')
        HOP_DONG_MUA_BAN = 'HDMB', _('Hợp đồng mua bán')
        VIET_TAY = 'VT', _('Giấy tờ viết tay')
        KHAC = 'KHAC', _('Khác')

    class HuongDatChoices(models.TextChoices):
        DONG = 'D', _('Đông')
        TAY = 'T', _('Tây')
        NAM = 'N', _('Nam')
        BAC = 'B', _('Bắc')
        DONG_BAC = 'DB', _('Đông Bắc')
        DONG_NAM = 'DN', _('Đông Nam')
        TAY_BAC = 'TB', _('Tây Bắc')
        TAY_NAM = 'TN', _('Tây Nam')
        KHONG_XAC_DINH = 'KXD', _('Không xác định')

    class LoaiDatChoices(models.TextChoices):
        DAT_O = 'DO', _('Đất ở (Thổ cư)')
        DAT_NONG_NGHIEP = 'DNN', _('Đất nông nghiệp')
        DAT_DU_AN = 'DDA', _('Đất dự án')
        DAT_THUONG_MAI = 'DTM', _('Đất thương mại dịch vụ')
        KHAC = 'KHAC', _('Loại khác')

    class TrangThaiChoices(models.TextChoices):
        CON_BAN = 'CB', _('Còn bán')
        DA_BAN = 'DB', _('Đã bán')
        DA_COC = 'DC', _('Đã đặt cọc')

    class LoaiTaiKhoanChoices(models.TextChoices):
        CA_NHAN = 'CN', _('Cá nhân')
        MOI_GIOI = 'MG', _('Môi giới')
        CONG_TY = 'CTY', _('Công ty')

    owner = models.ForeignKey(
        User,
        related_name='listings', # Giúp truy cập các tin đăng của user: user.listings.all()
        on_delete=models.CASCADE, # Nếu user bị xóa, các tin đăng của họ cũng bị xóa
        verbose_name=_('Người đăng'),
        default=1,
        # Bạn cần quyết định giá trị mặc định cho các tin đã tồn tại
        # null=True, blank=True, # Tùy chọn 1: Cho phép null tạm thời
        # default=1 # Tùy chọn 2: Gán cho user có id=1 (thường là admin đầu tiên)
    )
    
    users_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="wishlist_products",
        blank=True,
        verbose_name=_('Người dùng quan tâm')
    )
    
    # --- 🧱 Thông tin cơ bản ---
    tieu_de = models.CharField(_('Tiêu đề'), max_length=255, default='Chưa có tiêu đề') # Thêm default
    # slug: blank=True và có logic tự tạo trong save(), không cần default cứng ở đây.
    # Django sẽ xử lý được khi migrate hoặc bạn có thể cho phép null nếu cần.
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, help_text=_('Tự động tạo nếu để trống, dùng cho URL')) # Thêm null=True để chắc chắn migrate được
    mo_ta = models.TextField(_('Mô tả'), blank=True) # blank=True, không cần default
    gia = models.DecimalField(_('Giá'), max_digits=19, decimal_places=0, default=0, help_text=_('Đơn vị: VNĐ')) # Thêm default
    dien_tich = models.DecimalField(_('Diện tích (m²)'), max_digits=10, decimal_places=2, default=0.0) # Thêm default
    phap_ly = models.CharField(
        _('Pháp lý'),
        max_length=10,
        choices=PhapLyChoices.choices,
        default=PhapLyChoices.SO_DO_SO_HONG # Đã có default
    )
    huong = models.CharField(
        _('Hướng'),
        max_length=10,
        choices=HuongDatChoices.choices,
        blank=True,
        null=True # Đã có null=True
    )
    mat_tien = models.DecimalField(_('Mặt tiền (m)'), max_digits=6, decimal_places=2, blank=True, null=True) # Đã có null=True
    chieu_dai = models.DecimalField(_('Chiều dài (m)'), max_digits=6, decimal_places=2, blank=True, null=True) # Đã có null=True
    loai_dat = models.CharField(
        _('Loại đất'),
        max_length=10,
        choices=LoaiDatChoices.choices,
        default=LoaiDatChoices.DAT_O # Đã có default
    )

    # --- 📍 Thông tin vị trí ---
    dia_chi = models.CharField(_('Địa chỉ'), max_length=255, default='Chưa cung cấp') # Đã có default
    tinh_thanh = models.CharField(_('Tỉnh/Thành phố'), max_length=100, default='Chưa rõ') # Thêm default
    quan_huyen = models.CharField(_('Quận/Huyện'), max_length=100, default='Chưa rõ') # Thêm default
    phuong_xa = models.CharField(_('Phường/Xã'), max_length=100, default='Chưa rõ') # Thêm default
    vi_do = models.FloatField(_('Vĩ độ (Latitude)'), blank=True, null=True) # Đã có null=True
    kinh_do = models.FloatField(_('Kinh độ (Longitude)'), blank=True, null=True) # Đã có null=True

    # --- 🖼️ Hình ảnh ---
    anh_dai_dien = models.ImageField(_('Ảnh đại diện'), upload_to='property_images/', blank=True, null=True) # Đã có null=True

    # --- 📆 Thông tin thời gian & trạng thái ---
    ngay_dang = models.DateTimeField(_('Ngày đăng'), auto_now_add=True) # auto_now_add xử lý việc này
    ngay_cap_nhat = models.DateTimeField(_('Ngày cập nhật'), auto_now=True) # auto_now xử lý việc này
    trang_thai = models.CharField(
        _('Trạng thái'),
        max_length=10,
        choices=TrangThaiChoices.choices,
        default=TrangThaiChoices.CON_BAN # Đã có default
    )
    available = models.BooleanField(_('Còn hiển thị'), default=True) # Đã có default

    # --- 👤 Thông tin người bán ---
    ten_nguoi_ban = models.CharField(_('Tên người bán'), max_length=150, default='Chưa rõ') # Thêm default
    so_dien_thoai = models.CharField(_('Số điện thoại'), max_length=20, default='') # Thêm default (chuỗi rỗng)
    email = models.EmailField(_('Email liên hệ'), blank=True, null=True) # Đã có null=True
    loai_tai_khoan = models.CharField(
        _('Loại tài khoản'),
        max_length=10,
        choices=LoaiTaiKhoanChoices.choices,
        default=LoaiTaiKhoanChoices.CA_NHAN # Đã có default
    )

    # --- Meta class và methods (giữ nguyên) ---
    class Meta:
        ordering = ['-ngay_dang']
        verbose_name = _('Bất động sản')
        verbose_name_plural = _('Bất động sản')

    def __str__(self) -> str:
        return self.tieu_de

    def get_absolute_url(self):
        # --- Sửa thành ---
        return reverse('products:product_detail', kwargs={'id': self.id, 'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug and self.tieu_de: # Chỉ tạo slug nếu chưa có và có tiêu đề
            base_slug = slugify(self.tieu_de) or "bat-dong-san"
            unique_slug = base_slug
            num = 1
            # Đảm bảo slug là duy nhất - Cẩn thận khi có nhiều bản ghi được tạo đồng thời
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    def is_in_user_wishlist(self, user):
        if user.is_authenticated:
            return self.users_wishlist.filter(pk=user.pk).exists()
        return False
        
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images', # Giúp truy cập từ Product: product.images.all()
        on_delete=models.CASCADE,
        verbose_name=_('Bất động sản')
    )
    image = models.ImageField(
        _('Hình ảnh'),
        upload_to='property_images/details/' # Lưu ảnh chi tiết vào thư mục con
    )
    alt_text = models.CharField(
        _('Văn bản thay thế'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Mô tả ngắn về hình ảnh (tốt cho SEO và người dùng khiếm thị)')
    )
    uploaded_at = models.DateTimeField(_('Ngày tải lên'), auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at'] # Sắp xếp theo ngày tải lên
        verbose_name = _('Ảnh chi tiết BĐS')
        verbose_name_plural = _('Ảnh chi tiết BĐS')
        
    def __str__(self):
        return f"Ảnh cho {self.product.tieu_de} ({self.id})"