from django.shortcuts import render
from .forms import Registration,AddPost
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import FileUploadForm,ChatForm
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from .models import Post, Comment, Like, User,Follow,Chat,Message
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,RedirectView
from django.urls import reverse
from django.http import request
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views import View
import json
from rest_framework.permissions import IsAuthenticated  
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from rest_framework.views import APIView

class RegistrationView(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    



class HomeView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        following_users = Follow.objects.filter(user=user).values('following')
        queryset = super().get_queryset().filter(user__in=following_users) | super().get_queryset().filter(user=user)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_info = User.objects.get(username=self.request.user.username)  # або User.objects.get(id=self.request.user.id)

        context['user_info'] = user_info
        return context





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
class AddAboutInformation(UpdateView):
    fields = ['about','date_of_birth','hobby','work','city']
    template_name = 'profile.html'
    model = User

    def get_success_url(self):
        return f'/home/profile/{self.kwargs["pk"]}'

class Profile(UpdateView):
    # form_class = FileUploadForm
    fields = ['avatar']
    template_name = 'profile.html'
    model = User
    
    def test_func(self):
        user_id = self.kwargs['pk']
        return self.request.user.id == int(user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        current_user_posts = Post.objects.filter(user=self.request.user)
        followers = Follow.objects.filter(user=user)
        context['user'] = user
        context['posts'] = posts
        context['current_user_posts'] = current_user_posts
        context['followers'] = followers
        return context
    
    def get_success_url(self):
        return f'/home/profile/{self.kwargs["pk"]}'
    
   
    

class BbDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'index.html'
   





class ToggleLikeView(View):
    def post(self, request, **kwargs):
        data = request.POST
        user = self.request.user
        post = get_object_or_404(Post, id=self.kwargs['pk'])

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




class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        comment_body = request.POST.get('text', '')
        post = Post.objects.get(pk=post_id)
        user = request.user
        comment = Comment.objects.create(body=comment_body, user=user, post=post)

        # Отримати ім'я користувача
        if user.is_authenticated:
            username = user.username
        else:
            username = 'Anonymous'  # або будь-яке значення, яке ви вважаєте за потрібне

        # Повернути дані коментаря у форматі JSON
        data = {
            'id': comment.id,
            'body': comment.body,
            'username': username
        }

        return JsonResponse(data)

class DeleteCommentView(DeleteView):
    model = Comment
    success_url = reverse_lazy('home')
    template_name = 'index.html'




class SearchView(ListView):
    model = User
    template_name = 'index.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        return context


class ProfileUSer(TemplateView):
    template_name = 'profileuser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        user_following = Follow.objects.filter(user=self.request.user, following=user).exists()
        posts = Post.objects.filter(user=user)
        followers = Follow.objects.filter(user=self.request.user, following=user)
        user_info = User.objects.get(id=user_id)
        context['user'] = user
        context['user_following'] = user_following
        context['posts'] = posts
        context['followers'] = followers
        context['user_info'] = user_info
        return context
    

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_following = Follow.objects.filter(user=request.user, following=user).exists()

    context = {
        'user': user,
        'user_following': user_following
    }

    return render(request, 'profileuser.html', context)


def follow_user(request, user_id):
    user = User.objects.get(id=user_id)
    follow, created = Follow.objects.get_or_create(user=request.user)
    follow.following.add(user)

    return redirect('profileuser', pk=user_id)

def unfollow_user(request, user_id):
    user = User.objects.get(id=user_id)
    follow = Follow.objects.get(user=request.user)
    follow.following.remove(user)

    return redirect('profileuser', pk=user_id)


class ChatView(TemplateView):
    template_name = 'masenger.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        following = Follow.objects.filter(user=user)
        context['following_users'] = following.values_list('following__username', flat=True)
        context['user'] = user
        chats = Chat.objects.filter(members=user)
        chat_users = []
        for chat in chats:
            members = chat.members.exclude(id=user.id)
            chat_users.extend(members)
        context['chat_users'] = chat_users
        return context
    

class StartChatView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        username = self.request.POST.get('username')  # Отримати ім'я другого користувача з форми
        user1 = get_object_or_404(User, username=username)
       
        for c in Chat.objects.all():
            if user in c.members.all() and user1 in c.members.all():
                print(user, user1, 'iiiiiii')
                self.url = '/chat'
                break
        else:
            print(user, user1, "yyy")
            chat = Chat()
            chat.save()
            chat.members.add(user, user1)
            self.url = '/chat'
        return super().get_redirect_url(*args, **kwargs)


class ChatHidenView(TemplateView):
    template_name = 'masenger.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        following = Follow.objects.filter(user=user)
        context['following_users'] = following.values_list('following__username', flat=True)
        context['user'] = user
        chats = Chat.objects.filter(members=user)
        chat_users = []
        chat_ids = []  # Збереження ідентифікаторів чатів

        for chat in chats:
            members = chat.members.exclude(id=user.id)
            chat_users.extend(members)
            chat_ids.append(chat.id)  # Додавання ідентифікатора чату в список

        username = self.request.GET.get('username')
        user1 = User.objects.get(username=username)
        context['usernow'] = user1
        context['username'] = username

        # Визначення поточного ідентифікатора чату за username
        chat_with_user = Chat.objects.filter(members=user).filter(members=user1).first()
        print(chat_with_user, 'chat_with_user')

        chatids = chat_with_user.id if chat_with_user else None
        print(chatids, "поточний id")  # Виведення ID поточного чату в консоль
        context['chatids'] = chatids

        context['chat_users'] = chat_users
        context['chat_ids'] = chat_ids  # Передача ідентифікаторів чатів у контекст

        return context


class MasegView(APIView):
    def post(self, request):
        print("kdkdkkkkkkkkkkkkkkkkkkkkkkdkddwwywyywywywywywybdbdbdbdbdb")
        data_post = request.POST
        user = request.user

        if 'chat' in data_post:
            chat_id = data_post.get('chat')
            chat = Chat.objects.get(id=chat_id)

            if 'message' in data_post:
                message_body = data_post['message']
                sent_at = timezone.now()

                message = Message(user=user, chat=chat, body=message_body, sent_at=sent_at)
                message.save()

                return JsonResponse({
                    'message': message_body,
                    'user_id': message.user_id,
                    'sent_at': sent_at.strftime("%Y-%m-%d %H:%M:%S")  # Форматуємо час надсилання повідомлення
                })

        return JsonResponse({
            'error': 'Invalid request'
        }, status=400)

class GetMessagesView(View):
    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        messages = Message.objects.filter(chat=chat).values('user__username', 'sent_at', 'body')

        formatted_messages = []
        for message in messages:
            formatted_message = {
                'user': message['user__username'],
                'sent_at': message['sent_at'].strftime("%Y-%m-%d %H:%M:%S"),  # Форматуємо час надсилання повідомлення
                'body': message['body']
            }
            formatted_messages.append(formatted_message)

        return JsonResponse({'messages': formatted_messages})