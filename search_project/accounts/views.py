from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.views import View
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mycollection:home')
        return render(request, 'signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name='login.html'
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'ログインしました。')
        return super().form_valid(form)