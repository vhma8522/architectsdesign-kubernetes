# Modificar cluster
kind delete cluster --name arquitectura-proyectos
kind create cluster --name arquitectura-proyectos --config cluster-config.yaml

# Descargar la imagen
docker pull nginx:alpine

# Cargar imagen en kubernetes
kind load docker-image nginx:alpine --name arquitectura-proyectos

# Deploy PODS
kubectl apply -f balanceo.yaml

# Monitor de puertos
kubectl port-forward svc/api-balanceador 8080:80

# En una consola generar el siguiente dato
kubectl logs -l app=mi-api --tail=1
kubectl logs -l app=api-clase -f --prefix

# destruir los recursos
kubectl delete -f clase-kubernetes.yaml

# borrar el cluster
kind delete cluster --name arquitectura-proyectos