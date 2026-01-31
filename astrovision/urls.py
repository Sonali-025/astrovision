"""
URL configuration for astrovision project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),

    #pages
    path("", views.home, name="home"),
    path("kundali/", views.kundali, name="kundali"),

    # Razorpay APIs
    path("create-order/", views.create_order, name="create_order"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("confirm-booking/", views.confirm_booking, name="confirm_booking"),

    # Free Kundali
    path("submit-kundali/", views.submit_kundali, name="submit_kundali"),
    path("kundali-success/", views.kundali_success),


      # Payment result pages
    path("payment-success/", views.payment_success),
    path("payment-failed/", views.payment_failed),
    
]




