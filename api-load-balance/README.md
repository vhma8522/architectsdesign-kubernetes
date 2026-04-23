# Modificar cluster
kind delete cluster --name arquitectura-proyectos
kind create cluster --name arquitectura-proyectos --config cluster-config.yaml
kind create cluster --name docker-desktop --config cluster-config.yaml

# Descargar la imagen
docker pull nginx:alpine

# Cargar imagen en kubernetes
kind load docker-image nginx:alpine --name docker-desktop

# Deploy PODS
kubectl apply -f balanceador-practica.yaml
kubectl apply -f balanceo.yaml

# Monitor de puertos
kubectl port-forward svc/mi-balanceador-web 8080:80

# En una consola generar el monitor de pods
kubectl logs -l app=mi-api --tail=1
kubectl logs -l app=api-clase -f --prefix

# Generar prueba de stress
kubectl run stress-test --image=williamyeh/hey --restart=Never -- -n 1000 -c 20 http://mi-balanceador-web/

# destruir los recursos
kubectl delete -f balanceo.yaml
kubectl delete -f balanceador-practica.yaml

# borrar el cluster
kind delete cluster --name arquitectura-proyectos