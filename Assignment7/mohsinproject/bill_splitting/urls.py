from django.urls import path
from . import views

urlpatterns = [
    path('split_evenly/', views.split_evenly, name='split_evenly'),
    path('split_unevenly/', views.split_unevenly, name='split_unevenly'),
    path('split_evenly_include_tip_tax/', views.split_evenly_include_tip_tax, name='split_evenly_include_tip_tax'),
    path('split_evenly_include_discount/', views.split_evenly_include_discount, name='split_evenly_include_discount'),
    path('split_include_shared_items/', views.split_include_shared_items, name='split_include_shared_items'),
]