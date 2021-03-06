"""zqxt_views URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from calc import views as calc_views

urlpatterns = [
	path('add/<int:a>/<int:b>/', calc_views.old_add2_redirect),
	path('new_add/<int:a>/<int:b>/', calc_views.add2, name='add2'),
	path('add/', calc_views.add, name='add'),
    path('admin/', admin.site.urls),
    path('', calc_views.index, name='home'),
    path('auth/token', calc_views.create_token, name='token'),
    path('api/get_category', calc_views.get_category, name='getCategory'),
    path('api/get_index/recommand', calc_views.get_index_recommand),
    path('api/get_person', calc_views.get_person),
    path('api/get_personWithoutLogin', calc_views.get_personWithoutLogin),
    path('login', calc_views.login),
    path('api/get_follow', calc_views.get_follow),
    path('api/get_star', calc_views.get_star),
    path('api/changeDesc', calc_views.changeDesc),
    path('api/get_followstatus', calc_views.getFollowStatus),
    path('api/change_followstatus', calc_views.changeFollowStatus),
    path('api/change_starstatus', calc_views.changeStarStatus),
    path('api/get_labeloftag', calc_views.getLabelOfTag),
    path('api/delete_star', calc_views.deleteStar),
    path('api/get_serviceDetail',calc_views.getServiceDetail),
    path('api/get_labelServices',calc_views.getLabelServices),
    path('api/submitTheOrder', calc_views.submitTheOrder),
    path('api/getOrders', calc_views.getOrders),
    path('api/getOrderDetail',calc_views.getOrderDetail),
    path('api/changeOrderStatus', calc_views.changeOrderStatus),
    path('api/deleteTheOrder',calc_views.deleteTheOrder),
    path('api/submitComment', calc_views.submitComment),
    path('api/getComment', calc_views.getComment),
    path('api/getSearchResult', calc_views.getSearchResult),
    path('api/getHotSearch', calc_views.getHotSearch)
]
