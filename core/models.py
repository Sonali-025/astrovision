from django.db import models


# =========================================
# 🔐 PAID CONSULTATION BOOKINGS (RAZORPAY)
# =========================================
class ConsultationOrder(models.Model):
    # User details
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    tob = models.TimeField(null=True, blank=True)
    pob = models.CharField(max_length=255, blank=True)

    # Razorpay details
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255)
    razorpay_signature = models.CharField(max_length=255)

    # Payment info
    amount = models.IntegerField(help_text="Amount in INR")
    payment_status = models.CharField(
        max_length=20,
        default="PAID",
        help_text="PAID / FAILED"
    )

    # Business logic
    astrologer = models.CharField(max_length=255)

    # Auto timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Paid Consultation"
        verbose_name_plural = "Paid Consultations"

    def __str__(self):
        return f"{self.name} | {self.service} | ₹{self.amount}"


# =========================================
# 🕉️ FREE KUNDALI REQUEST (NO PAYMENT)
# =========================================
class KundaliRequest(models.Model):
    full_name = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15)

    dob = models.DateField()
    tob = models.TimeField()
    pob = models.CharField(max_length=100)

    gender = models.CharField(max_length=10)
    purpose = models.CharField(max_length=100)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Free Kundali Request"
        verbose_name_plural = "Free Kundali Requests"

    def __str__(self):
        return f"Kundali | {self.full_name}"
