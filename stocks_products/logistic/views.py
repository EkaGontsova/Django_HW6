from rest_framework.filters import SearchFilter, BaseFilterBackend
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class ProductFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_name = request.GET.get('products')
        if product_name:
            try:
                product_id = int(product_name)
                return queryset.filter(positions__product_id=product_id)
            except ValueError:
                return (queryset.filter(positions__product__title__icontains=product_name) |
                        queryset.filter(positions__product__description__icontains=product_name))
        return queryset


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [SearchFilter, ProductFilterBackend]
    search_fields = ['address']
