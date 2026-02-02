from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
import json
import razorpay
import logging

from .models import ConsultationOrder, KundaliRequest

# ===============================
# RAZORPAY CLIENT
# ===============================
razorpay_client = razorpay.Client(auth=(
    settings.RAZORPAY_KEY_ID,
    settings.RAZORPAY_KEY_SECRET
))

# ===============================
# SERVICE PRICE LIST (₹ INR)
# ===============================
SERVICE_PRICES = {
    "Tarot Reading": 501,
    "Tarot Guidance (Combined)": 501,
    "Yes / No Answers": 101,
    "Angel Guidance (Combined)": 501,
    "Angel Oracle Reading": 501,
    "Akashic Record Reading": 2999,
    "Tarot + Angel Overall Package": 999,

    "Kundali Analysis": 251,
    "Palm Reading": 251,
    "Numerology": 251,
    "Spritiual Guidance": 251,
    "Vastu Consultation": 251,
}

TAROT_SERVICES = [
    "Tarot Reading",
    "Tarot Guidance (Combined)",
    "Yes / No Answers",
    "Angel Guidance (Combined)",
    "Angel Oracle Reading",
    "Tarot + Angel Overall Package",
]

NAYANA_EMAIL = "mausam089@gmail.com"
MAYANK_EMAIL = "aiastrovision@gmail.com"
BUSINESS_EMAIL = "aiastrovision@gmail.com"

# ===============================
# PAGE RENDERS
# ===============================
def home(request):
    return render(request, "index.html", {
        "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID
    })


def kundali(request):
    return render(request, "kundali.html")


def payment_success(request):
    return render(request, "payment_success.html")


def payment_failed(request):
    return render(request, "payment_failed.html")


def kundali_success(request):
    return render(request, "kundali_success.html")


# ===============================
# CREATE RAZORPAY ORDER
# ===============================
@require_POST
@csrf_exempt
def create_order(request):
    amount = int(request.POST.get("amount", 0))
    if amount <= 0:
        return JsonResponse({"error": "Invalid amount"}, status=400)

    order = razorpay_client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "id": order["id"],
        "amount": order["amount"]
    })

# ===============================
# VERIFY PAYMENT
# ===============================
@require_POST
@csrf_protect
def verify_payment(request):
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": request.POST["razorpay_order_id"],
            "razorpay_payment_id": request.POST["razorpay_payment_id"],
            "razorpay_signature": request.POST["razorpay_signature"],
        })
        return JsonResponse({"status": "success"})
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"status": "failed"}, status=400)

# ===============================
# CONFIRM BOOKING (SAVE + EMAIL)
# ===============================
@require_POST
@csrf_protect
def confirm_booking(request):
    name = request.POST["name"]
    phone = request.POST["phone"]
    service = request.POST["service"]
    message = request.POST.get("message", "")
    dob = request.POST.get("dob")
    tob = request.POST.get("tob")
    pob = request.POST.get("pob")

    amount = int(request.POST["amount"])

    razorpay_order_id = request.POST["razorpay_order_id"]
    payment_id = request.POST["payment_id"]
    razorpay_signature = request.POST["razorpay_signature"]

    if service in TAROT_SERVICES:
        astrologer = "Ms. Nayana Dey"
        admin_email = NAYANA_EMAIL
    else:
        astrologer = "Mr. Mayank Vijay Kanth"
        admin_email = MAYANK_EMAIL

    ConsultationOrder.objects.create(
        name=name,
        phone=phone,
        service=service,
        message=message,
        dob=dob,
        tob=tob,
        pob=pob,
        razorpay_order_id=razorpay_order_id,
        payment_id=payment_id,
        razorpay_signature=razorpay_signature,
        amount=amount,
        payment_status="PAID",
        astrologer=astrologer
    )

    # 🔐 SAFE EMAIL (Railway-safe)
    if settings.EMAIL_ENABLED:
        try:
            send_mail(
                "New Paid Consultation - AstroVision",
                f"""
Name: {name}
Phone: {phone}
DOB: {dob}
TOB: {tob}
POB: {pob}
Service: {service}
Amount: ₹{amount}

Payment ID: {payment_id}
Order ID: {razorpay_order_id}

Message:
{message}
""",
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=True
            )
        except Exception as e:
            print("Paid email skipped:", e)

    return JsonResponse({"status": "success"})


# ===============================
# FREE KUNDALI REQUEST
# ===============================
@csrf_exempt
def submit_kundali(request):
    if request.method == "POST":
        data = json.loads(request.body)

        KundaliRequest.objects.create(
            full_name=data["full_name"],
            whatsapp=data["whatsapp"],
            dob=data["dob"],
            tob=data["tob"],
            pob=data["pob"],
            gender=data["gender"],
            purpose=data["purpose"],
            message=data.get("message", "")
        )

        # 🔐 SAFE EMAIL (Railway-safe)
        if settings.EMAIL_ENABLED:
            try:
                send_mail(
                    "New FREE Kundali Request - AstroVision",
                    f"""
Name: {data['full_name']}
WhatsApp: {data['whatsapp']}
DOB: {data['dob']}
TOB: {data['tob']}
POB: {data['pob']}
Gender: {data['gender']}
Purpose: {data['purpose']}

Message:
{data.get('message', '')}
""",
                    settings.DEFAULT_FROM_EMAIL,
                    [MAYANK_EMAIL],
                    fail_silently=True
                )
            except Exception as e:
                print("Kundali email skipped:", e)

        return JsonResponse({"status": "success"})

