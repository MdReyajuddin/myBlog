from django.shortcuts import render, get_object_or_404, reverse ,redirect
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Author, Category, PostView
from .forms import CommentForm, PostForm

from marketing.models import Signup

# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists:
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.POST.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(overview__icontains=query)
        ).distinct()
    context ={
        'queryset': queryset,
    }
    return render(request, 'result_search.html', context)


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method=='POST':
        email = request.POST['email']
        new_signup=Signup()
        new_signup.email = email
        new_signup.save()

    context ={
        'object_list': featured,
        'latest': latest,
        }
    return render(request, 'index.html', context)

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def blog(request):
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    page_request_var = 'page'
    page= request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        'latest': latest,
        'queryset': queryset,
        'category_count': category_count,
        'page_request_var': page_request_var,
    }

    return render(request, 'blog.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    post.view_count +=1
    post.save()
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[:3]

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post', kwargs={'id': post.id}))

    context ={
        'post': post,
        'category_count': category_count,
        'latest': latest,
        'form': form,
    }
    return render(request, 'post.html', context)



def contact(request):
    return render(request, 'contact.html')

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method=='POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={'id': form.instance.id}))

    context={
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)

def post_update(request, id):
    title = 'Update'
    user= get_author(request.user)
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = user
            form.save()
            return redirect(reverse('post', kwargs={'id': form.instance.id}))

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)


def post_delete(request, id):
    post= get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('blog'))