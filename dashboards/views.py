from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogPostForm
from django.template.defaultfilters import slugify

@login_required(login_url='login')
def dashboard(request):
    category_conut = Category.objects.all().count()
    blog_count = Blog.objects.all().count()
    context = {
        'category_count': category_conut,
        'blog_count': blog_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/categories.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['category_name']
            if not Category.objects.filter(category_name=name).exists():
                form.save()
                return redirect('categories')
            else:
                form.add_error('category_name', 'Category_already_exists')
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_category.html', context)

def edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            name = form.cleaned_data['category_name']
            if not Category.objects.filter(category_name=name).exists():
                form.save()
                return redirect('categories')
            else:
                form.add_error('category_name', 'Category_Already_Exists')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    category = Category.objects.filter(pk=pk)
    category.delete()
    return redirect('categories')


def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'dashboard/posts.html', context)

def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) #temporarily saving the form
            post.author = request.user
            post.save()  #save to get the id
            title = form.cleaned_data['title']
            post.slug = slugify(title)+ '-'+str(post.id) 
            post.save()
            return redirect('posts')
        else:
            print('error hapeening')
            print(form.errors)
    form = BlogPostForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_post.html', context)

def edit_post(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)+'-'+str(post.id)
            post.save()
            return redirect('posts')
    
    form = BlogPostForm(instance=blog)
    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request, pk):
    post = Blog.objects.get(pk=pk)
    post.delete()
    return redirect('posts')