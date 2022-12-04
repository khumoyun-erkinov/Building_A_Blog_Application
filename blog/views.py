from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator



# Create your views here.

# def post_list(request):
#     posts = Post.published.all() #This codes bring all of elements from Database
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts':posts})


def post_list(request):
    post_list = Post.published.all()
    pagintor = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    posts = pagintor.page(page_number)
    return render(request,'blog/post/list.html',
                  {'posts':posts})





# def post_detail(reqeust,id):
#     post = get_object_or_404(Post, #This shortcut
#                              id=id,
#                              status = Post.Status.PUBLISHED) ## This code for showing  id
#     return render(reqeust,'blog/post/detail.html',
#                   {'post':post})


def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})
