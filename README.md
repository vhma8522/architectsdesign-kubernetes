## Deploy API
kubectl apply -f clase-api.yaml
kubectl get pods (Verán 3 pods naciendo).
kubectl apply -f backend-lb.yaml
kubectl apply -f frontend.yaml

## Monitoreo en vivo: 
kubectl get pods -w

# Borrar una terminal para simular una caida
kubectl delete pod [NOMBRE_DE_UN_POD]
kubectl delete pod api-resiliente-8448f6599c-bss4z

# Validar que en el momento que uno termina se crea otro
La Observación: En la terminal de monitoreo, verán que en el segundo exacto en que uno dice Terminating, aparece otro en Pending -> Running.

# Pruebas de Stress
# Ejecutar un pod de ataque
kubectl run simulator --image=williamyeh/hey --restart=Never -- -n 10000 -c 50 http://backend-lb/

# Eliminar recursos
kubectl delete -f clase-api.yaml
kubectl delete -f backend-lb.yaml
kubectl delete -f frontend.yaml

# Borra imágenes que no se están usando
docker image prune -f

# Borra redes y volúmenes sin uso
docker system prune --volumes -f

## Image Pull Back
# 1. Asegúrate de que la imagen existe en Docker Desktop
docker images

# 2. Cárgala al cluster (reemplaza con tu nombre de imagen y cluster)
kind load docker-image mi-api-backend:latest --name arquitectura-proyectos