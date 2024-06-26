from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Post, Follow, Like, comment

def remove_like(request, post_id):
    post=Post.objects.get(pk=post_id)
    user=User.objects.get(pk=request.user.id)
    like=Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"messasge": "like removed"})
def add_like(request,post_id):
    post=Post.objects.get(pk=post_id)
    user=User.objects.get(pk=request.user.id)
    newLike=Like(user=user, post=post)
    newLike.save()
    return JsonResponse({"messasge": "like added"})
def edit(request, post_id):
    if request.method=="POST":
        data=json.loads(request.body)
        edit_post=Post.objects.get(pk=post_id)
        edit_post.content=data['content']
        edit_post.save()
        return JsonResponse({'message': 'change successful', 'data': data['content']})


def about(request):
    return render(request,'network/about.html')
def index(request):
    allPosts=Post.objects.all().order_by("id").reverse()

    #pagination
    paginator=Paginator(allPosts,2)
    page_number= request.GET.get('page')
    posts_of_the_page=paginator.get_page(page_number)
    allLikes=Like.objects.all().order_by('id').reverse()
    whoYouLiked=[]
    try:
        for likes in allLikes:
          if likes.user.id==request.user.id:
              whoYouLiked.append(likes.post.id)
    except:
        whoYouLiked=[]

    return render(request, "network/index.html",{

        "allPosts":allPosts,
        "posts_of_the_page":posts_of_the_page,
        'whoYouLiked':whoYouLiked
    })

def newPost(request):
    if request.method=="POST":

        content=request.POST['content']
        imageUrl=request.POST["imageurl"]
        user=User.objects.get(pk=request.user.id)
        
        post=Post(content=content, user=user, imageUrl=imageUrl)
        
        post.save()
        return HttpResponseRedirect(reverse(index))
def profile(request,user_id):
     user=User.objects.get(pk=user_id)
     otherUser=User.objects.get(pk=request.user.id)
    
    
    
     allPosts=Post.objects.filter(user=user).order_by("id").reverse()
     #pagniator
     following= Follow.objects.filter(user=user)
     followers=Follow.objects.filter(user_follower=user)
     
     try:
         checkFollow=followers.filter(user=User.objects.get(pk=request.user.id))
         if len(checkFollow) !=0:
             isFollowing=True
         else:
             isFollowing =False
     except:
         isFollowing= False


     paginator=Paginator(allPosts,2)
     page_number= request.GET.get('page')
     posts_of_the_page=paginator.get_page(page_number)
     return render(request, "network/profile.html",{

        "allPosts":allPosts,
        "posts_of_the_page":posts_of_the_page,
        "username":user.username,
        'following':following,
        "followers":followers,
        "isFollowing":isFollowing,
        "user_profile":user
    })

def following(request):
    currentUser=User.objects.get(pk=request.user.id)
    following_people=Follow.objects.filter(user=currentUser)
    allPosts=Post.objects.all().order_by("id").reverse()
    followingPosts=[]

    for posts in allPosts:
        for person in following_people:
            if person.user_follower==posts.user:
                followingPosts.append(posts)
        #pagination
    paginator=Paginator(followingPosts,2)
    page_number= request.GET.get('page')
    posts_of_the_page=paginator.get_page(page_number)
    return render(request, "network/following.html",{

        "posts_of_the_page":posts_of_the_page
    })


def follow(request):
    userfollow=request.POST['userfollow']
    currentUser=User.objects.get(pk=request.user.id)
    userfollowData=User.objects.get(username=userfollow)
    f=Follow(user=currentUser, user_follower=userfollowData)
    f.save()
    user_id=userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def unfollow(request):
    userfollow=request.POST['userfollow']
    currentUser=User.objects.get(pk=request.user.id)
    userfollowData=User.objects.get(username=userfollow)
    f=Follow.objects.get(user=currentUser, user_follower=userfollowData)
    f.delete()
    user_id=userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))


def login_view(request):

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def addComment(request,post_id):
    if request.method=="POST":#this checvks if we are recioeving a post method
        #data=json.loads(request.body)
        data=json.loads(request.body)#this will help us get the data from our jasvascript
        addCommentPost= Post.objects.get(pk=post_id)
        #(User.objects.get(pk=request.user.id)# this is ensure we have the user makingthe comment
        #currentUser = request.user
        addCommentPost.comment=data["comment"]
        addCommentPost.save()
        return JsonResponse({"messeage":"change successful", "data" :['comment']})
       # postData = Post.objects.get(pk=id)
        #message = request.POST.get('newComment')
        

        #newComment = comment(author=user, post=postData, message=message)
        #newComment.save()

       # return JsonResponse({'message': 'change successful', 'data': data['message']})
    

def displayCategory(request):
    if request.method=="POST":
        categoryFromForm=request.POST['category']
        category=category.objects.get(categoryName=categoryFromForm)

        activeListings=Listings.objects.filter(isActive=True, category=category)
        allCategories=category.objects.all()
        return render(request, "auctions/index.html",{
        "listings":activeListings,
        "categories":allCategories,
        })

    #return HttpResponseRedirect(reverse('index'))
# def addComment(request,id):
#     currentUser=request.user
#     postData=Post.objects.get(pk=id)
#     message=request.POST['newComment'],



#     newComment= comment(
#         author=currentUser,
#         listing=postData,
#         message=message
#     )
#     newComment.save()
#     return HttpResponseRedirect(reverse(index))
#     #return HttpResponseRedirect(reverse("index",args=(id, )))