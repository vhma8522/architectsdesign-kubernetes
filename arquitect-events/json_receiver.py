from venv import logging as logger

import stomp
import json
import time
import sys
from jsonschema import validate, ValidationError
import os

# Loggeres para monitoreo
# Configura el nivel a INFO y define un formato opcional
logger.basicConfig(level=logger.INFO, format='%(levelname)s: %(message)s')

logger = logger.getLogger(__name__)

# IMPORTACIÓN DESDE LA LIBRERÍA CENTRAL
from schemas_lib import PEDIDO_SCHEMA

# Leemos las variables inyectadas por Docker
HOST = os.getenv('BROKER_HOST')
PORT = int(os.getenv('BROKER_PORT', 61613))
USER = os.getenv('BROKER_USER')
PASS = os.getenv('BROKER_PASSWORD')
DESTINATION = os.getenv('QUEUE_VALIDADOS')
DESTINATION = os.getenv('QUEUE_VALIDADOS')

logger.info(f"Configuración de conexión: HOST={HOST}, PORT={PORT}, USER={USER}, DESTINATION={DESTINATION}")

# Cargamos los datos
def load_json_asset(filename):
    # Obtenemos la ruta absoluta respecto al archivo actual
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'assets', filename)
    with open(file_path, 'r') as f:
        return json.load(f)
    
class ValidatingListener(stomp.ConnectionListener):
    topicsend = None
   
    def on_message(self, frame):
        try:
            payload = json.loads(frame.body)
            
            #print(f"Inicio DEBUG - Validando mensaje...")
            #print(f"DEBUG - Recibido: {frame.body}") # Agrega esto
            #print(f"FIN DEBUG - Validando mensaje...")

            # Validación usando el esquema centralizado
            validate(instance=payload, schema=PEDIDO_SCHEMA)
            self.topicsend = '/topic/PedidosErrores'
            
            print(f" RECEIVER [+] Mensaje VÁLIDO: Pedido #{payload['id_pedido']} de {payload['cliente']}")
        
        #TODO: Enviar a Topico sin procesar y avisar del error
        except ValidationError as e:
            print(f" RECEIVER [!] ERROR DE CONTRATO: {e.message}")
            self.topicsend = '/topic/Pedidos_Contract'
            
        except json.JSONDecodeError:
            print(" RECEIVER [!] ERROR: El cuerpo no es un JSON válido.")
            self.topicsend = '/topic/Pedidos_Invalid'

# Configuración de conexión

#TODO: Hacer ejecicio de try-catch para manejar errores de conexión

## Conexion desde windows local
param_host = '127.0.0.1' # Conexion desde windows local 127.0.0.1
conn = stomp.Connection([(param_host, 61613)])

## Conexion desde docker-compose
##conn = stomp.Connection([('activemq', 61613)])

conn.set_listener('validate_esquema', ValidatingListener())

#TODO: Cambiar a contraseñas seguras en enviroment or secrets
try:
    conn.connect('admin', 'admin', wait=True)   
except Exception as e:
    logger.error(f" ERROR DE CONEXIÓN: No se pudo conectar a ActiveMQ con las credenciales proporcionadas. Detalles: {e}")
    param_host = 'activemq' # Conexion desde docker-compose
    conn = stomp.Connection([(param_host, 61613)])
    conn.connect('admin', 'admin', wait=True)

logger.info(f"Conectado a ActiveMQ en {[(param_host, 61613)]}")

logger.info(f"Subscrito a ActiveMQ en {ValidatingListener().topicsend}")
conn.subscribe(destination=ValidatingListener().topicsend, id=1, ack='auto')

logger.info(f" RECEIVER Logger [*] Receptor iniciado (Esquema cargado de librería central)'")
print(' RECEIVER [*] Receptor iniciado (Esquema cargado de librería central)')

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()