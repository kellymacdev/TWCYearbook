from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.core import paginator
import os
from django.conf import settings


from .models import User, Post, Graduate


def index(request):
    #posts = Post.objects.all()
    #paginate = paginator.Paginator(posts, 10)
    #page_number = request.GET.get('page', 1)
    #page_obj = paginate.get_page(page_number)
    grads = Graduate.objects.all().order_by('name')
    return render(request, 'network/index.html', {
        #"posts": [post.serialize(request.user) for post in page_obj.object_list],
        #"page": page_obj.number,
        #"has_next": page_obj.has_next(),
        #"has_previous": page_obj.has_previous(),
        #"total_pages": page_obj.paginator.num_pages,
        "graduates": grads,
        "grads_name_id": [grad.name.replace('', '_') for grad in grads]
    })

@login_required
def all_posts(request, profile_name):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post(content=data.get("new_post_content",""), user=request.user)
        post.save()
        return JsonResponse(post.serialize(), safe=False)
    elif request.method == "GET":
        if profile_name == "all":
            posts = Post.objects.all().order_by("-timestamp")
        elif profile_name == "following":
            user_profile = User.objects.get(username=request.user)
            users_following = user_profile.following.all()
            posts = Post.objects.filter(user__in = users_following).order_by("-timestamp")
        else:
            user_profile = User.objects.get(username=profile_name)
            posts = Post.objects.filter(user=user_profile).order_by("-timestamp")

        paginate = paginator.Paginator(posts, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginate.get_page(page_number)
        return JsonResponse({
            "posts": [post.serialize(request.user) for post in page_obj.object_list],
            "page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "total_pages": page_obj.paginator.num_pages
            })


@login_required
def edit_post(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(pk=post_id)
        if request.user.is_authenticated and request.user==post.user:
            return JsonResponse(post.serialize(request.user),safe=False)
        else:
            return JsonResponse("not_user", safe=False)
    elif request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        if request.user.is_authenticated and request.user==post.user:
            data = json.loads(request.body)
            edited_content = data.get("content", "")
            post.content = edited_content
            post.save()
            return JsonResponse(post.serialize(request.user), safe=False)


@login_required
def profile(request, grad_id):
    if request.method == "GET":
        grad = Graduate.objects.get(pk=grad_id)
        gradname = grad.name.replace(' ', '-')
        folder_path = os.path.join(settings.BASE_DIR, 'network', 'static', 'photos', f'{gradname}')
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith('.') ]
        file_urls = [f'photos/{gradname}/{f}' for f in files]
        if grad.q9:
            if grad.spotify:
                song = grad.spotify
                song_description = None
            else:
                song_description = grad.q9
                song = None
        else:
            song = None
            song_description = None
        return render(request, "network/profile.html", {
            "graduate": grad,
            "song": song,
            "song_description": song_description,
            "pics": file_urls
        })
    elif request.method == "POST":
        grads = list(Graduate.objects.all().order_by('name'))
        current_grad = Graduate.objects.get(pk=grad_id)
        current_index = grads.index(current_grad)
        count_grad = Graduate.objects.count()
        if "next" in request.POST:
            next_index = current_index + 1
            if next_index > count_grad:
                next_index = 0
            next_id = grads[next_index].pk
            return redirect('profile', next_id)
        elif "previous" in request.POST:
            prev_index = current_index - 1
            if prev_index < 0:
                prev_index = count_grad-1
            prev_id = grads[prev_index].pk
            return redirect('profile', prev_id)


@login_required
def memoriam(request, person):
    grads = Graduate.objects.all()
    for_linda = []
    for_zaza = []
    if person == "linda":
        for grad in grads:
            if grad.for_linda:
                for_linda.append([grad.for_linda,grad.name])
        list = for_linda
        folder_path = os.path.join(settings.BASE_DIR, 'network', 'static', 'linda')
        files = sorted(
            [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith('.') ]
        )
        file_urls1 = [f'linda/{f}' for f in files[0:6]]
        file_urls2 = [f'linda/{f}' for f in files[6:]]
    elif person == "zaza":
        for grad in grads:
            if grad.for_zaza:
                for_zaza.append([grad.for_zaza,grad.name])
        list = for_zaza
        folder_path = os.path.join(settings.BASE_DIR, 'network', 'static', 'zaza')
        files = sorted(
            [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith('.') ]
        )
        file_urls1 = [f'zaza/{f}' for f in files[0:7]]
        file_urls2 = [f'zaza/{f}' for f in files[7:]]
    else:
        list = None
        file_urls1 = None
        file_urls2 = None


    return render(request, "network/memoriam.html", {
        "person": person.capitalize(),
        "memoriam_list": list,
        "imgs": [file_urls1, file_urls2]
    })

@login_required
def summary(request):
    grads = Graduate.objects.all()
    tot_babies = 0
    tot_jobs = 0
    tot_school = 0
    tot_countries = 0
    tot_tattoos = 0
    i = 0
    j= 0
    k = 0
    l = 0
    m = 0
    for grad in grads:
        if grad.jobs is not None:
            i+=1
            tot_jobs += grad.jobs
        if grad.school_years is not None:
            j += 1
            tot_school += grad.school_years
        if grad.countries is not None:
            k+= 1
            tot_countries += grad.countries
        if grad.tattoos is not None:
            l+=1
            tot_tattoos += grad.tattoos
        if grad.babies is not None:
            m += 1
            tot_babies += grad.babies
    av_babies = tot_babies/m
    av_jobs = tot_jobs/i
    av_school = tot_school/j
    av_countries = tot_countries/k
    av_tattoos = tot_tattoos/l

    return render(request, "network/summary.html",{
        "grads": grads,
        "av_babies": round(av_babies,2),
        "av_jobs": round(av_jobs,2),
        "av_school": round(av_school,2),
        "av_countries": round(av_countries,2),
        "av_tattoos": round(av_tattoos,2)
    })

@login_required
def toggle_follow(request, profile_name):
    if request.method == "PUT":
        user_profile = User.objects.get(username=profile_name)
        if request.user in user_profile.followers.all():
            user_profile.followers.remove(request.user)
            follow_status = "unfollowed"
        else:
            user_profile.followers.add(request.user)
            follow_status = "followed"
        return JsonResponse({
            'follow_status': follow_status,
            'follower_count': user_profile.followers.count(),
            "following_count": user_profile.following.count()
        })

@login_required
def toggle_like(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            like_status = "unliked"
        else:
            post.likes.add(request.user)
            like_status = "like"
        return JsonResponse({
            'like_status': like_status,
            'like_count': post.likes.count(),
        })


@login_required
def following(request, profile_name):
    return render(request, "network/following.html")

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
        invite_code = request.POST.get("invite_code")  # new field

        # Check invite code
        if invite_code != "CLASS2015":  # your secret code
            return render(request, "network/register.html", {
                "message": "Invalid invite code."
            })



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

