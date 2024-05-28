from django.contrib import admin
from .models import Pedido, ItemPedido


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = [
        'pedido',
        'produto',
        'variacao',
        'preco',
        'quantidade',
    ]


class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'total',
        'status',
    ]

    inlines = [
        ItemPedidoInLine
    ]
