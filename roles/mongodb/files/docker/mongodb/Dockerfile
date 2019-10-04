FROM        aemdesign/centos-tini:latest

MAINTAINER  devops <devops@aem.design>

LABEL       container.description="mongodb container"

RUN         yum -y install epel-release && \
            yum -y install mongodb-server && \
            yum clean all && \
            mkdir -p /data/db

EXPOSE 27017

CMD ["exec", "/usr/bin/mongod"]

