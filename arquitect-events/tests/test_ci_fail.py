import pytest
from json_receiver import RoutingListener

def test_failure_on_routing(mocker):
    """
    SIMULACIÓN DE FALLO:
    Este test forzará un error al validar el ruteo. 
    Imagina que un desarrollador cambió la lógica y ahora 
    el mensaje se pierde en lugar de ir a la cola de errores.
    """
    mock_conn = mocker.Mock()
    listener = RoutingListener(mock_conn)
    
    # Simulamos un frame con JSON corrupto
    class MockFrame:
        body = "{ 'id': 'malformed' " # JSON inválido
        
    listener.on_message(MockFrame())

    # El Pipeline esperaría que se llamara a la cola de errores
    # Forzamos el fallo verificando algo que NO debería pasar:
    assert mock_conn.send.call_count == 0, "ERROR CI: El mensaje fallido no fue enrutado a errores."