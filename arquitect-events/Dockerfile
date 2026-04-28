# Usamos una base de Java ligera
FROM eclipse-temurin:17-jre-alpine

# Definimos la versión de ActiveMQ
ENV ACTIVEMQ_VERSION 6.1.5
ENV ACTIVEMQ_HOME /opt/activemq

# Instalamos dependencias y descargamos el binario
RUN apk add --no-cache curl tar \
    && mkdir -p $ACTIVEMQ_HOME \
    && curl https://archive.apache.org/dist/activemq/$ACTIVEMQ_VERSION/apache-activemq-$ACTIVEMQ_VERSION-bin.tar.gz -o activemq.tar.gz \
    && tar -xzf activemq.tar.gz -C /opt \
    && mv /opt/apache-activemq-$ACTIVEMQ_VERSION/* $ACTIVEMQ_HOME \
    && rm activemq.tar.gz

# Exponemos los puertos principales:
# 61616: Protocolo OpenWire (JMS)
# 8161: Panel de administración Web
EXPOSE 61616 8161

WORKDIR $ACTIVEMQ_HOME

# Lanzamos ActiveMQ
CMD ["/bin/sh", "-c", "bin/activemq console"]