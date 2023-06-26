
from django import forms
from network.models import Comment,Post,User,Message

from django.contrib.auth.forms import UserCreationForm


class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "input-field"
            }),
            'email': forms.TextInput(attrs={
                "class": "input-field"
            }),
            'password1': forms.TextInput(attrs={
                "class": "input-field"
            })
            

        }

class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','photo']
       
class FileUploadForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['avatar']
        


class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
       


