from django.contrib import admin

# Nota: Los modelos de mongoengine (ReunionNacional, Agenda, Acuerdo, etc.)
# no se registran en el admin de Django ya que son documentos de MongoDB
# Para gestionarlos, se puede crear una interfaz personalizada en las vistas
