# Generated by Django 5.1.4 on 2025-04-20 15:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_weight_grams"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["-ngay_dang"],
                "verbose_name": "Bất động sản",
                "verbose_name_plural": "Bất động sản",
            },
        ),
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
        migrations.RemoveField(
            model_name="product",
            name="created",
        ),
        migrations.RemoveField(
            model_name="product",
            name="description",
        ),
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
        migrations.RemoveField(
            model_name="product",
            name="name",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="updated",
        ),
        migrations.RemoveField(
            model_name="product",
            name="weight_grams",
        ),
        migrations.AddField(
            model_name="product",
            name="anh_dai_dien",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="property_images/",
                verbose_name="Ảnh đại diện",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="chieu_dai",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Chiều dài (m)",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="dia_chi",
            field=models.CharField(
                default="Chưa cung cấp", max_length=255, verbose_name="Địa chỉ"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="dien_tich",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="Diện tích (m²)",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="Email liên hệ"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="gia",
            field=models.DecimalField(
                decimal_places=0,
                default=0,
                help_text="Đơn vị: VNĐ",
                max_digits=19,
                verbose_name="Giá",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="huong",
            field=models.CharField(
                blank=True,
                choices=[
                    ("D", "Đông"),
                    ("T", "Tây"),
                    ("N", "Nam"),
                    ("B", "Bắc"),
                    ("DB", "Đông Bắc"),
                    ("DN", "Đông Nam"),
                    ("TB", "Tây Bắc"),
                    ("TN", "Tây Nam"),
                    ("KXD", "Không xác định"),
                ],
                max_length=10,
                null=True,
                verbose_name="Hướng",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="kinh_do",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Kinh độ (Longitude)"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="loai_dat",
            field=models.CharField(
                choices=[
                    ("DO", "Đất ở (Thổ cư)"),
                    ("DNN", "Đất nông nghiệp"),
                    ("DDA", "Đất dự án"),
                    ("DTM", "Đất thương mại dịch vụ"),
                    ("KHAC", "Loại khác"),
                ],
                default="DO",
                max_length=10,
                verbose_name="Loại đất",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="loai_tai_khoan",
            field=models.CharField(
                choices=[("CN", "Cá nhân"), ("MG", "Môi giới"), ("CTY", "Công ty")],
                default="CN",
                max_length=10,
                verbose_name="Loại tài khoản",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="mat_tien",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Mặt tiền (m)",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="mo_ta",
            field=models.TextField(blank=True, verbose_name="Mô tả"),
        ),
        migrations.AddField(
            model_name="product",
            name="ngay_cap_nhat",
            field=models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật"),
        ),
        migrations.AddField(
            model_name="product",
            name="ngay_dang",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Ngày đăng",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="phap_ly",
            field=models.CharField(
                choices=[
                    ("SDSH", "Sổ đỏ/Sổ hồng"),
                    ("HDMB", "Hợp đồng mua bán"),
                    ("VT", "Giấy tờ viết tay"),
                    ("KHAC", "Khác"),
                ],
                default="SDSH",
                max_length=10,
                verbose_name="Pháp lý",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="phuong_xa",
            field=models.CharField(
                default="Chưa rõ", max_length=100, verbose_name="Phường/Xã"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="quan_huyen",
            field=models.CharField(
                default="Chưa rõ", max_length=100, verbose_name="Quận/Huyện"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="so_dien_thoai",
            field=models.CharField(
                default="", max_length=20, verbose_name="Số điện thoại"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="ten_nguoi_ban",
            field=models.CharField(
                default="Chưa rõ", max_length=150, verbose_name="Tên người bán"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="tieu_de",
            field=models.CharField(
                default="Chưa có tiêu đề", max_length=255, verbose_name="Tiêu đề"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="tinh_thanh",
            field=models.CharField(
                default="Chưa rõ", max_length=100, verbose_name="Tỉnh/Thành phố"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="trang_thai",
            field=models.CharField(
                choices=[("CB", "Còn bán"), ("DB", "Đã bán"), ("DC", "Đã đặt cọc")],
                default="CB",
                max_length=10,
                verbose_name="Trạng thái",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="vi_do",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Vĩ độ (Latitude)"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="available",
            field=models.BooleanField(default=True, verbose_name="Còn hiển thị"),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Tự động tạo nếu để trống, dùng cho URL",
                max_length=255,
                null=True,
                unique=True,
            ),
        ),
    ]
