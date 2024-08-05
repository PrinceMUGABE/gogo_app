
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userApp.urls')),
    path('vehicle/', include('vehicleApp.urls')),
    path('freelancer/', include('freelancerApp.urls')),
    path('order/', include('orderApp.urls')),
    path('application/', include('orderApplicationApp.urls')),
    path('discount/', include('discountApp.urls')),
    path('tracking/', include('trackingApp.urls')),
    path('company/', include('logistic_company.urls')),
    path('payment/', include('payment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)