from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home, about  # import home & about views

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('accounts/', include('accounts.urls')),  # your custom account views
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('about/', about, name='about'),  # about page
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
