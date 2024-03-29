# blog views
from django.shortcuts import render , redirect , get_object_or_404
from .models import Post , PostComment , PostLikes
from .forms import PostForm , PostCommentForm
from django.views.generic import CreateView , UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse , reverse_lazy
from django.db.models import Q

# Create your views here.

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request , 'blog/index.html' , {'posts':posts} )


@login_required
def detail_post(request , pk):
    post = Post.objects.get(id=pk)
    user_has_liked = PostLikes.objects.filter(user=request.user , post=post)
    comments = PostComment.objects.filter(post=post)
    # add a new comment to the post from the same view 
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    
    context = {'post':post , 'form':PostCommentForm() , 'comments':comments , 'user_has_liked':user_has_liked}
    return render(request , 'blog/post.html' , context)

class CreatePost(LoginRequiredMixin , CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create-post.html'

    def form_valid(self, form):
        post = form.save(commit=False)   
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(reverse_lazy('blog:b-home'))
    

class UpdatePost(LoginRequiredMixin , UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update-post.html'

    def get_success_url(self):
        return reverse_lazy('blog:b-post' , kwargs={'pk':self.kwargs['pk']})

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
    

@login_required   
def delete_post(request , pk):
    post = Post.objects.filter(Q(author=request.user) & Q(id=pk))
    post.delete()
    return redirect('blog:b-home')


@login_required
def delete_comment(request , pk):
    comment = PostComment.objects.get(Q(author=request.user) & Q(id=pk))
    pk = comment.post.id
    comment.delete()
    return redirect(reverse('blog:b-post' , kwargs={'pk':pk}))


@login_required
def like_post(request , pk):
    post = get_object_or_404(Post , id=pk)
    user = request.user
    
    if PostLikes.objects.filter(post=post , user=user).exists(): # then remove the like
        PostLikes.objects.filter(post=post , user=user).delete()
    else: # else like
        PostLikes.objects.create(user=user, post=post)

    return redirect(reverse('blog:b-post' , kwargs={'pk':pk}))
