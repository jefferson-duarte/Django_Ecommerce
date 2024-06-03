from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from .models import Perfil
from .forms import UserForm, PerfilForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import copy


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'user_form': UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfil_form': PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                ),
            }
        else:
            self.contexto = {
                'user_form': UserForm(
                    data=self.request.POST or None
                ),
                'perfil_form': PerfilForm(
                    data=self.request.POST or None
                ),
            }

        self.user_form = self.contexto['user_form']
        self.perfil_form = self.contexto['perfil_form']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.user_form.is_valid() or not self.perfil_form.is_valid():
            # if not self.user_form.is_valid():
            return self.renderizar

        username = self.user_form.cleaned_data.get('username')
        password = self.user_form.cleaned_data.get('password')
        email = self.user_form.cleaned_data.get('email')
        first_name = self.user_form.cleaned_data.get('first_name')
        last_name = self.user_form.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username
            )
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.perfil_form.cleaned_data['usuario'] = usuario
                perfil = Perfil(**self.perfil_form.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfil_form.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        else:
            usuario = self.user_form.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password,
            )

            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        return self.renderizar


class Atualizar(View):
    ...


class Login(View):
    ...


class Logout(View):
    ...
