from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render, resolve_url, get_object_or_404
from django.views.generic import CreateView, UpdateView
from .forms import SignupForm, ProfileForm
from .models import Profile



#회원가입
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
    return render(request, 'accounts/profile.html')
























# class RequestLoginViaUrlView(PasswordResetView):
#     template_name = 'accounts/request_login_via_url_form.html'
#     title = '이메일을 통한 로그인'
#     email_template_name = 'accounts/login_via_url.html'
#     success_url = settings.LOGIN_URL


# def login_via_url(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         current_user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
#         raise Http404
#
#     if default_token_generator.check_token(current_user, token):
#         auth_login(request, current_user)
#         messages.info(request, '로그인이 승인되었습니다.')
#         return redirect('root')
#
#     messages.error(request, '로그인이 거부되었습니다.')
#     return redirect('root')

#비밀번호 변경
class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)

