from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import UserForm


def account_new(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            User = form.save()
            return redirect(user)
    else:
        form = UserForm()
    return render(request, 'blog/post_new.html', {'form': form})