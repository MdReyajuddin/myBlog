from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # comment_count = models.IntegerField(default=0)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    featured = models.BooleanField()
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, null=True, blank=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'id': self.id})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    # @property
    # def view_count(self):
    #     return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

