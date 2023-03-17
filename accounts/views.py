from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from notification.models import Notificaiton
from .decorators import (not_logged_in_required)
from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm
)
from .models import Follow, User


@never_cache
@not_logged_in_required
def login_user(request):
    """
        - Ця функція виконує авторизацію користувача та повертає на головну
        сторінку сайту, якщо авторизація успішна.

        - Для того, щоб використати цю функцію, потрібно використовувати два
        декоратори: never_cache та not_logged_in_required.
        Декоратор never_cache запобігає кешуванню сторінки браузером,
        а декоратор not_logged_in_required перенаправляє авторизованих
        користувачів на головну сторінку.

        - Функція приймає запит методом POST, перевіряє форму на коректність
        та автентифікує користувача за допомогою функції authenticate
        з модулю django.contrib.auth. Якщо користувач успішно
        автентифікується, то викликається функція login з того ж модулю,
        що дозволяє залогінити користувача.

        - Якщо авторизація не вдалась, то викликається функція
        messages.warning з модулю django.contrib.messages,
        що виводить на сторінку повідомлення про помилку.

        - Функція повертає шаблон accounts/login.html з формою авторизації
        та контекстом, що містить цю форму.
    """
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Неправильні облікові дані")

    context = {
        "form": form
    }

    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@never_cache
@not_logged_in_required
def register_user(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Реєстрація успішна")
            return redirect('login')

    context = {
        "form": form
    }

    return render(request, 'accounts/registration.html', context)


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)

    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')

        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль успішно оновлено")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def change_profile_picture(request):
    if request.method == "POST":

        form = ProfilePictureUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)

            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_image = image
            user.save()
            messages.success(request, "Зображення профілю успішно оновлено")

        else:
            print(form.errors)

    return redirect('profile')


def view_user_information(request, username):
    account = get_object_or_404(User, username=username)
    following = False
    muted = None

    if request.user.is_authenticated:

        if request.user.id == account.id:
            return redirect("profile")

        followers = account.followers.filter(
            followed_by__id=request.user.id
        )
        if followers.exists():
            following = True

    if following:
        queryset = followers.first()
        if queryset.muted:
            muted = True
        else:
            muted = False

    context = {
        "account": account,
        "following": following,
        "muted": muted
    }

    return render(request, "accounts/user_information.html", context)


@login_required(login_url="login")
def follow_or_unfollow_user(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    followed_by = get_object_or_404(User, id=request.user.id)

    follow, created = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        follow.delete()

    return redirect("view_user_information", username=followed.username)


@login_required(login_url='login')
def user_notifications(request):
    notifications = Notificaiton.objects.filter(
        user=request.user,
        is_seen=False
    )

    for notification in notifications:
        notification.is_seen = True
        notification.save()

    return render(request, 'accounts/notifications.html')


@login_required(login_url='login')
def mute_or_unmute_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    follower = get_object_or_404(User, pk=request.user.pk)
    instance = get_object_or_404(
        Follow,
        followed=user,
        followed_by=follower
    )

    if instance.muted:
        instance.muted = False
        instance.save()
    else:
        instance.muted = True
        instance.save()

    return redirect('view_user_information', username=user.username)
