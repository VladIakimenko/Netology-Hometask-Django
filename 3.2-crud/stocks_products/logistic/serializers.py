from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(**{'stock': stock, **position})

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            try:
                stock_product = StockProduct.objects.get(
                    stock=stock,
                    product=position['product']
                )
                stock_product.quantity = position['quantity']
                stock_product.price = position['price']
                stock_product.save()
            except StockProduct.DoesNotExist:
                StockProduct.objects.create(**{'stock': stock, **position})

    # THE COMMENTED OUT SNIPPET REPEATS THE ABOVE (TRY EXCEPT) FUNCTIONALITY WITH .update_or_create()
            # stock_product, created = StockProduct.objects.update_or_create(
            #     stock=stock,
            #     product=position['product'],
            #     defaults={
            #         'quantity': position['quantity'],
            #         'price': position['price'],
            #     }
            # )

        products_ids = [position['product'] for position in positions]
        StockProduct.objects\
            .filter(stock=stock)\
            .exclude(product__in=products_ids)\
            .delete()

        return stock
