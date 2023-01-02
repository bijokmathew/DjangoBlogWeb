from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Posts

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
                'liked': liked
            },
        )


