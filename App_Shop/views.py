from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy

# Import views
from django.views.generic import ListView, DetailView, UpdateView

# Models
from App_Shop.models import Product, Author, Category, Publisher, Comment, Likes
from App_Login.models import Profile

# Forms
from App_Shop.forms import CommentForm

# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Decorator
from django.contrib.auth.decorators import login_required

# Create your views here.


class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'App_Shop/product_detail.html'


@login_required
def create_comment(request, pk):
    product = Product.objects.get(pk=pk)
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('App_Shop:product_detail', pk=pk)

    dict = {
        'product': product,
        'comment_form': comment_form
    }
    return render(request, 'App_Shop/comment_form.html', context=dict)


@login_required
def edit_comment(request, pk):
    current_user = Profile.objects.get(user=request.user)
    product = get_object_or_404(Product, pk=pk)
    print(current_user)
    form = CommentForm(instance=product)
    if request.method == "POST":
        form = CommentForm(data=request.POST, instance=product)
        if form.is_valid():
            comment = form.save()
            form = CommentForm(instance=product)
            return HttpResponseRedirect(reverse_lazy('App_Shop:product_detail', kwargs={'pk': pk}))
    return render(request, 'App_Shop/edit_comment.html', context={'form': form})


class WritersList(ListView):
    model = Author
    template_name = 'App_Shop/writers.html'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'App_Shop/author.html'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'App_Shop/Category.html'


class PublisherDetail(DetailView):
    model = Publisher
    template_name = 'App_Shop/Publisher.html'
