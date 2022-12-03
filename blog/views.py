from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView

# Create your views here.

def post_list(request):
    posts = Post.published.all() #This codes bring all of elements from Database
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})





def post_detail(reqeust,id):
    post = get_object_or_404(Post, #This shortcut
                             id=id,
                             status = Post.Status.PUBLISHED)
    return render(reqeust,'blog/post/detail.html',
                  {'post':post})
