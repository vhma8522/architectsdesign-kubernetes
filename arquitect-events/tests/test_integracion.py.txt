import pytest
import stomp
import os
import time

def test_conexion_real_broker():
    host = os.getenv('BROKER_HOST', 'activemq')
    port = int(os.getenv('BROKER_PORT', 61613))
    
    conn = stomp.Connection([(host, port)])
    try:
        conn.connect('admin', 'admin', wait=True)
        assert conn.is_connected()
        conn.disconnect()
    except Exception as e:
        pytest.fail(f"No se pudo conectar al broker real: {e}")

def test_envio_recepcion_integracion():
    host = os.getenv('BROKER_HOST', 'activemq')
    conn = stomp.Connection([(host, 61613)])
    conn.connect('admin', 'admin', wait=True)
    
    test_msg = "Prueba de Integración"
    # Enviamos a una cola temporal de test
    conn.send(body=test_msg, destination='/queue/TestIntegracion')
    time.sleep(1) 
    
    # En integración real, aquí podrías tener un listener capturando esto
    conn.disconnect()