"""  import pytest
import json
from json_receiver_v2 import RoutingListener

# Clase ficticia para simular el 'frame' que envía ActiveMQ
class MockFrame:
    def __init__(self, body):
        self.body = body

def test_routing_to_error_queue_on_invalid_json(mocker):
    # 1. Creamos un Mock de la conexión
    mock_conn = mocker.Mock()
    
    # 2. Instanciamos el Listener con el mock
    listener = RoutingListener(mock_conn)
    
    # 3. Creamos un JSON inválido (falta 'metodo_pago' y 'total')
    invalid_payload = json.dumps({
        "id_pedido": 999,
        "cliente": "Usuario Error",
        "productos": []
    })
    frame = MockFrame(invalid_payload)

    # 4. Ejecutamos manualmente el método on_message
    listener.on_message(frame)

    # 5. VERIFICACIÓN: ¿Se llamó al método send hacia la cola de errores?
    # Buscamos en los argumentos del mock si el destino fue la cola de errores
    mock_conn.send.assert_called_once()
    args, kwargs = mock_conn.send.call_args
    
    assert kwargs['destination'] == '/queue/PedidosErrores'
    assert 'error' in kwargs['headers']
    print("\n[✔] Prueba exitosa: El mensaje fallido fue enrutado a la cola de errores.")

def test_no_routing_on_valid_json(mocker):
    mock_conn = mocker.Mock()
    listener = RoutingListener(mock_conn)
    
    valid_payload = json.dumps({
        "id_pedido": 1,
        "cliente": "Victor Hugo",
        "productos": [],
        "total": 100,
        "metodo_pago": "tarjeta"
    })
    frame = MockFrame(valid_payload)

    listener.on_message(frame)

    # VERIFICACIÓN: El método send NO debe llamarse si el JSON es correcto
    assert mock_conn.send.call_count == 0
    print("[✔] Prueba exitosa: El mensaje válido NO fue re-enrutado.")
"""

import pytest
import json
import os
from json_receiver import RoutingListener

# Helper para cargar los archivos de la carpeta assets
def get_asset(filename):
    # Obtiene la ruta absoluta de /app/assets/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el asset en: {file_path}")
        
    with open(file_path, 'r') as f:
        return f.read()

class MockFrame:
    def __init__(self, body):
        self.body = body

def test_routing_with_valid_asset(mocker):
    mock_conn = mocker.Mock()
    listener = RoutingListener(mock_conn)
    
    # CARGA DESDE ASSET
    raw_json = get_asset('pedido_valido.json')
    frame = MockFrame(raw_json)

    listener.on_message(frame)

    # Verificación: No debe haber ruteo a errores
    assert mock_conn.send.call_count == 0

def test_routing_with_invalid_asset(mocker):
    mock_conn = mocker.Mock()
    listener = RoutingListener(mock_conn)
    
    # CARGA DESDE ASSET
    raw_json = get_asset('pedido_invalido.json')
    frame = MockFrame(raw_json)

    listener.on_message(frame)

    # Verificación: Debe haberse enviado a la cola de errores
    mock_conn.send.assert_called_once()
    _, kwargs = mock_conn.send.call_args
    assert kwargs['destination'] == os.getenv('QUEUE_ERRORES', '/queue/PedidosErrores')