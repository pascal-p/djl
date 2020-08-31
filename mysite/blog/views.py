from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm


## CBV
class PostListView(ListView):
    queryset = Post.objects.all() # queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'

    def get(self, request, year, month, day, post):
        post_obj = get_object_or_404(Post, slug=post,
                                     # status='published',
                                     publish__year=year,
                                     publish__month=month,
                                     publish__day=day)
        # context = { 'ad' : ad_obj, 'comments': comments, 'comment_form': comment_form }
        context = { 'post': post_obj }
        return render(request, self.template_name, context)


## FBV
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


## Helper
def send_email_hlpr(request, post, cd):
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{cd['name']} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n" \
              f"{cd['name']}\'s comments: {cd['comments']}"
    send_mail(subject, message, 'toor@blog.org', [cd['to']])
    return
