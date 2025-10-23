from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'package',
        'added_at',
    ]
    
    list_filter = [
        'added_at',
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'package__name',
    ]
    
    readonly_fields = ['added_at']
    
    fieldsets = (
        ('Información', {
            'fields': ('user', 'package')
        }),
        ('Información Adicional', {
            'fields': ('added_at',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'package')