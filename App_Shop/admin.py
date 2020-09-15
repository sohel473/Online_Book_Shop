from django.contrib import admin
from App_Shop.models import Category, Author, Publisher, Product, Comment, Likes
# Register your models here.

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Likes)
