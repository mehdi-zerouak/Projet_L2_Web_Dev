from django import forms
from .models import Post , PostComment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title' , 'content' , 'image']
        widgets = {
            'content':forms.Textarea(attrs={'rows':20,'cols':100})
        }

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['comment']
        widgets = {
            'comment':forms.Textarea(attrs={'rows':10,'cols':70})
        }