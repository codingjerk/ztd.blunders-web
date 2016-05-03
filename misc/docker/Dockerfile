
FROM library/centos

RUN yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-14.ius.centos7.noarch.rpm -y
RUN yum install http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-redhat94-9.4-1.noarch.rpm -y
ADD mongodb-org.repo /etc/yum.repos.d/mongodb-org.repo
RUN yum update -y

RUN yum install git gcc -y
RUN yum install python34u.x86_64 python34u-pip.noarch python34u-devel.x86_64 -y
RUN yum install nginx -y

RUN yum install postgresql94.x86_64 postgresql94-devel.x86_64 -y
RUN yum install libpqxx libpqxx-devel -y
RUN yum install libffi-devel.x86_64 -y

RUN yum install mongodb-org.x86_64 -y

RUN pip3.4 install --upgrade pip
RUN pip3.4 install uWSGI
RUN pip3.4 install Flask
RUN pip3.4 install pymongo
RUN PATH=$PATH:/usr/pgsql-9.4/bin pip3.4 install psycopg2
RUN pip3.4 install bcrypt 
RUN pip3.4 install python-chess
RUN pip3.4 install uwsgitop

RUN useradd -m blunders 
RUN usermod -a -G blunders nginx

RUN su -l blunders bash -c "git clone https://jackalsh@bitbucket.org/ziltoidteam/ztd.blunders-web.git /home/blunders/ztd.blunders-web"
RUN su -l blunders bash -c "cd /home/blunders/ztd.blunders-web && git submodule init && git submodule update"
RUN cd /home/blunders/ztd.blunders-web && misc/generateSecretKey.py

RUN mkdir -p /var/run/blunders
RUN chown -R blunders:blunders /var/run/blunders

WORKDIR /home/blunders
RUN grep -v virtualenv /home/blunders/ztd.blunders-web/misc/uwsgi/uwsgi.ini > /home/blunders/uwsgi.ini

RUN cp /home/blunders/ztd.blunders-web/misc/uwsgi/blunders.conf /etc/nginx/conf.d/blunders.conf

EXPOSE 80

ADD executor.sh /root/executor.sh
CMD /bin/bash /root/executor.sh ; bash
