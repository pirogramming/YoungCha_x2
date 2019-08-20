from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render, resolve_url, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import SignupForm, ProfileForm
from .models import Profile, UserHistory, User
import json
import random
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
        auth_login(self.request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.get_success_url())


signup = SignupView.as_view()


@login_required
def profile(request):
    user_instance = User.objects.filter(id=request.user.id)[0]
    user_history = UserHistory.objects.filter(user_id=user_instance.id)
    user = Profile.objects.filter(user_id=request.user.id)[0]
    wallet_3 = format(user.wallet, ",")

    return render(request, 'accounts/profile.html', {'user_history': user_history, 'user_profile': user, "user_wallet": wallet_3})








class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:history')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)


def user(request):
    user_check = User.objects.filter(id=request.user.id)
    if not user_check:
        return redirect("data:data_home")
    if not ("@" in request.user.username):
        user_instance_check = Profile.objects.filter(user_id=user_check[0].id)
        if not user_instance_check:
            Profile.objects.create(name=user_check[0].last_name+user_check[0].first_name, user_id=user_check[0].id, wallet=10000000)
            return redirect("data:data_home")
        else:
            pass
    if request.method == 'POST':
        user_result = request.POST.get("abc")

        user_result = json.loads(user_result)

        user_history = UserHistory.objects.all()

        if len(user_history):
            latest_score = user_history[len(user_history) - 1].total_assets
        else:
            #유저 히스토리가 없을 경우 유효성 검사를 적당히 함
            latest_score = 999999999999
        user_result = request.POST.get("abc")
        user_result = json.loads(user_result)
        if user_result['total_return'] != int(latest_score):
            try:
                user_instance = User.objects.filter(id=request.user.id)[0]
                profile_instance = Profile.objects.filter(user_id=request.user.id)[0]
            except IndexError:
                return redirect(reverse('data:data_home'))

            profile_instance.wallet += int(user_result['total_return'])

            profile_instance.save()

            if user_result['delta_return'] != '0':
                UserHistory.objects.create(
                    user=user_instance,
                    stock_name=user_result["name"], # 0 = name
                    rate_of_return=user_result['total_yield'], # 1 = totalT_yield
                    total_assets=user_result["total_return"], # 2 = total_return
                    amount_of_asset_change=user_result['delta_return'], # 3 = delta_return
                    trade_numbers=user_result['trading_numbers'], # 4 = trading_numbers
                    john_bur_term=sum(list(map(float, user_result['jonber_periods']))), # 5 = jonber_periods
                )
                user_result['jonber_periods'] = [sum(list(map(float, user_result['jonber_periods'])))]


            else:
                UserHistory.objects.create(
                    user=user_instance,
                    stock_name=user_result[0],
                    rate_of_return=0,
                    total_assets=user_result['total_return'],
                    amount_of_asset_change=0,
                    trade_numbers=0,
                    john_bur_term=0,
                )
                user_result['jonber_periods'] = ['0']

            try:
                user_instance = User.objects.filter(id=request.user.id)[0]

            except IndexError:
                return redirect(reverse('data:data_home'))

            user_history = UserHistory.objects.filter(user_id=user_instance.id)
            user = Profile.objects.filter(user_id=request.user.id)[0]
            wallet_3 = format(user.wallet, ",")

            return render(request, "accounts/profile.html", {'user_history': user_history, 'user_profile': profile_instance, 'user_wallet': wallet_3})

        else:
            user_instance = User.objects.filter(id=request.user.id)[0]
            user_history = UserHistory.objects.filter(user_id=user_instance.id)
            user = Profile.objects.filter(user_id=request.user.id)[0]

            return render(request, 'accounts/profile.html', {'user_history': user_history, 'user_wallet': user.wallet})
    else:
        return redirect("data:data_home")