import pytest
import json
import os
from json_receiver import RoutingListener

# Helper para cargar assets
def get_asset(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_dir, 'assets', filename), 'r') as f:
        return f.read()

class MockFrame:
    def __init__(self, body):
        self.body = body

def test_valida_y_no_ruta_si_es_correcto(mocker):
    mock_conn = mocker.Mock()
    listener = RoutingListener(mock_conn)
    frame = MockFrame(get_asset('pedido_valido.json'))

    listener.on_message(frame)

    # El mensaje es válido, no debe llamar a send (cola de errores)
    assert mock_conn.send.call_count == 0

def test_ruta_a_errores_si_es_invalido(mocker):
    mock_conn = mocker.Mock()
    listener = RoutingListener(mock_conn)
    frame = MockFrame(get_asset('pedido_invalido.json'))

    listener.on_message(frame)

    # Debe llamar a send para moverlo a la cola de errores
    mock_conn.send.assert_called_once()
    _, kwargs = mock_conn.send.call_args
    assert kwargs['destination'] == '/queue/PedidosErrores'