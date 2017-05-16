# To build and run container in interactive mode run this within Dockerfile directory 
# docker build -t docker-blunders . && docker run -p 80:80 -ti docker-blunders
# For daemon mode
# docker build -t docker-blunders . && docker run -d -p 80:80 -t docker-blunders

FROM library/centos

# Installing repositories
RUN yum install -y https://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-14.ius.centos7.noarch.rpm \
                   http://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-6-x86_64/pgdg-redhat94-9.4-3.noarch.rpm
RUN yum update -y

# Installing system packages
RUN yum install -y git unzip gcc gcc-c++ \
         python34u.x86_64 python34u-pip.noarch python34u-devel.x86_64 \
         nginx \
         postgresql94.x86_64 postgresql94-devel.x86_64 \
         libpqxx libpqxx-devel \
         libffi-devel.x86_64 \
         supervisor \

# Installing python packages
RUN pip3.4 upgrade pip
RUN pip3.4 install uWSGI Flask redis bcrypt python-chess uwsgitop

RUN PATH=$PATH:/usr/pgsql-9.4/bin pip3.4 install psycopg2

# Creating user blunders for uwsgi to use
RUN useradd -m blunders 
RUN usermod -a -G blunders nginx # nginx must read uwsgi sockets

# Cloning the Blunders project

USER blunders

ARG GIT_BRANCH
RUN git clone -b $GIT_BRANCH https://jackalsh@bitbucket.org/ziltoidteam/ztd.blunders-web.git /home/blunders/ztd.blunders-web
WORKDIR /home/blunders/ztd.blunders-web 
RUN git submodule init && git submodule update
RUN misc/generateSecretKey.py

USER root
# Create directory for uwsgi sockets 
RUN mkdir -p /var/run/blunders
RUN chown -R blunders:blunders /var/run/blunders

# Copying uwsgi configuration
WORKDIR /home/blunders

ADD uwsgi/uwsgi.ini /home/blunders/uwsgi.ini
ADD nginx/blunders.conf /etc/nginx/conf.d/blunders.conf

# Compiling Stockfish chess engine for analyzation service
RUN curl https://stockfish.s3.amazonaws.com/stockfish-8-linux.zip -o /opt/stockfish.zip
RUN cd /opt/ && unzip /opt/stockfish.zip
RUN chown -R blunders:blunders /opt/stockfish-8-linux

EXPOSE 80

ADD supervisord/supervisord.ini /etc/supervisord.d/supervisord.ini
ADD executor.sh /root/executor.sh

CMD /root/executor.sh
