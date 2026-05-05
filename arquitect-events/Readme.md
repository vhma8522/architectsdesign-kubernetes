Ejecuta estos comandos en tu terminal para poner el broker en marcha:

# Construir la imagen:
docker-compose up -d
docker-compose up -d --build

# Correr el contenedor:
docker run -d -p 8161:8161 -p 61616:61616 -p 61613:61613 --name broker-lab activemq-lab


# Acceso al Panel
    Ingresar a http://localhost:8161.
    Ingresar a las colas pendientes http://localhost:8161/admin/queues.jsp
    Usuario: admin | Password: admin

## Ambiente python

# Es recomendable usar un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate

# Instalar la librería necesaria
pip install stomp.py
pip install jsonschema

# Correr el Consumer
## Python local
python json-receiver.py
## Python desde docker
docker exec -it cliente-python python json-receiver.py 

# Correr el Sender
## Python local
python json-sender.py
## Python desde docker
docker exec -it cliente-python python json-sender.py

## Comandos para libreria Python desde docker
docker logs -f cliente-python
docker exec -it cliente-python bash
docker-compose restart python-lab


# Eliminar ambiente
docker-compose down
docker-compose down --rmi all

# Eliminar ambiente y regrenerar sin cache
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Ejecutar pruebas
# Regenerar las imagens para incluir los nuevos paquetes
docker-compose up -d --build



# Unitarias
docker exec -it cliente-python pytest test_sender.py # Mock
docker exec -it cliente-python python json_sender.py # Variables de entorno
docker exec -it cliente-python python -m pytest test/test_receiver.py
# Integracion

# Code Coverage
docker exec -it cliente-python pytest --cov=. --cov-report=term-missing
docker exec -it cliente-python pytest --cov=. --cov-report=html