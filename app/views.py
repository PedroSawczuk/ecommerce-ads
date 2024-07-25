from django.shortcuts import render
from django.views.generic import *
from app.models import *

class HomeView(TemplateView):
    template_name = 'index.html'

class CategoriaListView(ListView):
    template_name = 'produtos/categorias.html'
    context_object_name = 'categorias'  
    model = Categoria   

class ProdutosListView(ListView):
    model = Produto
    template_name = 'produtos/listarprodutos.html'
    context_object_name = 'produtos'
    # queryset = Produto.disponiveis.all()

    def get_queryset(self): # removi o parâmetro daqui
        qs = super().get_queryset()
        slug = self.kwargs['slug'] # obtive o parâmetro dos argumentos passados na requisição
        if slug:
            cat = Categoria.objects.get(slug=slug) # acrescentei o objects.
            qs = qs.filter(categoria=cat)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        if slug:
            context['categoria'] = Categoria.objects.get(slug=slug)
        return context
    
class ProdutoDetailView(DetailView):
    model = Produto
    template_name = "produtos/produto.html"