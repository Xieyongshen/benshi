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
    path('login', calc_views.login),
    path('api/get_follow', calc_views.get_follow),
    path('api/get_star', calc_views.get_star),
]
