from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import DeleteCommentView,SearchView,follow_user,unfollow_user

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    path('create_post/', views.CreatePostView.as_view(success_url='/'), name='addpost'),
    path('home/profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('delete/<int:pk>',views.BbDeleteView.as_view(), name='delete'),
    path('post/<int:pk>/toggle_like/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('post/<int:pk>/add_comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('home/delete_comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('search/', SearchView.as_view(), name='search'),
    path('home/profileuser/<int:pk>',views.ProfileUSer.as_view(),name='profileuser'),
    path('follow/<int:user_id>/', follow_user, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),
    path('addaboutuser/<int:pk>/',views.AddAboutInformation.as_view(),name='add_about_user'),
    path('chat/',views.ChatView.as_view(),name='chat'),
    path('start_chat/<int:user_id>/', views.StartChatView.as_view(), name='start_chat'),
    path('chathiden/',views.ChatHidenView.as_view(),name='chathiden'),
    path('message/', views.MasegView.as_view(), name='message'),
    path('chathiden/get_messages/<int:chat_id>/', views.GetMessagesView.as_view(), name='get_messages'),
  
  
   
]


