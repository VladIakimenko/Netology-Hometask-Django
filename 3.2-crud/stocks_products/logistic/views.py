from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.all()
        search_query = self.request.query_params.get('products')
        if search_query:
            try:
                int(search_query)
                queryset = queryset.filter(products__id=search_query)
            except ValueError:
                queryset = queryset.filter(
                Q(products__title__icontains=search_query) |
                Q(products__description__icontains=search_query)
            )
        return queryset

