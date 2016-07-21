# To build and run container in interactive mode run this within Dockerfile directory 
# docker build -t docker-blunders . && docker run -p 80:80 -ti docker-blunders
# For daemon mode
# docker build -t docker-blunders . && docker run -d -p 80:80 -t docker-blunders

FROM library/centos

# Installing repositories
RUN yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-14.ius.centos7.noarch.rpm -y
RUN yum install http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-redhat94-9.4-1.noarch.rpm -y
RUN yum update -y

# Installing system packages
RUN yum install git gcc gcc-c++ -y
RUN yum install python34u.x86_64 python34u-pip.noarch python34u-devel.x86_64 -y
RUN yum install nginx -y
RUN yum install postgresql94.x86_64 postgresql94-devel.x86_64 -y
RUN yum install libpqxx libpqxx-devel -y
RUN yum install libffi-devel.x86_64 -y
RUN yum install supervisor -y

# Installing python packages
RUN pip3.4 install --upgrade pip
RUN pip3.4 install uWSGI
RUN pip3.4 install Flask
RUN pip3.4 install redis
RUN PATH=$PATH:/usr/pgsql-9.4/bin pip3.4 install psycopg2
RUN pip3.4 install bcrypt 
RUN pip3.4 install python-chess
RUN pip3.4 install uwsgitop

# Creating user blunders for uwsgi to use
RUN useradd -m blunders 
RUN usermod -a -G blunders nginx # nginx must read uwsgi sockets

# Cloning the Blunders project
ARG GIT_BRANCH
RUN su -l blunders bash -c "git clone -b $GIT_BRANCH https://jackalsh@bitbucket.org/ziltoidteam/ztd.blunders-web.git /home/blunders/ztd.blunders-web"
RUN su -l blunders bash -c "cd /home/blunders/ztd.blunders-web && git submodule init && git submodule update"
RUN cd /home/blunders/ztd.blunders-web && misc/generateSecretKey.py

# Create directory for uwsgi sockets 
RUN mkdir -p /var/run/blunders
RUN chown -R blunders:blunders /var/run/blunders

# Copying uwsgi configuration
WORKDIR /home/blunders

ADD uwsgi/uwsgi.ini /home/blunders/uwsgi.ini
ADD nginx/blunders.conf /etc/nginx/conf.d/blunders.conf

# Compiling Stockfish chess engine for analyzation service
RUN git clone https://github.com/mcostalba/Stockfish.git /opt/stockfish
RUN make -j4 build ARCH=x86-64 -C /opt/stockfish/src/
RUN chown blunders:blunders /opt/stockfish/src/stockfish

EXPOSE 80

ADD supervisord/supervisord.ini /etc/supervisord.d/supervisord.ini
ADD executor.sh /root/executor.sh

CMD /root/executor.sh
