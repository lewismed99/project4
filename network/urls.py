
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("about", views.about, name="about"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newPost',views.newPost,name='newPost'),
    path('profile/<int:user_id>',views.profile,name='profile'),
    path('follow',views.follow,name='follow'),
    path('unfollow',views.unfollow,name='unfollow'),
    path('following',views.following,name='following'),
     path('edit/<int:post_id>',views.edit,name='edit'),
     path('remove_like/<int:post_id>',views.remove_like,name='edit'),
     path('add_like/<int:post_id>',views.add_like,name='edit'),
     path('addComment/<int:id>',views.addComment,name='addComment'),

]
