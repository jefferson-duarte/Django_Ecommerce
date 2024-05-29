from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from .models import Produto


class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6


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
