from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm,SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector




#Paginator is used for pages
#EmptyPage is used for no existing or unfill page
#ListView this is generic view,Alternative post list view
#flat = You pass flat=True to it to get single values,
# such as [1, 2, 3, ...] instead of one-tuples such as [(1,), (2,), (3,) ...].
#django-taggit also includesa similar_objects() manager that you can use to retrieve objects by shared tags. You can take a look
#at all django-taggit managers at




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


@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False) #bu saqlamaydi databesga chunki false belgilangan
        comment.post = post
        comment.save()
    return render(request,'blog/post/comment.html',
                  {'post':post,
                   'form':form,
                   'comment':comment
                   })











# Create your views here.

# def post_list(request):
#     posts = Post.published.all() #This codes bring all of elements from Database
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts':posts})

def post_list(request,tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tag__in=[tag])


    pagintor = Paginator(post_list,3)
    page_number = request.GET.get('page')
    try:
        posts = pagintor.page(page_number)
    except PageNotAnInteger:
        posts = pagintor.page(1)
    except EmptyPage:
        posts = pagintor.page(pagintor.num_pages)

    return render(request,'blog/post/list.html',
                  {'posts':posts,
                   'tag':tag})


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
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]




    return render(request,
                  'blog/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   'form':form,
                   'similar_posts':similar_posts})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search = SearchForm('title','body'),
            ).filter(search=query)
    return render(request,
                  'blog/post/search.html',
                  {'form':form,
                   'query':query,
                   'results':results})




#137-page


