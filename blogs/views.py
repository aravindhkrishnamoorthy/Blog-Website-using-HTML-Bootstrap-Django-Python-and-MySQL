from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Blog, Category
from django.db.models import Q

# Create your views here.

def posts_by_category(request, category_id):
    # fetch the post that belongs to the category with the id category
    posts = Blog.objects.filter(status='Published', category=category_id)
    # cat = Category.objects.all() this is already done in get_catogoires(views) so i 
    # used context processors
    
    # use try/except when we want some custom action if the category does not exist
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     # return redirect('home')
    #     pass   
    
    # use get_object_or_404 when you want to show the error page if the category does not exist
    category = get_object_or_404(Category, pk=category_id)
    context = {
        # "categories": cat,
        "posts": posts,
        "category": category,
    }
    return render(request, 'posts_by_category.html', context)


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        "single_blog": single_blog,
    }
    return render(request, 'blogs.html', context)

def search(request):
    search = request.GET.get('keyword')
    print(search)
    blogs = Blog.objects.filter(Q(title__icontains=search) | Q(short_description__icontains=search) | 
                                  Q(blog_body__icontains=search), status='Published')
    context = {
        'blogs':blogs,
        'keyword': search,
    }
    return render(request, 'search.html', context)