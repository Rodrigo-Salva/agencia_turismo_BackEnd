from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Wishlist, Package
from .serializers import (
    WishlistSerializer,
    WishlistCreateSerializer,
    WishlistListSerializer
)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['package']
    search_fields = ['package__name']
    ordering_fields = ['added_at']
    ordering = ['-added_at']
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('package')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return WishlistCreateSerializer
        elif self.action == 'list':
            return WishlistListSerializer
        return WishlistSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        package = serializer.validated_data['package']
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            package=package
        )
        
        if not created:
            return Response(
                {'message': 'Este paquete ya está en tu lista de deseos'},
                status=status.HTTP_200_OK
            )
        
        return Response(
            WishlistSerializer(wishlist_item).data,
            status=status.HTTP_201_CREATED
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='toggle/(?P<package_id>[^/.]+)')
    def toggle(self, request, package_id=None):
        try:
            wishlist_item = Wishlist.objects.get(
                user=request.user,
                package_id=package_id
            )
            wishlist_item.delete()
            return Response(
                {'message': 'Paquete eliminado de la lista de deseos', 'in_wishlist': False},
                status=status.HTTP_200_OK
            )
        except Wishlist.DoesNotExist:
            try:
                package = Package.objects.get(id=package_id)
            except Package.DoesNotExist:
                return Response(
                    {'error': 'Paquete no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            wishlist_item = Wishlist.objects.create(
                user=request.user,
                package=package
            )
            return Response(
                {
                    'message': 'Paquete agregado a la lista de deseos',
                    'in_wishlist': True,
                    'item': WishlistSerializer(wishlist_item).data
                },
                status=status.HTTP_201_CREATED
            )
    
    @action(detail=False, methods=['get'], url_path='check/(?P<package_id>[^/.]+)')
    def check(self, request, package_id=None):
        exists = Wishlist.objects.filter(
            user=request.user,
            package_id=package_id
        ).exists()
        
        return Response({'in_wishlist': exists})
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        count = self.get_queryset().count()
        self.get_queryset().delete()
        
        return Response(
            {'message': f'{count} elemento(s) eliminado(s) de la lista de deseos'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})