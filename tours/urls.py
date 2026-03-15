from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tours_list, name='tours_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('details/', views.details_page, name='details_page'),
    path('contact/', views.contact_view, name='contact_page'),
]