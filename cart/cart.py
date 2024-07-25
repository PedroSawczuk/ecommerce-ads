from decimal import Decimal
from django.http import request
from django.conf import settings

from app.models import Produto

class Cart(object):

    def __init__(self):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart

    def addProduto(self, produto, quantidade=1, alterarquant=False):
        idproduto = str(produto.id)
        if idproduto not in self.cart:
            self.cart[idproduto] = {'quantidade': 0, 'preco': str(produto.preco)}
        if alterarquant:
            self.cart[idproduto]['quantidade'] = quantidade
        else:
            self.carrinho[idproduto]['quantidade'] += quantidade
        self._salvar()
    
    def _salvar(self):
        self.session.modified = True

    def removerProduto(self, produto):
        idproduto = str(produto.id)
        if produto in self.cart:
            del self.cart[idproduto]
            self._salvar()

    def __iter__(self):
        idsprodutos = self.cart.key()
        produtos = Produto
        produtos = Produto.objects.filter(id__in=idsprodutos)
        cart = self.cart.copy()
        for p in produtos:
            cart[str(p.id)]['produto'] = p
        for item in cart.value():
            item['preco'] = Decimal(item['prco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield

    def __len__(self):
        return sum(item['quantidade'] for item in self.cart.values())
    
    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.cart.values())
    
    def limpar(self):
        del self.session[settings.CART_SESSION_ID]
        self._salvar