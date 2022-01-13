from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import *
# Create your models here.

class Pago(models.Model):
    
    no_tarjeta= models.BigIntegerField(null=True)
    nombre_tarjeta= models.CharField(max_length=40)
    cvv= models.IntegerField() 
    fecha_vencimiento = models.DateField(null=True)
    

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self) -> str:
        return self.id+" "+self.nombre_tarjeta

class Transaccion_Pendiente(models.Model):
    
    id_producto= models.IntegerField()
    nombre_producto = models.CharField(max_length=25)
    usuario_comprador = models.CharField(max_length=25)
    fecha_peticion = models.DateField(null=True)
    pago= models.ForeignKey(Pago, on_delete=models.CASCADE,null=True)
    

    class Meta:
        verbose_name = 'Transaccion_Pendiente'
        verbose_name_plural = 'Transacciones_Pendientes'

    def __str__(self) -> str:
        return self.id

class Transaccion_Autorizado(models.Model):
    
    id_producto= models.IntegerField()
    nombre_producto = models.CharField(max_length=25)
    usuario_authorizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, max_length=25,null=True)
    usuario_comprador = models.CharField(max_length=25)
    fecha_peticion = models.DateField(null=True)
    fecha_autorizado = models.DateField(null=True)
    pago= models.ForeignKey(Pago, on_delete=models.CASCADE,null=True)
    

    class Meta:
        verbose_name = 'Transaccion_Pendiente'
        verbose_name_plural = 'Transacciones_Pendientes'

    def __str__(self) -> str:
        return self.id

STATUS_CHOICES = (
    (1, 'Abierto'),
    (2, 'Cerrado'),
    (3, 'Manual'),
)

class Estado_Servidor(models.Model):
    estado=models.IntegerField(choices=STATUS_CHOICES,default=1)
    fecha=models.DateTimeField()