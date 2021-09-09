from django.urls import path
from shortme import views

urlpatterns = [
    path('', views.ShortenUrlList.as_view(), name='main'),
    path('api/<str:short_url_part>/', views.ShortenUrlListApiDetail.as_view(), name='api-modif'),
    path('api/', views.ShortenUrlListApi.as_view(), name='api'),
    path('<str:short_url>/', views.visit_world, name='redirector')
]
