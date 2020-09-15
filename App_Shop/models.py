from django.db import models
from django.conf import settings
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Author(models.Model):
    name = models.CharField(max_length=264, blank=True)
    description = models.TextField(
        max_length=1000, verbose_name='Description', blank=True)
    isMVP = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return str(self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=264, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    mainimage = models.ImageField(upload_to='products')
    name = models.CharField(max_length=264)
    isPublished = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name='publisher')
    authors = models.ManyToManyField(Author, related_name='authors')
    description = models.TextField(max_length=2000, verbose_name='Description')
    page_no = models.IntegerField(default=1)
    date_published = models.IntegerField(default=0)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_comment')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('comment_date',)

    def __str__(self):
        return self.comment


class Likes(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='liked_product')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liker_user')

    def __str__(self):
        return self.user + " likes " + self.blog

    class Meta:
        verbose_name_plural = "Likes"
