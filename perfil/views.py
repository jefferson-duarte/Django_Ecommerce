from typing import Any
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from .models import Perfil
from .forms import UserForm, PerfilForm


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

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
                    data=self.request.POST or None
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

        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        return self.renderizar


class Atualizar(View):
    ...


class Login(View):
    ...


class Logout(View):
    ...
