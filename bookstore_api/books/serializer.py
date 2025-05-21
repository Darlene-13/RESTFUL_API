from rest_framework import serializers
from .models import Book, PriceHistory

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'price','start_date','end_date']
        read_only_fields=['id']

class BookSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Book 
        fields = ['id', 'title', 'language', 'price', 'genre', 'created_at', 'updated_at', 'price_history']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'price': {'required': True},
            'language': {'required': True},
            'genre': {'required': True},
        }

        def validate_price(self, value):
            """Ensure that the price is always positive"""
            if value <=0:
                raise serializers.ValidationError("Price must be positive")
            return value
        
        def create(self, validated_data):
            # Create a book and its initial price history entry
            book = Book.objects.create(**validated_data)

            #Create initial price history entry
            PriceHistory.objects.create(
                book=book,
                price=validated_data['price'],
                start_date = validated_data['created_at'],
                end_date = None
            )
        def update(self, instance, validated_data):
            """ Update the book and a create a new price hisory entry if price is changed"""
            if 'price' in validated_data['price'] != instance.price:
                current_price = instance.price_history.order_by('start_date').first()
                if current_price and not current_price.end_date:
                    import datetime
                    