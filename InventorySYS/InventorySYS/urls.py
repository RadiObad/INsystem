"""InventorySYS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from inventory import views as my_order
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from inventory.views import HomeView, get_data, ChartData

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', my_order.home, name='homen'), #when the sys run(defulate url)    
    url(r'^test/$', my_order.product_list, name='test'),
    url(r'^orders$', my_order.index, name='home'),
    url(r'^order/(?P<order_id>\d+)/$', my_order.show, name='show'),
    url(r'^order/new/$', my_order.add_new, name='new'),
    url(r'^order/edit/(?P<order_id>\d+)/$', my_order.edit, name='edit'),
    url(r'^order/delete/(?P<order_id>\d+)/$', my_order.destroy, name='delete'),
    url(r'^products$', my_order.index_product, name='home_product'),
    url(r'^product/new/$', my_order.new_product, name='new_product'),
    url(r'^category/new/$',my_order.new_category,name='new_category'),
    url(r'^product/delete/(?P<product_id>\d+)/$', my_order.destroy_product, name='delete_product'),
    url(r'^users/login/$', auth.login, {'template_name': 'login.html'}, name='login'),
    url(r'^users/logout/$', auth.logout, {'next_page': '/'}, name='logout'),
    url(r'^users/change_password/$', login_required(auth.password_change), {'post_change_redirect' : '/','template_name': 'change_password.html'}, name='change_password'),
    url(r'^add/(?P<product_id>\d+)/$',my_order.cart_add,name='cart_add'),
    url(r'^cards/$',my_order.cart_detail, name='cart_detail'),
    url(r'^remove/(?P<product_id>\d+)/$',my_order.cart_remove,name='cart_remove'),
    url(r'^remove/$',my_order.cart_remove_all,name='cart_remove_all'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',my_order.product_detail,name='product_detail'),
    url(r'^create/$',my_order.order_create,name='order_create'),
    url(r'^orders/(?P<order_id>\d+)/$', my_order.order_detils, name='order_detils'),
    url(r'^api/nome/$', HomeView.as_view(), name='nome'),    
    url(r'^api/data/$', get_data, name='api-data'),
    url(r'^api/chart/nome/$', ChartData.as_view()),


]
