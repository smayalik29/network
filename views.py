from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from posts.models import Post
from .forms import SignupForm, ProfileForm
from .models import User, Profile


def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, "Registration successfully!")
        return redirect('login')
        auth_login(request, user)
        messages.success(request, "Account created successfully!")
        

    return render(request, 'accounts/signup.html', {'form': form})

def auth_login_view(request):
        # If user is already logged in
    if request.user.is_authenticated:
        return redirect('home')  # redirect to profile/home

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Correct authenticate call for custom user model
        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")

    # Return the login page for GET requests or failed POST
    return render(request, 'accounts/login.html')
@login_required
def auth_logout_view(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


@login_required
def profile_view(request, username=None):
    """
    If username is provided, show that user's profile.
    Otherwise, show the logged-in user's profile.
    """
    # Get the profile to display
    if username:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
    else:
        profile, created = Profile.objects.get_or_create(user=request.user)

    # Profile update form only for own profile
    if request.user == profile.user:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('my_profile')
        else:
            form = ProfileForm(instance=profile)
    else:
        form = None  # other users cannot edit your profile

    # Posts and connections of the profile being viewed
    posts = Post.objects.filter(user=profile.user).order_by('-created_at')
    connections = profile.connections.all()

    context = {
        'form': form,
        'profile_user': profile,
        'posts': posts,
        'connections': connections
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def user_profile(request,username):
    user=get_object_or_404(User,username=username)
    posts=Post.objects.filter(user=user)
    return render(request,'accounts/user_profile.html',{
        'profile_user':user
        })
    
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

