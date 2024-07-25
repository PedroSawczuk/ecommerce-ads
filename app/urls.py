from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('categorias', CategoriaListView.as_view(), name="categorias"),
    path('<slug:slug>/produtos', ProdutosListView.as_view(), name="listarprodutos"),
    path('produto/<slug:slugprod>/<int:pk>/', ProdutoDetailView.as_view(), name='detailproduto'),
]
