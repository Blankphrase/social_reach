from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.CreatorSignupView.as_view(), name='creators_signup'),
    path('profile/edit/<pk>/', views.CreatorUpdateView.as_view(), name='profile_edit'),
    path('platform/create/', views.platform_create, name='platform_create'),
    path('platform/update/<pk>/', views.PlatformUpdateView.as_view(), name='platform_update'),
    path('platform/delete/<pk>/', views.PlatformDeleteView.as_view(), name='platform_delete'),
    path('quote/create/<pk>/', views.quote_create, name='quote_create'),
    path('quote/update/<pk>/', views.QuoteUpdateView.as_view(), name='quote_update'),
    path('quote/delete/<pk>/', views.QuoteDeleteView.as_view(), name='quote_delete'),
]
