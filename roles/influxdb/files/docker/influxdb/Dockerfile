FROM        aemdesign/centos-tini:latest

MAINTAINER  devops <devops@aem.design>

LABEL   os.version="centos" \
        container.description="influxdb"

ENV INFLUXDB_VERSION=1.2.2

COPY influxdb.conf /etc/influxdb/influxdb.conf

RUN gpg \
    --keyserver hkp://p80.pool.sks-keyservers.net:80 \
    --recv-keys 05CE15085FC09D18E99EFB22684A14CF2582E0C5 && \
    curl -L -O https://dl.influxdata.com/influxdb/releases/influxdb-${INFLUXDB_VERSION}.x86_64.rpm.asc && \
    curl -L -O https://dl.influxdata.com/influxdb/releases/influxdb-${INFLUXDB_VERSION}.x86_64.rpm && \
    gpg --batch --verify influxdb-${INFLUXDB_VERSION}.x86_64.rpm.asc influxdb-${INFLUXDB_VERSION}.x86_64.rpm && \
    yum install -y influxdb-${INFLUXDB_VERSION}.x86_64.rpm && \
    rm -f influxdb-${INFLUXDB_VERSION}.x86_64.rpm*

EXPOSE 8083, 8086

VOLUME /var/lib/influxdb

CMD ["exec", "influxd"]