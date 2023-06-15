from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('home/logout/', views.LogoutPage.as_view(), name='logout'),
    path('create_post/', views.CreatePostView.as_view(success_url='/'), name='addpost'),
    path('home/profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('delete/<int:pk>',views.BbDeleteView.as_view(), name='delete'),
    path('post/<int:pk>/toggle_like/', views.ToggleLikeView.as_view(), name='toggle_like'),
]


