# Ztd.Blunders Web

## Try it online
Ztd.Blunders available on [chessblunders.org](https://chessblunders.org/) and this is our main server. 

Best experience you will get using our [mobile client](https://play.google.com/store/apps/details?id=io.ztd.blunders.free).

## Introducing
Ztd.Blunders is the software for deployment a Web server for solving chess problems. This is Open Source project written with use of Flask, PostgreSQL, MongoDB and several other tools and libraries. To use it you will need special prepared databases, you will not find them in this repository.

Those databases are result of several months of research and analyzing for over 6000000+ officially registered chess games.  From all this data, we derived 1700000+ positions, where one of the players makes brute mistake and it's opponent can win in an elegant way. More, sophisticated algorithm was developed to assign each position a rating score, showing relative difficulty for finding best move.

## Dockerize it!
Yes, we support docker, in order to run server just run in project root directory:

```
#!bash
docker-compose up
```
You will get running application server, supporting both mobile and web API. To check it just enter to [http://localhost:80](Link URL). You should see project welcome page.
## Manual installing
In this article we will cover deployment of Ztd.Blunders server. We are focusing on CentOS 7 x64 distribution, however this is not step by step manual. Variations are possible and different software versions can cause some problems.

1. Install repository and update submodules  
    ```
    yum install git  
    git clone git@bitbucket.org:ziltoidteam/chessdb-web.git
    ```

    Enter to Git repository's directory and update modules  
    ```
    $ git submodule init  
    $ git submodule update
    ```

2. Installing python.  
    Currently, default repository includes only 2.7 version, but we need 3.4. We will find it in IUS repository.  
    Source: https://iuscommunity.org/pages/Repos.html  
    ```$ yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-14.ius.centos7.noarch.rpm```  
    NOTE: IUS repository installs EPEL repository as dependence  
    ```$ yum install python34u.x86_64 python34u-pip.noarch```

3. Installing PostgreSQL server.
    We can use special repository from PostgreSQL maintainers. Current available version is 9.4.  
    Source: http://www.postgresql.org/download/linux/redhat/#  
    ```
    $ yum install http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-redhat94-9.4-1.noarch.rpm
    ```  
    ```
    $ sudo yum install postgresql94.x86_64postgresql94-server.x86_64postgresql94-devel.x86_64  
    ```  
    ```
    $ /usr/pgsql-9.4/bin/postgresql94-setup initdb  
    ```  
    ```
    $ systemctl enable postgresql-9.4.service Edit config file to allow local login.
    ```  
    ```  
    $ vi /var/lib/pgsql/9.4/data/pg_hba.conf
    ```

    Find and edit rules to allow password less connection with.
    ```bash
    local all all trust  
    host all all 127.0.0.1/32 trust```

    Start the service:
    ```$ systemctl start postgresql-9.4.service```  
    By default, database user postgres is activated. We will use it. At first, create empty database chessdb
    ```$ createdb -U postgres chessdb```  
    Second, we will load scheme to use in our project. It is just a dump stored in our repository.
    ```$ psql -U postgres chessdb < misc/postgresql_scheme.sql```  

4. Installing Redis
    We use Redis as TTL cache.
    ```$ yum install redis ```
    ```$ pip3.4 install redis ```
5. Create secret key to enable sessions  
    Source: http://flask.pocoo.org/docs/0.10/quickstart/  
    We created special script to generate this key. Go to repository root directory and run
    ```$ misc/generateSecretKey.py```  
    You should see secret.key file created in the repository. Don't replace this key during server work as it can corrupt your user's sessions.

6. Installing dependencies for flask project.  
    ```$ sudo pip install Flask```  

7. We need to install Python driver for PostgreSQL.  
    ```$ sudo yum install gcc python34u-devel libpqxx libpqxx-devel```  
    Do following as root: 
    ```$ export PATH=$PATH:/usr/pgsql-9.4/bin```  
    ```$ pip3.4 install psycopg2```  

8. Install Python BCrypt library  
    ```$ sudo yum install libffi-devel $ sudo pip3.4 install bcrypt```  

9. Install python-chess library  
    ```$ sudo pip3.4 install python-chess```  

10. Load games and blunders databases  
    We assume you have specially prepared collection of database, you will not find it here. We will publish it's schema when it will be stable. Ideally, you will use separate postgresql database instance.
    Now you have all the data to run the service.
11. You can run server from repository's root directory  
    ```$ sudo python3.4 ./debug.py```  
    If you want systemd script, we prepared one for you
    ```$ sudo cp misc/blunders.service /usr/lib/systemd/system/```  
    Your repository location can be in different location than ours so you can edit this file to set it up.
12. You can conect to the server on port 8089, as set in debug.py. This configuration is for testing purposes only.

## Advanced - setup uWSGI+nginx service.
1. We assume, that all the processed will run as local, non root account, so install user blunders without any permissions. /home/blunders will be it's home.
Flask is one thread server by definition, so you it's problematic to use it in multiuser mode in production. We will use uWSGI service to create and maintain multi instances and make load balancing between them. Nginx will be configured to sit in fron of them as web server.
2. If you installed all python packages as we told in previous sections, you probably want skip this step. For production we will set up python virtual environment and install all python packages into /home/blunders/env folder. This is our default. To use global packages you probably want to edit uwsgi.ini file, but it's all up to you.  Read more about  virtual environment here https://virtualenv.pypa.io/en/latest/userguide.html.

3. Copy uwsgi.ini to /home/blunders. This is configuration file for uWSGI. We will use pip to install uWSGI, but will install it globally.
    ```
  $ pip3.4 install uWSGI
    ```
Copy systemd unit to proper directory
    ```
  $ cp /home/blunders/ztd.blunders-web/misc/uwsgi/blunders.service /usr/lib/systemd/system/
  $ systemctl daemon-reload
  $ systemctl start blunders && systemctl enable blunders
    ```

4. Install nginx server
    ```
  $ yum install nginx
    ```
Copy default Vhost configuration.
  $ cp /home/blunders/ztd.blunders-web/misc/uwsgi/blunders.conf /etc/nginx/conf.d/
uWSGI will create directory /var/run/blunder with unix socket for communication with nginx, but this socket is owned by blunders user. To get nginx read access to this socket, add nginx user to blunders group
    ```
  $ usermod -a -G blunders nginx
    ```
Start nginx and service should be available on with your browser.
    ```
  $ systemctl start nginx && systemctl enable nginx
    ```
## Monitoring and maintainance
1. To monitor uWSGI servicem you can use excelent tool
    ```
  $ pip3 install uwsgitop
    ```
    ```
  $ uwsgitop /var/run/blunders/uwsgi-stats.sock
    ```
2. If you want to gracefully reload the workers
    ```
  $ echo "r" > /var/run/blunders/uwsgi.fifo
    ```