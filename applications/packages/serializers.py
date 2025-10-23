from rest_framework import serializers
from .models import Wishlist, Package


class WishlistSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_description = serializers.CharField(source='package.description', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'package',
            'package_name',
            'package_description',
            'added_at',
        ]
        read_only_fields = ['id', 'user', 'added_at']
    
    def validate(self, data):
        request = self.context.get('request')
        package = data.get('package')
        
        if request and request.user and package:
            if Wishlist.objects.filter(user=request.user, package=package).exists():
                raise serializers.ValidationError(
                    "Este paquete ya está en tu lista de deseos"
                )
        
        return data


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['package']


class WishlistListSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'package',
            'package_name',
            'added_at',
        ]