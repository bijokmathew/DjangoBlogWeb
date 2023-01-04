from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import Posts, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.


def get_base(request):
    return render(request, 'index.html')


class PostList(generic.ListView):
    model = Posts
    queryset = Posts.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5


class PostDetails(View):
    def get(self, request, slug, *args, **kwargs):
        query_post = Posts.objects.filter(status=1)
        post = get_object_or_404(query_post, slug=slug)
        comments = post.comment.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        messages.add_message(request, messages.INFO, request.user.username + "  added the comment successfully")
        query_post = Posts.objects.filter(status=1)
        post = get_object_or_404(query_post, slug=slug)
        comment_all = post.comment.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        form_data = CommentForm(data=request.POST)
        if form_data.is_valid():
            form_data.instance.email = request.user.email
            form_data.instance.name = request.user.username
            comment = form_data.save(commit=False)
            comment.post = post
            comment.save()                    
        else:
            form_data = CommentForm()
            print(" CommentForm") 
            
        return render(
                request, 
                'post_detail.html', 
                {
                    'liked': liked,
                    'comments': comment_all,
                    'commented': True,
                    'post': post,
                    'comment_form': CommentForm()
                }
            )


class PostLike(View):
    def post(self, request, slug):
        # posts = Posts.objects.filter(status=1)
        post = get_object_or_404(Posts, slug=slug)
        if post.likes.filter(id=self.request.user.id).exists():
            post.likes.remove(self.request.user)
        else:
            post.likes.add(self.request.user)

        return HttpResponseRedirect(reverse("post_detail", args=[slug]))