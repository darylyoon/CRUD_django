from email.policy import HTTP
from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, DeleteBlogPostForm
from accounts.models import Account
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import DeleteView
# Create your views here.

def create_blog_view(request):

    context = {}
    
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
        context['success'] = 'Posted successfully!'

    context['form'] = form

    return render(request, "blog/create_blog.html", context)

def detail_blog_view(request, slug):

    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)

def edit_blog_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    
    blog_post = get_object_or_404(BlogPost, slug = slug)

    if blog_post.author != user:
        return HttpResponse("<h1 align='center'>You are not the owner of the post. <br>RSM help desk has been alerted and your information has been reported to the relevant authorities.<h1>")

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            blog_post = obj
    
    form = UpdateBlogPostForm(
        initial = {
            'title':blog_post.title,
            'body':blog_post.body,
            'image':blog_post.image,
        }
    )

    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))

def delete_blog_view(request, slug):

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    
    blog_post = get_object_or_404(BlogPost, slug = slug)

    if blog_post.author != user:
        return HttpResponse("You are not the owner of the post. RSM help desk has been alerted and your information has been reported to the relevant authorities.")
    
    try:
        if request.method == 'POST':
            form = DeleteBlogPostForm(request.POST, instance = blog_post)
            blog_post.delete()
            return redirect('home')
        else:
            form = DeleteBlogPostForm(instance=blog_post)
    except Exception as e:
        return HTTPResponse('cant')
    
    context = {
        'form' : form,
    }

    return render(request, 'blog/delete_blog.html', context)
