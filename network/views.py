from django.shortcuts import render
from .forms import Registration,AddPost
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import FileUploadForm
from django.urls import reverse_lazy
from .models import Post, Comment, Like, User
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import request
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
import json
from django.shortcuts import get_object_or_404, redirect
# Create your views here.

class RegistrationView(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'



    def get_queryset(self):
        # Отримання поточного користувача
        user = self.request.user

        # Фільтрація постів за користувачем
        queryset = super().get_queryset().filter(user=user)

        return queryset  
       

class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class LogoutPage(LogoutView):
    pass



class CreatePostView(CreateView):
    model = Post
    form_class = AddPost
    template_name = 'post.html'
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

   
# class PostView(TemplateView):
#     template_name = 'posts.html'

#     def post(self, request,**kwargs):
#         data = request.POST
#         user = self.request.user
#         post = Post.objects.get(id=self.kwargs['pk'])
#     success_url = reverse_lazy('home')

# class Profile(UpdateView):
#     form_class = FileUploadForm
#     template_name= 'profile.html'
#     model = User
    
#     def form_valid(self, form,**kwargs):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
#     success_url = reverse_lazy('profile', kwargs={'pk': pk})

class Profile(UpdateView):
    # form_class = FileUploadForm
    fields = ['avatar']
    template_name = 'profile.html'
    model = User
    
    
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)
    
    def get_success_url(self):
        return (f'/home/profile/{self.kwargs["pk"]}')
    

class BbDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'index.html'
   

   


class ToggleLikeView(View):
    def post(self, request, **kwargs):
        data = request.POST
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])

        if 'text' in data.keys():
            comment = Comment(user=user, post=post, body=data['text'])
            comment.save()
            result = render_to_string('comment.html', {'user': user, 'comment': comment})
            return JsonResponse(result, safe=False)

        if 'like' in data.keys():
            try:
                like = Like.objects.get(user=user, post=post)
                like.delete()
                is_like = False
            except Like.DoesNotExist:
                like = Like(user=user, post=post)
                like.save()
                is_like = True

            like_count = Like.objects.filter(post=post).count()
            return JsonResponse({'like_count': like_count, 'is_like': is_like}, safe=False)

        if 'is_like' in data.keys():
            is_like = Like.objects.filter(user=user, post=post).exists()
            return JsonResponse({'is_like': is_like}, safe=False)