from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm

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