
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    content=models.CharField(max_length=140)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    imageUrl=models.CharField(max_length=1000,null=True)
    date=models.DateTimeField(auto_now_add=True) 
    comment=models.CharField(max_length=140, default="feedback")
    
    def __str__(self):
        return f"post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"

class Follow(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_who_is_following")
    user_follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_who_is_followed")
    def __str__(self):
        return f"{self.user} is following {self.user_follower}"
    

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_like')
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_like')


    def __str__(self):
        return f"{self.user} liked {self.post}"
    

class comment (models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userComment")
    post=models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="postComment")
    message=models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.author} comment on {self.post}"
class Category(models.Model):
    
    categoryName=models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName
    