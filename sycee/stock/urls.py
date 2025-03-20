from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('update/', views.update_stock_data, name='update-stock-data'),
]
