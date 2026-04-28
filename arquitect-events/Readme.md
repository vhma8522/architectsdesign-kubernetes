Ejecuta estos comandos en tu terminal para poner el broker en marcha:

Construir la imagen:
docker build -t activemq-lab .

Correr el contenedor:
docker run -d -p 8161:8161 -p 61616:61616 --name broker-lab activemq-lab

Acceso al Panel: Ve a http://localhost:8161.

Usuario: admin | Password: admin

## Ambiente python

# Es recomendable usar un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate

# Instalar la librería necesaria
pip install stomp.py