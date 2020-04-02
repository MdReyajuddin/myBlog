from django import forms
# from tinymce import TinyMCE

from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 'categories', 'featured', 'previous_post', 'next_post')

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
                            'class': 'form-control',
                            'placeholder': 'Type Your Comment',
                            'id': 'usercomment',
                            'rows': '4'}))
    class Meta:
        model = Comment
        fields = ('content',)
