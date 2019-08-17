from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import SignupForm, ProfileForm
from .models import Profile, UserHistory, User

# 회원가입
class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect(self.get_success_url())


signup = SignupView.as_view()


@login_required
def profile(request):
    user_instance = User.objects.filter(id=request.user.id)[0]
    user_history = UserHistory.objects.filter(user_id=user_instance.id)
    return render(request, 'accounts/profile.html', {'user_history': user_history})


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:history')

    def get_object(self):
        return self.request.user.profile


# profile_edit = ProfileUpdateView.as_view()
profile_edit = ProfileUpdateView.as_view()


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:history')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)

#
#
def user(request):
    if request.method == 'POST':
        user_result = request.POST.get("abc")
        user_result = user_result.split(",")  # 스플릿 결과는 리스트


        user_instance = User.objects.filter(id=request.user.id)[0]
        if user_result[3] != '0':
            UserHistory.objects.create(
                user=user_instance,
                stock_name=user_result[0],
                rate_of_return=user_result[1],
                total_assets=user_result[2],
                amount_of_asset_change=user_result[3],
                trade_numbers=user_result[4],
                john_bur_term=user_result[5],
            )
            user_result[5:] = [sum(list(map(float, user_result[5:])))]

        else:
            UserHistory.objects.create(
                user=user_instance,
                stock_name=user_result[0],
                rate_of_return=0,
                total_assets=user_result[2],
                amount_of_asset_change=0,
                trade_numbers=0,
                john_bur_term=0,
            )
            user_result[5:] = ['0']

    user_instance = User.objects.filter(id=request.user.id)[0]
    user_history = UserHistory.objects.filter(user_id=user_instance.id)
    return render(request, "accounts/profile.html", {'user_history': user_history})


def profile_delete(request):
    if request.method == 'POST':

        print(request.POST.getlist('checkRow'))
        # print(UserHistory.objects.filter(pk__in=a))
        return redirect()




