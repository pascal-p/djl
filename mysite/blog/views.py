from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.author import AuthorListView, AuthorDetailView, AuthorCreateView, AuthorUpdateView, AuthorDeleteView

from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import TrigramSimilarity

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


## CBV
class PostListView(AuthorListView):
    template_name = 'blog/post/list.html'

    def get(self, request, tag_slug=None):
        queryset = Post.published.all()
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])

        paginator = Paginator(queryset, 3)               ## 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)

        except PageNotAnInteger:
            posts = paginator.page(1)                    ## If page is not an integer deliver the first page

        except EmptyPage:
            posts = paginator.page(paginator.num_pages)  ## If page is out of range deliver last page of results

        return render(request, 'blog/post/list.html',
                      {'page': page, 'posts': posts, 'tag': tag})


class PostDetailView(AuthorDetailView):
    model = Post
    template_name = 'blog/post/detail.html'

    def get(self, request, year, month, day, post):
        post, comments = self._get_qs_hlpr(request, year, month, day, post)
        comment_form = CommentForm()                       ## Assume a get request, send inital empty form to fill

        # similar posts by tags - limited to 4
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)\
                                                                     .annotate(same_tags=Count('tags'))\
                                                                     .order_by('-same_tags','-publish')[:4]

        context = {'post': post, 'comments': comments, 'new_comment': None,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts}
        return render(request, 'blog/post/detail.html', context)

    def post(self, request, year, month, day, post):
        post, comments = self._get_qs_hlpr(request, year, month, day, post)
        new_comment = None
        if request.method == 'POST':                           ## A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)  ## Create Comment object but don't save to database yet
                new_comment.post = post                        ## Assign the current post to the comment
                new_comment.save()                             ## Save the comment to the database

        context = {'post': post, 'comments': comments, 'new_comment': new_comment,
                   'comment_form': comment_form}
        return render(request, 'blog/post/detail.html', context)


    def _get_qs_hlpr(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month, publish__day=day)

        # List of active comments for this post
        comments = post.comments.filter(active=True)
        return (post, comments)


class PostCreate(AuthorCreateView):
    model = Post
    template_name = 'blog/post/form.html'
    fields = ['title', 'slug', 'body', 'status', 'publish', 'tags']
    success_url = reverse_lazy('blog:post_list')

class PostUpdate(AuthorUpdateView):
    model = Post
    template_name = 'blog/post/form.html'
    fields = ['title', 'slug', 'body', 'status', 'publish', 'tags']
    success_url = reverse_lazy('blog:post_list')

class PostDelete(AuthorDeleteView):
    model = Post
    template_name = 'blog/post/confirm_delete.html'
    fields = ['title', 'slug', 'body', 'status', 'publish'], 'tags'
    success_url = reverse_lazy('blog:post_list')

## FBV
@login_required
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():         # form valid?
            cd = form.cleaned_data  # yes, clean up data...
            send_email_hlpr(request, post, cd)
            sent = True
    else:
        # assume a get - send empty form to user to fill up
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form,
                                                    'sent': sent})

@login_required
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Post.published.annotate(
               similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'blog/post/search.html',
                  {'form': form, 'query': query, 'results': results})

## Helper
def send_email_hlpr(request, post, cd):
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{cd['name']} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n" \
              f"{cd['name']}\'s comments: {cd['comments']}"
    send_mail(subject, message, 'toor@blog.org', [cd['to']])
    return
