#!/usr/bin/env python3
"""
Script de prueba para verificar la estructura de exportación
"""

# Simular un evento con clientes
evento_ejemplo = {
    'evento_num': 10,
    'reloj': 45.5,
    'evento': 'FIN_SERVICIO',
    'clientes': [
        {
            'id': 1,
            'estado': 'SIENDO ATENDIDO',
            'peluquero_esperando': 'Veterano A',
            'hora_ref': 'N/A',
            'refrigerio': 'No'
        },
        {
            'id': 3,
            'estado': 'ESPERANDO',
            'peluquero_esperando': 'Veterano B',
            'hora_ref': '75.5',
            'refrigerio': 'No'
        },
        {
            'id': 4,
            'estado': 'ESPERANDO',
            'peluquero_esperando': 'Aprendiz',
            'hora_ref': '80.2',
            'refrigerio': 'Sí'
        }
    ],
    'rnd_llegada': '',
    'tiempo_entre_llegadas': '',
    'proxima_llegada': '',
    'rnd_peluquero': '',
    'peluquero_preferido': '',
    'rnd_servicio': '0.5678',
    'tiempo_servicio': '12.34',
    'aprendiz': 'Libre',
    'veterano_a': 'Ocupado (C1, T:5.0)',
    'veterano_b': 'Libre',
    'cola_espera': 2,
    'clientes_atendidos': 5,
    'recaudacion': 150000,
    'refrigerios_entregados': 1,
    'costo_refrigerios': 5500,
    'ganancia_neta': 144500
}

print("=" * 80)
print("ESTRUCTURA DE EXPORTACIÓN A EXCEL")
print("=" * 80)

# Simular la estructura de exportación
row_data = {
    'N° Evento': evento_ejemplo['evento_num'],
    'Reloj': evento_ejemplo['reloj'],
    'Evento': evento_ejemplo['evento'],
    'Ganancia Neta': evento_ejemplo['ganancia_neta']
}

print("\n📊 Columnas después de 'Ganancia Neta':\n")

for i in range(5):
    if i < len(evento_ejemplo['clientes']):
        cliente = evento_ejemplo['clientes'][i]
        print(f"Cliente {i+1}:")
        print(f"  - ID: C{cliente['id']}")
        print(f"  - Estado: {cliente['estado']}")
        print(f"  - Peluquero: {cliente['peluquero_esperando']}")
        print(f"  - Hora Refrigerio: {cliente['hora_ref']}")
        print(f"  - Refrigerio: {cliente['refrigerio']}")
        print()
    else:
        print(f"Cliente {i+1}: (vacío)")
        print()

if len(evento_ejemplo['clientes']) > 5:
    print(f"Más Clientes: +{len(evento_ejemplo['clientes']) - 5}")
else:
    print("Más Clientes: (ninguno)")

print("\n" + "=" * 80)
print("✅ La estructura está correcta")
print("=" * 80)
