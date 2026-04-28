import stomp
import time

class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print(f" [y] Mensaje recibido: {frame.body}")

conn = stomp.Connection([('127.0.0.1', 61613)])
conn.set_listener('', MyListener())
conn.connect('admin', 'admin', wait=True)

conn.subscribe(destination='/queue/LaboratorioDocker', id=1, ack='auto')

print(' [*] Esperando mensajes. Para salir presiona CTRL+C')
while True:
    time.sleep(1)