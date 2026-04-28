import stomp
import json
import time

# Datos del mensaje en formato diccionario
data = {
    "id_pedido": 1025,
    "cliente": "Victor Hugo Martinez",
    "productos": [
        {"item": "Laptop iMac 24", "cantidad": 1},
        {"item": "Mouse Inalámbrico", "cantidad": 2}
    ],
    "total": 2550.00,
    "timestamp": time.ctime()
}

# Configuración de conexión
conn = stomp.Connection([('127.0.0.1', 61613)])
conn.connect('admin', 'admin', wait=True)

# Convertir el diccionario a una cadena JSON
json_payload = json.dumps(data)

# Enviar a la cola
conn.send(body=json_payload, destination='/queue/PedidosJSON')

print(" [x] JSON enviado con éxito:")
print(json_payload)

conn.disconnect()