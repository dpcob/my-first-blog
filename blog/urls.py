from django.urls import path
from . import views

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('post/<int:pk>/',views.post_detail,name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/wc/', views.post_wc, name='post_wc'),
    path('souun/', views.souun, name='souun'),
    path('souun/new/', views.souun_new, name='souun_new'),
    path('souun/<int:pk>/jdg/', views.jdg_souun, name='jdg_souun'),
    # path('souun/<int:pk>/',views.souun_detail,name='souun_detail'),
]
