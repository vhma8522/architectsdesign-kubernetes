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
            
            print(f"Inicio DEBUG - Validando mensaje...")
            print(f"DEBUG - Recibido: {frame.body}") # Agrega esto
            print(f"FIN DEBUG - Validando mensaje...")

            # Validación usando el esquema centralizado
            validate(instance=payload, schema=PEDIDO_SCHEMA)
            
            print(f" RECEIVER [+] Mensaje VÁLIDO: Pedido #{payload['id_pedido']} de {payload['cliente']}")
            
        except ValidationError as e:
            print(f" [!] ERROR DE CONTRATO: {e.message}")
        except json.JSONDecodeError:
            print(" RECEIVER [!] ERROR: El cuerpo no es un JSON válido.")

# Configuración de conexión

#TODO: Hacer ejecicio de try-catch para manejar errores de conexión

## Conexion desde windows local
#conn = stomp.Connection([('127.0.0.1', 61613)])

## Conexion desde docker-compose
conn = stomp.Connection([('activemq', 61613)])

conn.set_listener('validate_esquema', ValidatingListener())
#TODO: Cambiar a contraseñas seguras en enviroment or secrets
conn.connect('admin', 'admin', wait=True)

conn.subscribe(destination='/queue/PedidosJSON', id=1, ack='auto')

print(' RECEIVER [*] Receptor iniciado (Esquema cargado de librería central)')
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()