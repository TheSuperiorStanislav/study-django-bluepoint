from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from django.shortcuts import render

from .forms import BlogForm, BlogPostForm
from .models import Blog, BlogPost
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if Blog.objects.filter(owner = user).exists():
                ctx['has_blog'] = True
                blog = Blog.objects.get(owner = user)
                ctx['blog'] = blog
                ctx['blog_post'] = BlogPost.objects.filter(blog = blog)
        return ctx

class NewBlogView(CreateView):
    form_class = BlogForm
    template_name = 'blog_settings.html'

    def form_valid(self, form):
        blog_obj = form.save(commit = False)
        blog_obj.owner = self.request.user
        blog_obj.slug = slugify(blog_obj.title)

        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if Blog.objects.filter(owner = user).exists():
            return HttpResponseForbidden('You can create only one blog per account!')
        return super(NewBlogView,self).dispatch(request, *args, **kwargs)

class UpdateBlogView(UpdateView):
    form_class = BlogForm
    template_name = 'blog_settings.html'
    success_url = '/'
    model = Blog
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogView,self).dispatch(request, *args, **kwargs)


class NewBlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = 'blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewBlogPostView,self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog_obj = form.save(commit = False)
        blog_obj.blog = Blog.objects.get(owner = self.request.user)
        blog_obj.slug = slugify(blog_obj.title)
        blog_obj.is_published = True

        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))
    
class UpdateBlogPostView(UpdateView):
    form_class = BlogPostForm
    template_name = 'blog_post.html'
    success_url = '/'
    model = BlogPost
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogPostView,self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(UpdateBlogPostView, self).get_queryset()
        return queryset.filter(blog_owner = self.request.user)
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_details.html'

