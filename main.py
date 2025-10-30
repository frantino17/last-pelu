import sys
import random
import numpy as np
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QTabWidget,
                             QTextEdit, QGroupBox, QSpinBox, QDoubleSpinBox,
                             QHeaderView, QMessageBox, QCheckBox, QGridLayout,
                             QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class PeluqueriaVIPSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.simulation_data = []
        self.last_simulation_results = None  # Para guardar los resultados
        self.last_simulation_params = None   # Para guardar los parámetros
        
    def initUI(self):
        self.setWindowTitle('Simulación de Peluquería VIP - Eventos Discretos (CORREGIDA)')
        self.setGeometry(100, 100, 2000, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # ===== PARÁMETROS INGRESABLES =====
        parameters_group = QGroupBox("Parámetros de la Peluquería")
        parameters_layout = QGridLayout()
        
        # Tiempos de servicio
        parameters_layout.addWidget(QLabel("Aprendiz - Tiempo min (min):"), 0, 0)
        self.aprendiz_min = QDoubleSpinBox()
        self.aprendiz_min.setRange(1, 100)
        self.aprendiz_min.setValue(20)
        parameters_layout.addWidget(self.aprendiz_min, 0, 1)
        
        parameters_layout.addWidget(QLabel("Aprendiz - Tiempo max (min):"), 0, 2)
        self.aprendiz_max = QDoubleSpinBox()
        self.aprendiz_max.setRange(1, 100)
        self.aprendiz_max.setValue(30)
        parameters_layout.addWidget(self.aprendiz_max, 0, 3)
        
        parameters_layout.addWidget(QLabel("Veterano A - Tiempo min (min):"), 1, 0)
        self.vetA_min = QDoubleSpinBox()
        self.vetA_min.setRange(1, 100)
        self.vetA_min.setValue(11)
        parameters_layout.addWidget(self.vetA_min, 1, 1)
        
        parameters_layout.addWidget(QLabel("Veterano A - Tiempo max (min):"), 1, 2)
        self.vetA_max = QDoubleSpinBox()
        self.vetA_max.setRange(1, 100)
        self.vetA_max.setValue(13)
        parameters_layout.addWidget(self.vetA_max, 1, 3)
        
        parameters_layout.addWidget(QLabel("Veterano B - Tiempo min (min):"), 2, 0)
        self.vetB_min = QDoubleSpinBox()
        self.vetB_min.setRange(1, 100)
        self.vetB_min.setValue(12)
        parameters_layout.addWidget(self.vetB_min, 2, 1)
        
        parameters_layout.addWidget(QLabel("Veterano B - Tiempo max (min):"), 2, 2)
        self.vetB_max = QDoubleSpinBox()
        self.vetB_max.setRange(1, 100)
        self.vetB_max.setValue(18)
        parameters_layout.addWidget(self.vetB_max, 2, 3)
        
        # Tiempos entre llegadas
        parameters_layout.addWidget(QLabel("Llegadas - Tiempo min (min):"), 3, 0)
        self.llegada_min = QDoubleSpinBox()
        self.llegada_min.setRange(1, 100)
        self.llegada_min.setValue(2)
        parameters_layout.addWidget(self.llegada_min, 3, 1)
        
        parameters_layout.addWidget(QLabel("Llegadas - Tiempo max (min):"), 3, 2)
        self.llegada_max = QDoubleSpinBox()
        self.llegada_max.setRange(1, 100)
        self.llegada_max.setValue(12)
        parameters_layout.addWidget(self.llegada_max, 3, 3)
        
        # Porcentajes de preferencia
        parameters_layout.addWidget(QLabel("% Preferencia Aprendiz:"), 4, 0)
        self.porc_aprendiz = QDoubleSpinBox()
        self.porc_aprendiz.setRange(0, 100)
        self.porc_aprendiz.setValue(15)
        parameters_layout.addWidget(self.porc_aprendiz, 4, 1)
        
        parameters_layout.addWidget(QLabel("% Preferencia Veterano A:"), 4, 2)
        self.porc_vetA = QDoubleSpinBox()
        self.porc_vetA.setRange(0, 100)
        self.porc_vetA.setValue(45)
        parameters_layout.addWidget(self.porc_vetA, 4, 3)
        
        parameters_layout.addWidget(QLabel("% Preferencia Veterano B:"), 5, 0)
        self.porc_vetB = QDoubleSpinBox()
        self.porc_vetB.setRange(0, 100)
        self.porc_vetB.setValue(40)
        parameters_layout.addWidget(self.porc_vetB, 5, 1)
        
        # Precios y costos
        parameters_layout.addWidget(QLabel("Precio Aprendiz ($):"), 5, 2)
        self.precio_aprendiz = QDoubleSpinBox()
        self.precio_aprendiz.setRange(0, 100000)
        self.precio_aprendiz.setValue(18000)
        parameters_layout.addWidget(self.precio_aprendiz, 5, 3)
        
        parameters_layout.addWidget(QLabel("Precio Veteranos ($):"), 6, 0)
        self.precio_veteranos = QDoubleSpinBox()
        self.precio_veteranos.setRange(0, 100000)
        self.precio_veteranos.setValue(32500)
        parameters_layout.addWidget(self.precio_veteranos, 6, 1)
        
        parameters_layout.addWidget(QLabel("Costo Refrigerio ($):"), 6, 2)
        self.costo_refrigerio = QDoubleSpinBox()
        self.costo_refrigerio.setRange(0, 100000)
        self.costo_refrigerio.setValue(5500)
        parameters_layout.addWidget(self.costo_refrigerio, 6, 3)
        
        parameters_layout.addWidget(QLabel("Tiempo límite refrigerio (min):"), 7, 0)
        self.tiempo_refrigerio = QDoubleSpinBox()
        self.tiempo_refrigerio.setRange(0, 1000)
        self.tiempo_refrigerio.setValue(30)
        parameters_layout.addWidget(self.tiempo_refrigerio, 7, 1)
        
        parameters_layout.addWidget(QLabel("Horas de atención (horas):"), 7, 2)
        self.horas_atencion = QDoubleSpinBox()
        self.horas_atencion.setRange(1, 24)
        self.horas_atencion.setValue(8)
        parameters_layout.addWidget(self.horas_atencion, 7, 3)
        
        parameters_group.setLayout(parameters_layout)
        layout.addWidget(parameters_group)
        
        # ===== PARÁMETROS DE SIMULACIÓN =====
        sim_group = QGroupBox("Parámetros de Simulación")
        sim_layout = QHBoxLayout()
        
        sim_layout.addWidget(QLabel("Número de días a simular:"))
        self.days_input = QSpinBox()
        self.days_input.setRange(1, 10000)
        self.days_input.setValue(100)
        sim_layout.addWidget(self.days_input)
        
        sim_layout.addWidget(QLabel("Desde evento N°:"))
        self.start_event_input = QSpinBox()
        self.start_event_input.setRange(1, 10000)
        self.start_event_input.setValue(1)
        sim_layout.addWidget(self.start_event_input)
        
        sim_layout.addWidget(QLabel("Cantidad de eventos a mostrar:"))
        self.iterations_input = QSpinBox()
        self.iterations_input.setRange(1, 1000)
        self.iterations_input.setValue(20)
        sim_layout.addWidget(self.iterations_input)
        
        self.simulate_button = QPushButton("Ejecutar Simulación")
        self.simulate_button.clicked.connect(self.run_simulation)
        sim_layout.addWidget(self.simulate_button)
        
        self.export_button = QPushButton("Exportar a Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        self.export_button.setEnabled(False)
        sim_layout.addWidget(self.export_button)
        
        sim_group.setLayout(sim_layout)
        layout.addWidget(sim_group)
        
        # ===== RESULTADOS =====
        self.tabs = QTabWidget()
        
        # Tabla de eventos discretos
        self.events_table = QTableWidget()
        self.tabs.addTab(self.events_table, "Vector de Estado - Eventos Discretos")
        
        # Resultados estadísticos
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.tabs.addTab(self.results_text, "Resultados")
        
        layout.addWidget(self.tabs)
        
    def get_parameters(self):
        """Obtiene todos los parámetros ingresados"""
        return {
            'aprendiz_min': self.aprendiz_min.value(),
            'aprendiz_max': self.aprendiz_max.value(),
            'vetA_min': self.vetA_min.value(),
            'vetA_max': self.vetA_max.value(),
            'vetB_min': self.vetB_min.value(),
            'vetB_max': self.vetB_max.value(),
            'llegada_min': self.llegada_min.value(),
            'llegada_max': self.llegada_max.value(),
            'porc_aprendiz': self.porc_aprendiz.value() / 100,
            'porc_vetA': self.porc_vetA.value() / 100,
            'porc_vetB': self.porc_vetB.value() / 100,
            'precio_aprendiz': self.precio_aprendiz.value(),
            'precio_veteranos': self.precio_veteranos.value(),
            'costo_refrigerio': self.costo_refrigerio.value(),
            'tiempo_refrigerio': self.tiempo_refrigerio.value(),
            'horas_atencion': self.horas_atencion.value()
        }
    
    def run_simulation(self):
        try:
            n_days = self.days_input.value()
            start_event = self.start_event_input.value()
            iterations = self.iterations_input.value()
            params = self.get_parameters()
            
            # Ejecutar simulación para N días
            daily_results = []
            
            for day in range(n_days):
                day_result = self.simulate_day(day, start_event, iterations, params)
                daily_results.append(day_result)
                
                # Mostrar vector de estado del primer día
                if day == 0:
                    self.display_events_table(day_result['events_log'], start_event, iterations)
            
            # Calcular estadísticas finales
            self.display_final_results(daily_results, n_days, params)
            
            # Guardar resultados para exportar
            self.last_simulation_results = {
                'daily_results': daily_results,
                'n_days': n_days,
                'first_day_events': daily_results[0]['events_log'] if daily_results else [],
                'params': params,
                'start_event': start_event,
                'iterations': iterations
            }
            self.last_simulation_params = params
            self.export_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}\n\n{str(type(e).__name__)}")
    
    def simulate_day(self, day_num, start_event, iterations, params):
        # Inicializar sistema
        clock = 0
        total_revenue = 0
        total_refreshments_cost = 0
        refreshments_given = 0
        max_waiting_clients = 0
        
        # Peluqueros
        barbers = [
            {'name': 'Aprendiz', 'index': 0, 'busy': False, 'service_end': None, 'customer': None, 
             'price': params['precio_aprendiz'], 'servicios_completados': 0},
            {'name': 'Veterano A', 'index': 1, 'busy': False, 'service_end': None, 'customer': None, 
             'price': params['precio_veteranos'], 'servicios_completados': 0},
            {'name': 'Veterano B', 'index': 2, 'busy': False, 'service_end': None, 'customer': None, 
             'price': params['precio_veteranos'], 'servicios_completados': 0}
        ]
        
        # Cola única FIFO
        waiting_queue = []
        served_customers = []
        all_customers = {}
        
        # Log de eventos
        events_log = []
        
        # Contadores
        customer_counter = 1
        event_counter = 0
        end_time = params['horas_atencion'] * 60
        
        # ===== EVENTO INICIAL =====
        event_counter += 1
        
        # Generar primera llegada en la fila de INICIO
        rnd_llegada_inicial = random.random()
        tiempo_primera_llegada = params['llegada_min'] + (params['llegada_max'] - params['llegada_min']) * rnd_llegada_inicial
        next_arrival_time = clock + tiempo_primera_llegada
        
        init_event = {'type': 'INICIO', 'time': 0, 'event_num': event_counter, 
                     'rnd_llegada': rnd_llegada_inicial, 'proxima_llegada': next_arrival_time}
        init_record = self.record_event(clock, init_event, barbers, waiting_queue, 
                                      served_customers, total_revenue, 
                                      refreshments_given, total_refreshments_cost, 
                                      all_customers, params, 
                                      {'rnd_llegada': rnd_llegada_inicial, 'proxima_llegada': next_arrival_time})
        events_log.append(init_record)
        
        # Programar primera llegada
        event_counter += 1
        future_events = [
            {'type': 'LLEGADA', 'time': next_arrival_time, 'customer_id': 1, 
             'rnd_llegada': rnd_llegada_inicial, 'event_num': event_counter}
        ]
        
        # Bucle principal de simulación
        while True:
            # Verificar si hay eventos futuros
            if not future_events:
                # Si no hay eventos y no hay clientes siendo atendidos, terminar
                if not any(barber['busy'] for barber in barbers):
                    break
                else:
                    # Hay clientes siendo atendidos pero no hay eventos programados
                    # Esto no debería pasar, pero por seguridad rompemos
                    break
            
            # Ordenar eventos por tiempo
            future_events.sort(key=lambda x: (x['time'], x['event_num']))
            next_event = future_events.pop(0)
            clock = next_event['time']
            event_counter = next_event['event_num']
            
            # Procesar según tipo de evento
            if next_event['type'] == 'LLEGADA':
                customer_id = next_event['customer_id']
                
                # Determinar preferencia de peluquero
                rnd_peluquero = random.random()
                if rnd_peluquero <= params['porc_aprendiz']:
                    preferred_barber = 0
                elif rnd_peluquero <= params['porc_aprendiz'] + params['porc_vetA']:
                    preferred_barber = 1
                else:
                    preferred_barber = 2
                
                # Crear cliente
                customer = {
                    'id': customer_id,
                    'arrival_time': clock,
                    'preferred_barber': preferred_barber,
                    'rnd_peluquero': rnd_peluquero,
                    'start_service_time': None,
                    'end_service_time': None,
                    'got_refreshment': False,
                    'refrigerio_time': None,
                    'refrigerio_programado': False,
                    'barber_served_by': None,
                    'service_time': None,
                    'rnd_servicio': None
                }
                
                all_customers[customer_id] = customer
                
                # Calcular tiempo entre llegadas
                if customer_id > 1:
                    tiempo_entre_llegadas = clock - all_customers[customer_id-1]['arrival_time']
                else:
                    tiempo_entre_llegadas = clock  # Para el primer cliente
                
                # Programar próxima llegada ANTES de registrar el evento
                proxima_llegada = None
                if clock < end_time:
                    customer_counter += 1
                    event_counter += 1
                    rnd_llegada = random.random()
                    tiempo_entre_llegadas_futuro = params['llegada_min'] + (params['llegada_max'] - params['llegada_min']) * rnd_llegada
                    proxima_llegada = clock + tiempo_entre_llegadas_futuro
                    future_events.append({
                        'type': 'LLEGADA',
                        'time': proxima_llegada,
                        'customer_id': customer_counter,
                        'rnd_llegada': rnd_llegada,
                        'event_num': event_counter
                    })
                
                # Verificar si el peluquero preferido está libre
                if not barbers[preferred_barber]['busy']:
                    # Atender inmediatamente
                    self.start_service(customer, preferred_barber, clock, barbers, 
                                     future_events, params, event_counter)
                else:
                    # Agregar a cola de espera
                    waiting_queue.append(customer)
                    
                    # PROGRAMAR EVENTO DE REFRIGERIO para este cliente
                    event_counter += 1
                    refrigerio_time = clock + params['tiempo_refrigerio']
                    customer['refrigerio_time'] = refrigerio_time
                    customer['refrigerio_programado'] = True
                    
                    future_events.append({
                        'type': 'REFRIGERIO',
                        'time': refrigerio_time,
                        'customer_id': customer_id,
                        'event_num': event_counter
                    })
                
                # Registrar evento con la información COMPLETA de la próxima llegada
                eventos_adicionales = {
                    'rnd_llegada': next_event['rnd_llegada'],
                    'rnd_peluquero': rnd_peluquero,
                    'peluquero_preferido': barbers[preferred_barber]['name'],
                    'tiempo_entre_llegadas': tiempo_entre_llegadas,
                    'proxima_llegada': proxima_llegada
                }
                
                if day_num == 0:
                    event_record = self.record_event(clock, next_event, barbers, waiting_queue, 
                                                   served_customers, total_revenue, 
                                                   refreshments_given, total_refreshments_cost,
                                                   all_customers, params, eventos_adicionales)
                    events_log.append(event_record)
            
            elif next_event['type'] == 'FIN_SERVICIO':
                barber_index = next_event['barber_index']
                customer_id = next_event['customer_id']
                
                # Finalizar servicio
                customer = barbers[barber_index]['customer']
                customer['end_service_time'] = clock
                total_revenue += barbers[barber_index]['price']
                barbers[barber_index]['servicios_completados'] += 1
                served_customers.append(customer.copy())
                
                # Liberar peluquero
                barbers[barber_index]['busy'] = False
                barbers[barber_index]['service_end'] = None
                barbers[barber_index]['customer'] = None
                
                # Buscar próximo cliente en la cola que prefiera este peluquero
                next_customer = None
                for i, cust in enumerate(waiting_queue):
                    if cust['preferred_barber'] == barber_index:
                        next_customer = waiting_queue.pop(i)
                        break
                
                if next_customer:
                    # Atender siguiente cliente
                    self.start_service(next_customer, barber_index, clock, barbers, 
                                     future_events, params, event_counter)
                
                # Registrar evento
                eventos_adicionales = {
                    'cliente_atendido': customer_id,
                    'peluquero': barbers[barber_index]['name'],
                    'precio_cobrado': barbers[barber_index]['price']
                }
                if day_num == 0:
                    event_record = self.record_event(clock, next_event, barbers, waiting_queue, 
                                                   served_customers, total_revenue, 
                                                   refreshments_given, total_refreshments_cost,
                                                   all_customers, params, eventos_adicionales)
                    events_log.append(event_record)
            
            elif next_event['type'] == 'REFRIGERIO':
                customer_id = next_event['customer_id']
                
                # Verificar que el cliente aún esté en espera y no haya recibido refrigerio
                customer_in_queue = None
                for cust in waiting_queue:
                    if cust['id'] == customer_id:
                        customer_in_queue = cust
                        break
                
                # Solo dar refrigerio si el cliente está en cola (no si ya está siendo atendido)
                if customer_in_queue and not customer_in_queue['got_refreshment']:
                    customer_in_queue['got_refreshment'] = True
                    all_customers[customer_id]['got_refreshment'] = True
                    refreshments_given += 1
                    total_refreshments_cost += params['costo_refrigerio']
                    
                    # Registrar evento
                    eventos_adicionales = {
                        'cliente_refrigerio': customer_id,
                        'costo': params['costo_refrigerio'],
                        'tiempo_espera': clock - customer_in_queue['arrival_time']
                    }
                    if day_num == 0:
                        event_record = self.record_event(clock, next_event, barbers, waiting_queue, 
                                                       served_customers, total_revenue, 
                                                       refreshments_given, total_refreshments_cost,
                                                       all_customers, params, eventos_adicionales)
                        events_log.append(event_record)
            
            # Actualizar máximo de clientes en espera
            max_waiting_clients = max(max_waiting_clients, len(waiting_queue))
        
        return {
            'total_revenue': total_revenue,
            'refreshments_given': refreshments_given,
            'refreshments_cost': total_refreshments_cost,
            'max_waiting_clients': max_waiting_clients,
            'customers_served': len(served_customers),
            'events_log': events_log,
            'barbers_stats': [b['servicios_completados'] for b in barbers]
        }
    
    def start_service(self, customer, barber_index, clock, barbers, future_events, params, event_counter):
        """Inicia el servicio de un cliente con un peluquero"""
        # Generar tiempo de servicio
        rnd_servicio = random.random()
        if barber_index == 0:  # Aprendiz
            service_time = params['aprendiz_min'] + (params['aprendiz_max'] - params['aprendiz_min']) * rnd_servicio
        elif barber_index == 1:  # Veterano A
            service_time = params['vetA_min'] + (params['vetA_max'] - params['vetA_min']) * rnd_servicio
        else:  # Veterano B
            service_time = params['vetB_min'] + (params['vetB_max'] - params['vetB_min']) * rnd_servicio
        
        customer['start_service_time'] = clock
        customer['service_time'] = service_time
        customer['rnd_servicio'] = rnd_servicio
        customer['barber_served_by'] = barber_index
        
        barbers[barber_index]['busy'] = True
        barbers[barber_index]['service_end'] = clock + service_time
        barbers[barber_index]['customer'] = customer
        
        # Programar fin de servicio
        event_counter += 1
        future_events.append({
            'type': 'FIN_SERVICIO',
            'time': clock + service_time,
            'barber_index': barber_index,
            'customer_id': customer['id'],
            'event_num': event_counter
        })
    
    def record_event(self, clock, event, barbers, waiting_queue, served_customers, 
                    total_revenue, refreshments_given, total_refreshments_cost,
                    all_customers, params, eventos_adicionales):
        """Registra el estado del sistema en un evento"""
        record = {
            'evento_num': event.get('event_num', 0),
            'reloj': clock,
            'evento': event['type'],
            'rnd_llegada': '',
            'tiempo_entre_llegadas': '',
            'proxima_llegada': '',
            'rnd_peluquero': '',
            'peluquero_preferido': '',
            'rnd_servicio': '',
            'tiempo_servicio': '',
            'aprendiz': '',
            'veterano_a': '',
            'veterano_b': '',
            'cola_espera': len(waiting_queue),
            'clientes_atendidos': len(served_customers),
            'recaudacion': total_revenue,
            'refrigerios_entregados': refreshments_given,
            'costo_refrigerios': total_refreshments_cost,
            'ganancia_neta': total_revenue - total_refreshments_cost,
            'clientes': [],  # Lista para almacenar información de cada cliente
            'espera_promedio': 0,
            'clientes_con_refrigerio': 0
        }
        
        # Información específica del evento
        if event['type'] == 'INICIO' and eventos_adicionales:
            record['rnd_llegada'] = f"{eventos_adicionales.get('rnd_llegada', ''):.4f}" if eventos_adicionales.get('rnd_llegada') else ''
            record['proxima_llegada'] = f"{eventos_adicionales.get('proxima_llegada', ''):.2f}" if eventos_adicionales.get('proxima_llegada') else ''
            record['tiempo_entre_llegadas'] = ''  # En INICIO no hay tiempo entre llegadas
        
        elif event['type'] == 'LLEGADA' and eventos_adicionales:
            record['rnd_llegada'] = f"{eventos_adicionales.get('rnd_llegada', ''):.4f}" if eventos_adicionales.get('rnd_llegada') else ''
            record['tiempo_entre_llegadas'] = f"{eventos_adicionales.get('tiempo_entre_llegadas', ''):.2f}" if eventos_adicionales.get('tiempo_entre_llegadas') else ''
            record['proxima_llegada'] = f"{eventos_adicionales.get('proxima_llegada', ''):.2f}" if eventos_adicionales.get('proxima_llegada') else ''
            record['rnd_peluquero'] = f"{eventos_adicionales.get('rnd_peluquero', ''):.4f}" if eventos_adicionales.get('rnd_peluquero') else ''
            record['peluquero_preferido'] = eventos_adicionales.get('peluquero_preferido', '')
        
        elif event['type'] == 'FIN_SERVICIO' and eventos_adicionales:
            customer_id = eventos_adicionales.get('cliente_atendido')
            if customer_id and customer_id in all_customers:
                customer = all_customers[customer_id]
                record['rnd_servicio'] = f"{customer.get('rnd_servicio', ''):.4f}" if customer.get('rnd_servicio') else ''
                record['tiempo_servicio'] = f"{customer.get('service_time', ''):.2f}" if customer.get('service_time') else ''
        
        elif event['type'] == 'REFRIGERIO' and eventos_adicionales:
            # Para eventos de refrigerio, no hay información de llegadas
            pass
        
        # Estado de peluqueros
        for i, barber in enumerate(barbers):
            if barber['busy']:
                tiempo_restante = barber['service_end'] - clock if barber['service_end'] else 0
                estado = f"Ocupado (C{barber['customer']['id']}, T:{tiempo_restante:.1f})"
            else:
                estado = "Libre"
            
            if i == 0:
                record['aprendiz'] = estado
            elif i == 1:
                record['veterano_a'] = estado
            else:
                record['veterano_b'] = estado
        
        # Información detallada de cada cliente en cola
        total_espera = 0
        clientes_con_refrigerio = 0
        
        for customer in waiting_queue:
            tiempo_espera = clock - customer['arrival_time']
            total_espera += tiempo_espera
            
            cliente_info = {
                'id': customer['id'],
                'espera': f"{tiempo_espera:.1f}",
                'refrigerio': "Sí" if customer['got_refreshment'] else "No",
                'hora_ref': f"{customer.get('refrigerio_time', 'N/A'):.1f}" if isinstance(customer.get('refrigerio_time'), float) else str(customer.get('refrigerio_time', 'N/A'))
            }
            
            if customer['got_refreshment']:
                clientes_con_refrigerio += 1
            
            record['clientes'].append(cliente_info)
        
        # Calcular estadísticas de la cola
        if len(waiting_queue) > 0:
            record['espera_promedio'] = total_espera / len(waiting_queue)
        record['clientes_con_refrigerio'] = clientes_con_refrigerio
        
        return record
    
    def display_events_table(self, events_log, start_event, iterations):
        """Muestra la tabla de eventos"""
        # Filtrar eventos a mostrar
        end_event = min(start_event + iterations - 1, len(events_log))
        filtered_events = events_log[start_event-1:end_event]
        
        headers = ['N° Evento', 'Reloj', 'Evento', 'RND Llegada', 'Tiempo Entre Llegadas', 
                   'Próxima Llegada', 'RND Peluquero', 'Peluquero Preferido', 'RND Servicio', 
                   'Tiempo Servicio', 'Aprendiz', 'Veterano A', 'Veterano B', 'Cola', 'Atendidos',
                   'Recaudación', 'Refrigerios', 'Costo Ref', 'Ganancia Neta', 
                   'Cliente ID', 'Espera', 'Refrigerio', 'Hora Ref']
        
        self.events_table.setRowCount(len(filtered_events))
        self.events_table.setColumnCount(len(headers))
        self.events_table.setHorizontalHeaderLabels(headers)
        
        for row, event in enumerate(filtered_events):
            self.events_table.setItem(row, 0, QTableWidgetItem(str(event['evento_num'])))
            self.events_table.setItem(row, 1, QTableWidgetItem(f"{event['reloj']:.2f}"))
            self.events_table.setItem(row, 2, QTableWidgetItem(event['evento']))
            
            # RND Llegada
            val = event['rnd_llegada']
            self.events_table.setItem(row, 3, QTableWidgetItem(str(val)))
            
            # Tiempo Entre Llegadas
            val = event['tiempo_entre_llegadas']
            self.events_table.setItem(row, 4, QTableWidgetItem(str(val)))
            
            # Próxima Llegada
            val = event['proxima_llegada']
            self.events_table.setItem(row, 5, QTableWidgetItem(str(val)))
            
            # RND Peluquero
            val = event['rnd_peluquero']
            self.events_table.setItem(row, 6, QTableWidgetItem(str(val)))
            
            # Peluquero Preferido
            self.events_table.setItem(row, 7, QTableWidgetItem(str(event['peluquero_preferido'])))
            
            # RND Servicio
            val = event['rnd_servicio']
            self.events_table.setItem(row, 8, QTableWidgetItem(str(val)))
            
            # Tiempo Servicio
            val = event['tiempo_servicio']
            self.events_table.setItem(row, 9, QTableWidgetItem(str(val)))
            
            # Estados de peluqueros
            self.events_table.setItem(row, 10, QTableWidgetItem(str(event['aprendiz'])))
            self.events_table.setItem(row, 11, QTableWidgetItem(str(event['veterano_a'])))
            self.events_table.setItem(row, 12, QTableWidgetItem(str(event['veterano_b'])))
            
            # Estadísticas
            self.events_table.setItem(row, 13, QTableWidgetItem(str(event['cola_espera'])))
            self.events_table.setItem(row, 14, QTableWidgetItem(str(event['clientes_atendidos'])))
            self.events_table.setItem(row, 15, QTableWidgetItem(f"${event['recaudacion']:.2f}"))
            self.events_table.setItem(row, 16, QTableWidgetItem(str(event['refrigerios_entregados'])))
            self.events_table.setItem(row, 17, QTableWidgetItem(f"${event['costo_refrigerios']:.2f}"))
            self.events_table.setItem(row, 18, QTableWidgetItem(f"${event['ganancia_neta']:.2f}"))
            
            # Información de clientes - mostrar solo el primer cliente para no hacer la tabla demasiado ancha
            if event['clientes']:
                primer_cliente = event['clientes'][0]
                self.events_table.setItem(row, 19, QTableWidgetItem(f"C{primer_cliente['id']}"))
                self.events_table.setItem(row, 20, QTableWidgetItem(primer_cliente['espera']))
                self.events_table.setItem(row, 21, QTableWidgetItem(primer_cliente['refrigerio']))
                self.events_table.setItem(row, 22, QTableWidgetItem(primer_cliente['hora_ref']))
            else:
                self.events_table.setItem(row, 19, QTableWidgetItem(""))
                self.events_table.setItem(row, 20, QTableWidgetItem(""))
                self.events_table.setItem(row, 21, QTableWidgetItem(""))
                self.events_table.setItem(row, 22, QTableWidgetItem(""))
        
        # Ajustar tamaño de columnas
        header = self.events_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def display_final_results(self, daily_results, n_days, params):
        """Muestra los resultados finales de la simulación"""
        # Calcular estadísticas
        daily_revenues = [day['total_revenue'] for day in daily_results]
        max_clients = [day['max_waiting_clients'] for day in daily_results]
        refreshments_per_day = [day['refreshments_given'] for day in daily_results]
        refreshments_costs = [day['refreshments_cost'] for day in daily_results]
        
        # Ganancia neta (recaudación - costos de refrigerios)
        daily_net_profit = [rev - cost for rev, cost in zip(daily_revenues, refreshments_costs)]
        
        avg_revenue = np.mean(daily_revenues)
        avg_net_profit = np.mean(daily_net_profit)
        max_chairs_needed = max(max_clients)
        days_with_5_or_more = sum(1 for r in refreshments_per_day if r >= 5)
        prob_5_or_more = days_with_5_or_more / n_days
        
        # Estadísticas adicionales
        total_customers = sum(day['customers_served'] for day in daily_results)
        total_refreshments = sum(refreshments_per_day)
        total_refreshments_cost = sum(refreshments_costs)
        
        # Promedio de servicios por peluquero
        servicios_aprendiz = np.mean([day['barbers_stats'][0] for day in daily_results])
        servicios_vetA = np.mean([day['barbers_stats'][1] for day in daily_results])
        servicios_vetB = np.mean([day['barbers_stats'][2] for day in daily_results])
        
        # Desviaciones estándar
        std_revenue = np.std(daily_revenues)
        std_net_profit = np.std(daily_net_profit)
        
        # Valores máximos y mínimos
        min_revenue = min(daily_revenues)
        max_revenue = max(daily_revenues)
        min_net_profit = min(daily_net_profit)
        max_net_profit = max(daily_net_profit)
        
        results_text = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║           RESULTADOS DE LA SIMULACIÓN - PELUQUERÍA VIP                ║
╚═══════════════════════════════════════════════════════════════════════╝

Simulación de {n_days} días de trabajo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESPUESTAS A LAS PREGUNTAS DEL ENUNCIADO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  PROMEDIO DE RECAUDACIÓN DIARIA: ${avg_revenue:,.2f}
    • Desviación estándar: ${std_revenue:,.2f}
    • Recaudación mínima: ${min_revenue:,.2f}
    • Recaudación máxima: ${max_revenue:,.2f}

2️⃣  CANTIDAD DE SILLAS NECESARIAS: {max_chairs_needed} sillas
    • Máximo de clientes esperando simultáneamente: {max_chairs_needed}
    • Esto asegura que ningún cliente deba estar de pie

3️⃣  PROBABILIDAD DE 5+ REFRIGERIOS AL DÍA: {prob_5_or_more:.4f} ({prob_5_or_more*100:.2f}%)
    • Días con 5 o más refrigerios: {days_with_5_or_more} de {n_days}
    • Promedio de refrigerios por día: {total_refreshments/n_days:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 ANÁLISIS ECONÓMICO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ganancia Neta Diaria Promedio: ${avg_net_profit:,.2f}
  (Recaudación - Costo de Refrigerios)

• Desviación estándar ganancia neta: ${std_net_profit:,.2f}
• Ganancia neta mínima: ${min_net_profit:,.2f}
• Ganancia neta máxima: ${max_net_profit:,.2f}

Costos de Refrigerios:
• Total en {n_days} días: ${total_refreshments_cost:,.2f}
• Promedio por día: ${total_refreshments_cost/n_days:,.2f}
• Refrigerios entregados totales: {total_refreshments}
• Costo unitario: ${params['costo_refrigerio']:,.2f}

Proyección Mensual (30 días):
• Recaudación estimada: ${avg_revenue * 30:,.2f}
• Costo refrigerios estimado: ${(total_refreshments_cost/n_days) * 30:,.2f}
• Ganancia neta estimada: ${avg_net_profit * 30:,.2f}

Proyección Anual (365 días):
• Recaudación estimada: ${avg_revenue * 365:,.2f}
• Costo refrigerios estimado: ${(total_refreshments_cost/n_days) * 365:,.2f}
• Ganancia neta estimada: ${avg_net_profit * 365:,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 ESTADÍSTICAS DE CLIENTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Total de clientes atendidos: {total_customers}
• Promedio de clientes por día: {total_customers/n_days:.2f}
• Clientes que recibieron refrigerio: {total_refreshments}
• Porcentaje de clientes con refrigerio: {(total_refreshments/total_customers*100) if total_customers > 0 else 0:.2f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✂️  PRODUCTIVIDAD DE PELUQUEROS (Promedio por día):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Aprendiz: {servicios_aprendiz:.2f} servicios/día
  - Precio: ${params['precio_aprendiz']:,.2f}
  - Ingreso promedio: ${servicios_aprendiz * params['precio_aprendiz']:,.2f}/día

• Veterano A: {servicios_vetA:.2f} servicios/día
  - Precio: ${params['precio_veteranos']:,.2f}
  - Ingreso promedio: ${servicios_vetA * params['precio_veteranos']:,.2f}/día

• Veterano B: {servicios_vetB:.2f} servicios/día
  - Precio: ${params['precio_veteranos']:,.2f}
  - Ingreso promedio: ${servicios_vetB * params['precio_veteranos']:,.2f}/día

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️  PARÁMETROS DE LA SIMULACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tiempos de Servicio (minutos):
• Aprendiz: U({params['aprendiz_min']:.0f}, {params['aprendiz_max']:.0f})
• Veterano A: U({params['vetA_min']:.0f}, {params['vetA_max']:.0f})
• Veterano B: U({params['vetB_min']:.0f}, {params['vetB_max']:.0f})

Llegadas:
• Tiempo entre llegadas: U({params['llegada_min']:.0f}, {params['llegada_max']:.0f}) minutos

Preferencias de Clientes:
• Aprendiz: {params['porc_aprendiz']*100:.0f}%
• Veterano A: {params['porc_vetA']*100:.0f}%
• Veterano B: {params['porc_vetB']*100:.0f}%

Precios:
• Servicio Aprendiz: ${params['precio_aprendiz']:,.2f}
• Servicio Veteranos: ${params['precio_veteranos']:,.2f}

Política de Refrigerios:
• Se entrega después de: {params['tiempo_refrigerio']:.0f} minutos de espera
• Costo por refrigerio: ${params['costo_refrigerio']:,.2f}

Horario de Atención:
• {params['horas_atencion']:.0f} horas ({params['horas_atencion']*60:.0f} minutos)
• Se trabaja hasta atender todos los clientes que llegaron durante el horario

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 DISTRIBUCIÓN DE REFRIGERIOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Histograma de refrigerios
        from collections import Counter
        refrigerio_counts = Counter(refreshments_per_day)
        results_text += "\nDías con X refrigerios:\n"
        for count in sorted(refrigerio_counts.keys()):
            freq = refrigerio_counts[count]
            pct = (freq / n_days) * 100
            bar = '█' * int(pct / 2)
            results_text += f"  {count:2d} refrigerios: {freq:4d} días ({pct:5.2f}%) {bar}\n"
        
        results_text += "\n" + "═" * 75 + "\n"
        
        self.results_text.setText(results_text)
    
    def export_to_excel(self):
        """Exporta los resultados de la simulación a Excel"""
        if not self.last_simulation_results:
            QMessageBox.warning(self, "Advertencia", "Primero debe ejecutar una simulación")
            return
        
        try:
            # Abrir diálogo para guardar archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"simulacion_peluqueria_{timestamp}.xlsx"
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar simulación en Excel",
                default_filename,
                "Excel Files (*.xlsx);;All Files (*)"
            )
            
            if not filename:
                return  # Usuario canceló
            
            # Crear Excel con pandas
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Hoja 1: Vector de Estado (eventos del primer día)
                events_data = []
                for event in self.last_simulation_results['first_day_events']:
                    # Función auxiliar para formatear valores
                    def format_value(val, decimals=2):
                        if val == '' or val is None:
                            return ''
                        if isinstance(val, (int, float)):
                            return round(val, decimals)
                        return val
                    
                    row_data = {
                        'N° Evento': event['evento_num'],
                        'Reloj': format_value(event['reloj'], 2),
                        'Evento': event['evento'],
                        'RND Llegada': event['rnd_llegada'],
                        'Tiempo Entre Llegadas': event['tiempo_entre_llegadas'],
                        'Próxima Llegada': event['proxima_llegada'],
                        'RND Peluquero': event['rnd_peluquero'],
                        'Peluquero Preferido': event['peluquero_preferido'] if event['peluquero_preferido'] else '',
                        'RND Servicio': event['rnd_servicio'],
                        'Tiempo Servicio': event['tiempo_servicio'],
                        'Aprendiz': event['aprendiz'] if event['aprendiz'] else '',
                        'Veterano A': event['veterano_a'] if event['veterano_a'] else '',
                        'Veterano B': event['veterano_b'] if event['veterano_b'] else '',
                        'Cola': event['cola_espera'],
                        'Atendidos': event['clientes_atendidos'],
                        'Recaudación': format_value(event['recaudacion'], 2),
                        'Refrigerios': event['refrigerios_entregados'],
                        'Costo Ref': format_value(event['costo_refrigerios'], 2),
                        'Ganancia Neta': format_value(event['ganancia_neta'], 2)
                    }
                    
                    # Agregar información de clientes (hasta 5 clientes para no hacer la tabla demasiado ancha)
                    for i, cliente in enumerate(event['clientes'][:5]):
                        row_data[f'Cliente {i+1} ID'] = f"C{cliente['id']}"
                        row_data[f'Cliente {i+1} Espera'] = cliente['espera']
                        row_data[f'Cliente {i+1} Refrigerio'] = cliente['refrigerio']
                        row_data[f'Cliente {i+1} Hora Ref'] = cliente['hora_ref']
                    
                    # Si hay más de 5 clientes, agregar un campo para indicarlo
                    if len(event['clientes']) > 5:
                        row_data['Clientes Adicionales'] = f"+{len(event['clientes']) - 5} clientes más"
                    
                    events_data.append(row_data)
                
                df_events = pd.DataFrame(events_data)
                df_events.to_excel(writer, sheet_name='Vector de Estado', index=False)
                
                # Hoja 2: Resumen por día
                daily_data = []
                for i, day in enumerate(self.last_simulation_results['daily_results']):
                    daily_data.append({
                        'Día': i + 1,
                        'Recaudación': round(day['total_revenue'], 2),
                        'Costo Refrigerios': round(day['refreshments_cost'], 2),
                        'Ganancia Neta': round(day['total_revenue'] - day['refreshments_cost'], 2),
                        'Clientes Atendidos': day['customers_served'],
                        'Refrigerios Entregados': day['refreshments_given'],
                        'Max Clientes Esperando': day['max_waiting_clients'],
                        'Servicios Aprendiz': day['barbers_stats'][0],
                        'Servicios Veterano A': day['barbers_stats'][1],
                        'Servicios Veterano B': day['barbers_stats'][2]
                    })
                
                df_daily = pd.DataFrame(daily_data)
                df_daily.to_excel(writer, sheet_name='Resumen Diario', index=False)
                
                # Hoja 3: Estadísticas Finales
                params = self.last_simulation_results['params']
                daily_results = self.last_simulation_results['daily_results']
                n_days = self.last_simulation_results['n_days']
                
                daily_revenues = [day['total_revenue'] for day in daily_results]
                refreshments_per_day = [day['refreshments_given'] for day in daily_results]
                max_clients = [day['max_waiting_clients'] for day in daily_results]
                daily_net_profit = [day['total_revenue'] - day['refreshments_cost'] for day in daily_results]
                
                stats_data = {
                    'Métrica': [
                        'Días Simulados',
                        'Promedio Recaudación Diaria',
                        'Desv. Std. Recaudación',
                        'Recaudación Mínima',
                        'Recaudación Máxima',
                        '',
                        'Promedio Ganancia Neta Diaria',
                        'Desv. Std. Ganancia Neta',
                        'Ganancia Neta Mínima',
                        'Ganancia Neta Máxima',
                        '',
                        'Sillas Necesarias',
                        'Probabilidad 5+ Refrigerios',
                        'Días con 5+ Refrigerios',
                        '',
                        'Total Clientes Atendidos',
                        'Promedio Clientes por Día',
                        'Total Refrigerios Entregados',
                        'Promedio Refrigerios por Día',
                        '',
                        'Servicios Promedio Aprendiz/Día',
                        'Servicios Promedio Veterano A/Día',
                        'Servicios Promedio Veterano B/Día'
                    ],
                    'Valor': [
                        n_days,
                        f"${np.mean(daily_revenues):,.2f}",
                        f"${np.std(daily_revenues):,.2f}",
                        f"${min(daily_revenues):,.2f}",
                        f"${max(daily_revenues):,.2f}",
                        '',
                        f"${np.mean(daily_net_profit):,.2f}",
                        f"${np.std(daily_net_profit):,.2f}",
                        f"${min(daily_net_profit):,.2f}",
                        f"${max(daily_net_profit):,.2f}",
                        '',
                        max(max_clients),
                        f"{sum(1 for r in refreshments_per_day if r >= 5) / n_days:.4f}",
                        sum(1 for r in refreshments_per_day if r >= 5),
                        '',
                        sum(day['customers_served'] for day in daily_results),
                        f"{sum(day['customers_served'] for day in daily_results) / n_days:.2f}",
                        sum(refreshments_per_day),
                        f"{sum(refreshments_per_day) / n_days:.2f}",
                        '',
                        f"{np.mean([day['barbers_stats'][0] for day in daily_results]):.2f}",
                        f"{np.mean([day['barbers_stats'][1] for day in daily_results]):.2f}",
                        f"{np.mean([day['barbers_stats'][2] for day in daily_results]):.2f}"
                    ]
                }
                
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Estadísticas Finales', index=False)
                
                # Hoja 4: Parámetros de Simulación
                params_data = {
                    'Parámetro': [
                        'Aprendiz - Tiempo Min (min)',
                        'Aprendiz - Tiempo Max (min)',
                        'Veterano A - Tiempo Min (min)',
                        'Veterano A - Tiempo Max (min)',
                        'Veterano B - Tiempo Min (min)',
                        'Veterano B - Tiempo Max (min)',
                        '',
                        'Llegadas - Tiempo Min (min)',
                        'Llegadas - Tiempo Max (min)',
                        '',
                        '% Preferencia Aprendiz',
                        '% Preferencia Veterano A',
                        '% Preferencia Veterano B',
                        '',
                        'Precio Aprendiz',
                        'Precio Veteranos',
                        'Costo Refrigerio',
                        'Tiempo Límite Refrigerio (min)',
                        'Horas de Atención'
                    ],
                    'Valor': [
                        params['aprendiz_min'],
                        params['aprendiz_max'],
                        params['vetA_min'],
                        params['vetA_max'],
                        params['vetB_min'],
                        params['vetB_max'],
                        '',
                        params['llegada_min'],
                        params['llegada_max'],
                        '',
                        f"{params['porc_aprendiz']*100:.0f}%",
                        f"{params['porc_vetA']*100:.0f}%",
                        f"{params['porc_vetB']*100:.0f}%",
                        '',
                        f"${params['precio_aprendiz']:,.2f}",
                        f"${params['precio_veteranos']:,.2f}",
                        f"${params['costo_refrigerio']:,.2f}",
                        params['tiempo_refrigerio'],
                        params['horas_atencion']
                    ]
                }
                
                df_params = pd.DataFrame(params_data)
                df_params.to_excel(writer, sheet_name='Parámetros', index=False)
                
                # Ajustar ancho de columnas
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
            
            QMessageBox.information(self, "Éxito", f"Simulación exportada exitosamente a:\n{filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar a Excel:\n{str(e)}\n\n{str(type(e).__name__)}")


def main():
    app = QApplication(sys.argv)
    simulator = PeluqueriaVIPSimulator()
    simulator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()