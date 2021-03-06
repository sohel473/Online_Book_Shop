from django.urls import path
from App_Shop import views

app_name = 'App_Shop'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('product/<pk>/comment/', views.create_comment, name='comment'),
    path('product/<pk1>/update_comment/<pk2>',
         views.edit_comment, name='update_comment'),
    path('author/<pk>', views.AuthorDetail.as_view(), name='author'),
    path('category/<pk>', views.CategoryDetail.as_view(), name='category'),
    path('publisher/<pk>', views.PublisherDetail.as_view(), name='publisher'),
    path('writers/', views.WritersList.as_view(), name='writers'),
]
