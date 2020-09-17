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

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list


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
            print(request.user)
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
def edit_comment(request, pk1, pk2):
    product = get_object_or_404(Product, pk=pk1)
    comment = get_object_or_404(Comment, pk=pk2)
    print(comment)
    form = CommentForm(instance=comment)
    if request.method == "POST":
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            form = CommentForm(instance=comment)
            return HttpResponseRedirect(reverse_lazy('App_Shop:product_detail', kwargs={'pk': pk1}))
    return render(request, 'App_Shop/edit_comment.html', context={'form': form, 'product': product})


class WritersList(ListView):
    model = Author
    template_name = 'App_Shop/writers.html'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'App_Shop/Author.html'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'App_Shop/Category.html'


class PublisherDetail(DetailView):
    model = Publisher
    template_name = 'App_Shop/Publisher.html'
