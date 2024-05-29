from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View


class ListaProdutos(ListView):
    ...


class DetalheProduto(View):
    ...


class AdicionarAoCarrinho(View):
    ...


class RemoverDoCarrinho(View):
    ...


class Carrinho(View):
    ...


class Finalizar(View):
    ...
