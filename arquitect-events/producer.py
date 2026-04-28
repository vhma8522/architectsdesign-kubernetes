import stomp
import time

conn = stomp.Connection([('127.0.0.1', 61613)]) # Nota: ActiveMQ mapea STOMP al 61613 por defecto
conn.connect('admin', 'admin', wait=True)

mensaje = "Hola clase de Sistemas Distribuidos!"
conn.send(body=mensaje, destination='/queue/LaboratorioDocker')

print(f" [x] Mensaje enviado: {mensaje}")
conn.disconnect()