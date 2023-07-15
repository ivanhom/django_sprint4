from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone


from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Comment, Post, User
from blogicum.settings import PER_PAGE


def index(request):
    """Главная страница. Список публикаций."""
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    paginator = Paginator(post_list, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


@login_required
def create_post(request):
    """Создание новой публикации."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    context = {'form': form}
    if form.is_valid():
        form.save(commit=False)
        form.instance.author = request.user
        form.save()
        return redirect('blog:profile', username=request.user)
    return render(request, 'blog/create.html', context)


def post_detail(request, post_id):
    """Страница публикации."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        post = get_object_or_404(
            Post,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
            pk=post_id
        )
    form = CommentForm()
    comments = post.comments.all()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)


@login_required
def edit_post(request, post_id):
    """Редактирование публикации."""
    is_edit = True
    instance = get_object_or_404(Post, pk=post_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form, 'is_edit': is_edit}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    """Удаление публикации."""
    is_delete = True
    instance = get_object_or_404(Post, pk=post_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(instance=instance)
    context = {'form': form, 'is_delete': is_delete}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    """Добавление комментария к публикации."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария к публикации."""
    is_edit = True
    instance = get_object_or_404(Comment, post=post_id, pk=comment_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(
        request.POST or None,
        instance=instance
    )
    context = {'comment': instance, 'form': form, 'is_edit': is_edit}
    if form.is_valid():
        form.save()
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария к публикации."""
    is_delete = True
    instance = get_object_or_404(Comment, post=post_id, pk=comment_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id=post_id)
    context = {'comment': instance, 'is_delete': is_delete}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/comment.html', context)


def profile(request, username):
    """Страница профиля пользователя."""
    profile = get_object_or_404(User, username=username)
    post_list = profile.posts.all()
    if request.user.username != username:
        post_list = post_list.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    paginator = Paginator(post_list, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование информации профиля пользователя."""
    instance = get_object_or_404(User, username=request.user)
    if request.user.username != instance.username:
        return redirect('blog:index')
    form = UserForm(
        request.POST or None,
        instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)


def category_posts(request, category_slug):
    """Список публикаций в выбранной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    paginator = Paginator(post_list, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)
