from django.db import models

# Create your models here.
class Galeria(models.Model):
    titulo = models.CharField(max_length=150, default="")
    imagen = models.ImageField(upload_to='galeria/')
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo Subido el {self.fecha_subida.strftime('%Y-%m-%d')}"
    