import stomp
import json
import time
import os
from venv import logging as logger

# Loggeres para monitoreo
# Configura el nivel a INFO y define un formato opcional
logger.basicConfig(level=logger.INFO, format='%(levelname)s: %(message)s')

logger = logger.getLogger(__name__)

# Configuración de conexión
#conn = stomp.Connection([('127.0.0.1', 61613)])
## Conexion desde docker-compose
conn = stomp.Connection([('activemq', 61613)])

conn.connect('admin', 'admin', wait=True)

# Convertir el diccionario a una cadena JSON
json_payload = json.dumps(data)

# Enviar a la cola
conn.send(body=json_payload, destination='/queue/PedidosJSON')

print(" SENDER [x] JSON enviado con éxito:")
print(json_payload)

conn.disconnect()

def get_connection():
    host = os.getenv('BROKER_HOST', '127.0.0.1')
    port = int(os.getenv('BROKER_PORT', 61613))
    user = os.getenv('BROKER_USER', 'admin')
    password = os.getenv('BROKER_PASSWORD', 'admin')
    
    conn = stomp.Connection([(host, port)])
    return conn, user, password

def send_pedido(data):
    conn, user, pwd = get_connection()
    logger.info(f"Intentando conectar a ActiveMQ en {[(host, port)]} con usuario '{user}'")

    try:
        conn.connect(user, pwd, wait=True)
        payload = json.dumps(data)
        conn.send(body=payload, destination='/queue/PedidosValidados')
        conn.disconnect()
        return True
    except Exception as e:
        print(f"Error enviando: {e}")
        return False
    finally:        
        if conn.is_connected():
            conn.disconnect()