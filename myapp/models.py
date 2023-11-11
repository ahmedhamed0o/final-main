# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class role (models.Model):
    role = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.role}"


class category(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser, models.Model):
    roles = models.ForeignKey(
        role, on_delete=models.CASCADE, blank=True, null=True, related_name="roles")
    categories = models.ManyToManyField(category, blank=True)
    picture = models.ImageField(
        upload_to="images/", default='images/default.png')
    pass


class articles(models.Model):
    title = models.CharField(max_length=20)
    image = models.CharField(max_length=2000)
    content = models.TextField(max_length=200)
    upperContent = models.TextField(max_length=500)
    secondImage = models.CharField(max_length=2000, blank=True)
    underContent = models.TextField(max_length=500)
    location = models.CharField(max_length=20)
    category = models.ForeignKey(
        category, on_delete=models.CASCADE, related_name="article_category")
    isActive = models.BooleanField(default=True)
    articleTime = models.TimeField()
    articleDate = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def date(self):
        return self.articleDate.strftime('%B %d')


class comments(models.Model):
    content = models.TextField(max_length=500, null=True)
    article = models.ForeignKey(
        articles, on_delete=models.CASCADE, related_name="comment_article")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"
