from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


#Paginator is used for pages
#EmptyPage is used for no existing or unfill page
#ListView this is generic view,Alternative post list view



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'



def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status= Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url} \n\n" \
                      f"{cd['name']}\`s comments: {cd['comments']}"
            send_mail(subject,message,'erkinovkhumoyun@gmail.com',
                      [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                  'form':form,
                                                  'sent':sent})










# Create your views here.

# def post_list(request):
#     posts = Post.published.all() #This codes bring all of elements from Database
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts':posts})

# def post_list(request):
#     post_list = Post.published.all()
#
#     pagintor = Paginator(post_list,3)
#     page_number = request.GET.get('page')
#     try:
#         posts = pagintor.page(page_number)
#     except PageNotAnInteger:
#         posts = pagintor.page(1)
#     except EmptyPage:
#         posts = pagintor.page(pagintor.num_pages)

#     return render(request,'blog/post/list.html',
#                   {'posts':posts})
#

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
