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
docker image prune -a
# Detiene y elimina contenedores, redes y volúmenes definidos en tu docker-compose
docker-compose down --volumes --remove-orphans
docker network prune -f

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
docker exec -it cliente-python python -m pytest tests/test_receiver.py

# Integracion

# Code Coverage
docker exec -it cliente-python pytest --cov=. --cov-report=term-missing
docker exec -it cliente-python pytest --cov=. --cov-report=html

## CI/CD
# Local-first
docker exec -it cliente-python python -m pytest tests/test_ci_smoke.py --cov=. --cov-fail-under=80

# Prebuilt CI/CD
## Paso A: Limpieza de Caché
docker exec -it cliente-python find . -name "__pycache__" -type d -exec rm -rf {} +

## Paso B: Validación de Estructura
docker exec -it cliente-python bash -c "ls -l json_receiver.py tests/test_ci_smoke.py && python -m py_compile json_receiver.py"

## Validamos sintaxis
docker exec -it cliente-python python -m py_compile json_receiver.py
docker exec -it cliente-python echo $?

## Paso C: Ejecución de Smoke Tests
docker exec -it cliente-python python -m pytest tests/test_ci_smoke.py -v