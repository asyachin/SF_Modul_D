from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        post_rating = sum([post.rating * 3 for post in self.post_set.all()])
        comment_rating = sum([comment.rating for comment in self.user.comment_set.all()])
        post_comment_rating = sum([comment.rating for post in self.post_set.all() for comment in post.comments.all()])
        
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'A'
    news = 'N'
    TYPES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_type = models.CharField(max_length=1, choices=TYPES, default=article)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:124]}..."


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

