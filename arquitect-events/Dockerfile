FROM eclipse-temurin:17-jre-alpine

ENV ACTIVEMQ_VERSION 6.1.5
ENV ACTIVEMQ_HOME /opt/activemq

RUN apk add --no-cache curl tar \
    && mkdir -p $ACTIVEMQ_HOME \
    && curl https://archive.apache.org/dist/activemq/$ACTIVEMQ_VERSION/apache-activemq-$ACTIVEMQ_VERSION-bin.tar.gz -o activemq.tar.gz \
    && tar -xzf activemq.tar.gz -C /opt \
    && mv /opt/apache-activemq-$ACTIVEMQ_VERSION/* $ACTIVEMQ_HOME \
    && rm activemq.tar.gz

# IMPORTANTE: Permitir conexiones externas al panel web
RUN sed -i 's/127.0.0.1/0.0.0.0/g' $ACTIVEMQ_HOME/conf/jetty.xml

WORKDIR $ACTIVEMQ_HOME
EXPOSE 8161 61616 61613 1883

CMD ["/bin/sh", "-c", "bin/activemq console"]