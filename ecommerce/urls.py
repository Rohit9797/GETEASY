"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from ecommapp import views

urlpatterns =[

    path('admin/', admin.site.urls),
    path('',views.home),
    #path('',include('ecommapp.urls')),

    path('home',views.home),#edited index=home

    path('delete/<rid>',views.delete),
    path('edit,/<rid>',views.edit),
    path('addition/<x>/<y>',views.addition),
    path('signup',views.user_register),
    path('productlist',views.product_list),
    path('base',views.reuse),
    #path('login',views.login),
    #path('signup',views.signup),
    path('sort/<sv>',views.sort),
    path('catfilter/<catv>',views.catfilter),
    path('pricefilter/<pv>',views.pricefilter),
    path('pricerange',views.pricerange),
    path('pdetails/<pid>',views.product_details),
    path('addproduct',views.addproduct),
    path('delproduct/<rid>',views.delproduct),
    path('djangoform',views.djangoform),
    path('modelform',views.modelform),
    #path('register',views.user_register),
    path('login',views.user_login),
    path('setsession',views.setsession),
    path('getsession',views.getsession),
    path('cart/<pid>',views.addtocart),
    path('logout',views.user_logout),
    path('viewcart',views.viewcart),
    path('changeqty/<pid>/<f>',views.changeqty),
    path('placeorder',views.placeorder),
    path('payment',views.makepayment),
    path('store',views.storedetails),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)