import pytest
import json
from json_sender import send_pedido

def test_json_serialization(mocker):
    # Mock de la conexión de stomp para no requerir el servidor real
    mock_conn = mocker.patch('stomp.Connection')
    
    datos_prueba = {
        "id_pedido": 1,
        "cliente": "Test User",
        "productos": [],
        "total": 100,
        "metodo_pago": "tarjeta"
    }
    
    # Ejecutar la función
    resultado = send_pedido(datos_prueba)
    
    # Verificaciones (Assertions)
    assert resultado is True
    # Verificar que se llamó a send con un string (JSON) y no con un diccionario
    args, kwargs = mock_conn.return_value.send.call_args
    assert isinstance(kwargs['body'], str)
    assert "id_pedido" in kwargs['body']

def test_sender_failure(mocker):
    # Simular un error de conexión
    mock_conn = mocker.patch('stomp.Connection')
    mock_conn.return_value.connect.side_effect = Exception("Connection Refused")
    
    resultado = send_pedido({"data": "test"})
    
    assert resultado is False