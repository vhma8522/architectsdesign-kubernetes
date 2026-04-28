import stomp
import json
import time
import sys
from jsonschema import validate, ValidationError

# IMPORTACIÓN DESDE LA LIBRERÍA CENTRAL
from schemas_lib import PEDIDO_SCHEMA

class ValidatingListener(stomp.ConnectionListener):
    def on_message(self, frame):
        try:
            payload = json.loads(frame.body)
            
            # Validación usando el esquema centralizado
            validate(instance=payload, schema=PEDIDO_SCHEMA)
            
            print(f" [+] Mensaje VÁLIDO: Pedido #{payload['id_pedido']} de {payload['cliente']}")
            
        except ValidationError as e:
            print(f" [!] ERROR DE CONTRATO: {e.message}")
        except json.JSONDecodeError:
            print(" [!] ERROR: El cuerpo no es un JSON válido.")

# Configuración de conexión
conn = stomp.Connection([('127.0.0.1', 61613)])
conn.set_listener('', ValidatingListener())
conn.connect('admin', 'admin', wait=True)
conn.subscribe(destination='/queue/PedidosValidados', id=1, ack='auto')

print(' [*] Receptor iniciado (Esquema cargado de librería central)')
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()