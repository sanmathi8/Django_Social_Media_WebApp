from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .models import Profile, Post, Comment, Like, Follow
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm

@login_required
def home(request):
    posts = Post.objects.all().select_related('user', 'user__profile').prefetch_related('likes', 'comments', 'comments__user')
    comment_form = CommentForm()
    user_liked_posts = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    
    context = {
        'posts': posts,
        'comment_form': comment_form,
        'user_liked_posts': user_liked_posts,
    }
    return render(request, 'home.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    context = {
        'profile_user': profile_user,
        'profile': profile_user.profile,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile', username=request.user.username)
        messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'edit_profile.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
        messages.error(request, "Please upload a valid image.")
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id).select_related('profile')
    return render(request, 'search.html', {'query': query, 'results': results})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_exists = Like.objects.filter(post=post, user=request.user)
    
    if like_exists.exists():
        like_exists.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        liked = True
        
    likes_count = post.likes.count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('ajax') == 'true':
        return JsonResponse({
            'liked': liked,
            'likes_count': likes_count
        })
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added!")
        else:
            messages.error(request, "Could not add empty comment.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow == request.user:
        messages.warning(request, "You cannot follow yourself.")
        return redirect('profile', username=username)
        
    follow_rel = Follow.objects.filter(follower=request.user, following=user_to_follow)
    
    if follow_rel.exists():
        follow_rel.delete()
        messages.info(request, f"Unfollowed {username}.")
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f"Following {username}!")
        
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('profile', username=username)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('profile', username=request.user.username)
