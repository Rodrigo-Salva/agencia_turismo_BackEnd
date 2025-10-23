from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class PackagePlaceholder(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Package placeholder'
        verbose_name_plural = 'Package placeholders'


class Wishlist(models.Model):
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        verbose_name='Usuario'
    )
    
    package = models.ForeignKey(
        'Package',
        on_delete=models.CASCADE,
        related_name='wishlisted_by',
        verbose_name='Paquete'
    )
    
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Agregado')
    
    class Meta:
        db_table = 'lista_deseos'
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Lista de Deseos'
        ordering = ['-added_at']
        unique_together = ['user', 'package']
        indexes = [
            models.Index(fields=['user', '-added_at']),
            models.Index(fields=['package']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.package.name}"