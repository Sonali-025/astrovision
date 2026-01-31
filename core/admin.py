from django.contrib import admin
from .models import ConsultationOrder, KundaliRequest


@admin.register(ConsultationOrder)
class ConsultationOrderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "service",
        "dob",
        "tob",
        "pob",
        "amount",
        "payment_status",
        "razorpay_payment_id",
        "astrologer",
        "created_at",
    )

    list_filter = (
        "service",
        "payment_status",
        "astrologer",
    )

    search_fields = (
        "name",
        "phone",
        "razorpay_payment_id",
        "razorpay_order_id",
    )

    ordering = ("-created_at",)


@admin.register(KundaliRequest)
class KundaliRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "whatsapp",
        "purpose",
        "created_at",
    )

    list_filter = ("purpose",)
    search_fields = ("full_name", "whatsapp")
    ordering = ("-created_at",)
