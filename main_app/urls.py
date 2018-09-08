from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('campaigns/explore', views.CampaignListView.as_view(), name='campaigns_list'),
    path('campaigns/<pk>', views.CampaignDetailView.as_view(), name='campaigns_detail'),
    path('influencer', views.influencer_view, name='influencer_view')
]
