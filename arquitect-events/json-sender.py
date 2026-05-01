import stomp
import json
import time
import os

# Datos del mensaje en formato diccionario
data = {
    "id_pedido": 1025,
    "cliente": "Victor Mtz",
    "productos": [
        {"item": "Laptop iMac 24", "cantidad": 1},
        {"item": "Mouse Inalámbrico", "cantidad": 2}
    ],
    "total": 2550.00,
    "timestamp": time.ctime()
}

# Leemos las variables inyectadas por Docker
HOST = os.getenv('BROKER_HOST')
PORT = int(os.getenv('BROKER_PORT', 61613))
USER = os.getenv('BROKER_USER')
PASS = os.getenv('BROKER_PASSWORD')
DESTINATION = os.getenv('QUEUE_VALIDADOS')

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