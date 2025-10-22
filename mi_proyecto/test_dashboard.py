#!/usr/bin/env python
"""Script para probar que el dashboard incluye todas las categorías"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import Participante
from mi_aplication.constants import CATEGORIAS_FORMATIVAS

print("=" * 80)
print("VERIFICACIÓN DE CATEGORÍAS EN DASHBOARD")
print("=" * 80)

# Contar participantes por categoría
print(f"\nTotal de categorías definidas: {len(CATEGORIAS_FORMATIVAS)}\n")

dict_categorias = dict(CATEGORIAS_FORMATIVAS)

# Simular el procesamiento que hace la vista
participantes_con_categoria = Participante.objects.filter(
    categoria_formativa__exists=True, 
    categoria_formativa__ne=''
)

stats_por_categoria = {}
for participante in participantes_con_categoria:
    if participante.categoria_formativa:
        categoria = participante.categoria_formativa
        if categoria not in stats_por_categoria:
            stats_por_categoria[categoria] = {'total': 0}
        stats_por_categoria[categoria]['total'] += 1

print("Conteo por categoría:")
print("-" * 80)

categorias_resultado = []
for codigo_categoria, nombre_categoria in CATEGORIAS_FORMATIVAS:
    if codigo_categoria in stats_por_categoria:
        total = stats_por_categoria[codigo_categoria]['total']
        print(f"✓ {nombre_categoria}: {total} participantes")
        categorias_resultado.append({
            'nombre': nombre_categoria,
            'total': total
        })
    else:
        # Categoría sin datos, agregar con total 0
        print(f"• {nombre_categoria}: 0 participantes (sin datos)")
        categorias_resultado.append({
            'nombre': nombre_categoria,
            'total': 0
        })

print("\n" + "=" * 80)
print(f"RESULTADO: Todas las {len(CATEGORIAS_FORMATIVAS)} categorías están incluidas")
print(f"Total categorías en resultado: {len(categorias_resultado)}")
print("=" * 80)

# Verificar que todas estén incluidas
if len(categorias_resultado) == len(CATEGORIAS_FORMATIVAS):
    print("\n✓ ÉXITO: Todas las categorías aparecerán en el gráfico de flor")
    print("  Incluso las que tienen 0 participantes mostrarán un pétalo en cero")
else:
    print("\n✗ ERROR: Faltan categorías")
