from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Category, Post, Comment, Author # импортируем нашу модель
from django.core.paginator import Paginator
from .forms import PostForm

class NewsList(ListView):
    model = Post # указываем модель, объекты которой мы будем выводить
    template_name = 'news/news.html' # указываем имя шаблона, в котором будет лежать html, в котором будут все посты
    context_object_name = 'news' # указываем имя переменной, которая будет хранить все объекты
    queryset = Post.objects.order_by('-created_at')
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by('-created_at')
	
class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news_detail'

    def get_queryset(self):
        # Фильтруем объекты Post по свежести и сортируем их по дате публикации в убывающем порядке
        return Post.objects.order_by('-created_at')


def news_search(request):
    #Определить параметры фильтрации на основе get-запроса
    date_filter = request.GET.get('date_filter', None)
    title_filter = request.GET.get('title_filter', None)
    author_filter = request.GET.get('author_filter', None)

    queryset = Post.objects.all()

    if date_filter:
        queryset = queryset.filter(created_at__date=date_filter)
    if title_filter:
        queryset = queryset.filter(title__icontains=title_filter)
    if author_filter:
        queryset = queryset.filter(author__name__icontains=author_filter)

    context = {
        'news': queryset,
        'date_filter': date_filter,
        'title_filter': title_filter,
        'author_filter': author_filter,
    }   
    return render(request, 'news/news_search.html', context)

def news_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PostForm()
    return render(request, 'news/news_add.html', {'form': form})

def news_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
    else:
        form = PostForm(instance=post)
    return render(request, 'news/news_edit.html', {'form': form, 'post': post})

def news_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('news_list')

    return render(request, 'news/news_delete.html', {'post': post})