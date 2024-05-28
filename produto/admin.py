from django.contrib import admin
from .models import Produto, Variacao


@admin.register(Variacao)
class VaricacaoAdmin(admin.ModelAdmin):
    list_display = [
        'produto',
        'nome',
        'preco',
        'preco_promocional',
        'estoque',
    ]


class VariacaoInLine(admin.TabularInline):
    model = Variacao
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'descricao_curta',
        'get_preco_formatado',
        'get_preco_promo_formatado',
        'tipo',
    ]

    inlines = [
        VariacaoInLine
    ]
