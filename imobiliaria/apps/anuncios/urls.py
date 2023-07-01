from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AnuncioViewSet, basename='anuncio')
router.register(r'plataformas', views.PlataformaAnuncioViewSet, basename='plataforma')

urlpatterns = [
    path('', include(router.urls)),
]