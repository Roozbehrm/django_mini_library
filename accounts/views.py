from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from books.forms import RegisterForm


def register(request):

    if request.user.is_authenticated:
        return redirect("books:book_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"خوش آمدید {user.username}! ثبت‌نام شما با موفقیت انجام شد.")
            return redirect("books:book_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


