# Introducing
Ztd.Blunders is the software for deployment a Web server for solving chess problems. This is OpenSource project written with use of Flask, PostgreSQL, MongoDB and several other tools and libs. To use it you will need special prepared databases, you will not find them in this repository.

Those databases are result of several month of research and analizing for over 6000000+ officially registered chess games.  From all this data, we derived 1700000+ positions, where one of the side make brute mistake and it's opponent can win in ellegant way. More, sophisticated algorithm was developed to assign each position a rating score.

# Installing
In this article we will cover deployment of Ztd.Blunders server. We are focusing on CentOS 7 x64 distribution, however this is not step by step manual. Variations are possible and different software versions can cause some problems.

1. Install repository and update submodules  
        $ yum install git  
        $ git clone git@bitbucket.org:ziltoidteam/chessdb-web.git  

    Enter to Git repository's directory and update modules  
        $ git submodule init  
        $ git submodule update

2. Installing python.  
    Currently, default repository includes only 2.7 version, but we need 3.4. We will find it in IUS repository.  
    Source: https://iuscommunity.org/pages/Repos.html  
    $ sudo yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-14.ius.centos7.noarch.rpm  
    NOTE: IUS repository installs EPEL repository as dependence  
    $ sudo yum install python34u.x86_64 python34u-pip.noarch

3. Installing PostgreSQL server.
    We can use special repository from PostgreSQL maintainers. Current available version is 9.4.  
    Source: http://www.postgresql.org/download/linux/redhat/#  
        $ yum install http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-redhat94-9.4-1.noarch.rpm
        $ sudo yum install postgresql94.x86_64postgresql94-server.x86_64postgresql94-devel.x86_64
        $ /usr/pgsql-9.4/bin/postgresql94-setup initdb
        $ systemctl enable postgresql-9.4.service Edit config file to allow local login.
        $ vi /var/lib/pgsql/9.4/data/pg_hba.conf
    Find and edit rules to allow password less connection with.
        # "local" is for Unix domain socket connections only
        local all all trust
        # IPv4 local connections:
        host all all 127.0.0.1/32 trust
    Start the service:
        $ systemctl start postgresql-9.4.service
    By default, database user postgres is activated. We will use it. At first, create empty database chessdb
        $ createdb -U postgres chessdb
    Second, we will load scheme to use in our project. It is just a dump stored in our repository.
        $ psql -U postgres chessdb < misc/postgresql_scheme.sql

4. Installing MongoDB server.  
    Once more, we will use custom repository with more recent version of software. At standart repository there is version 2.6.9, but we will install version 3.0.4  
    Source: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-red-hat/  
    Create file /etc/yum.repos.d/mongodb.repo with following content
        [mongodb-org-3.0]
        name=MongoDB Repository
        baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.0/x86_64/
        gpgcheck=0
        enabled=1
    Now install it:
        $ sudo yum install mongodb-org.x86_64
        $ sudo systemctl start mongod
        $ sudo chkconfig mongod on

5. Create secret key to enable sessions  
    Source: http://flask.pocoo.org/docs/0.10/quickstart/  
    We created special script to generate this key. Go to repository root directory and run
        $ misc/generateSecretKey.py
    You should see secret.key file created in the repository. Don't replace this key during server work as it can corrupt your user's sessions.

6. Installing dependencies for flask project.  
        $ sudo pip3.4 install Flask

7. Install Python driver for MongoDB  
        $ sudo pip3.4 install pymongo

8. We need to install Python driver for PostgreSQL.  
        $ sudo yum install gcc python34u-devel libpqxx libpqxx-devel
    Do following as root: 
        $ export PATH=$PATH:/usr/pgsql-9.4/bin
        $ pip3.4 install psycopg2

9. Install Python BCrypt library  
        $ sudo yum install libffi-devel $ sudo pip3.4 install bcrypt

10. Install python-chess library  
        $ sudo pip3.4 install python-chess  

11. Load games and blunders collections  
    We assume you have two specially prepared collections on MongoDB. We are not include them into this repository now, but will probably do this in the future.
        $ mongoimport --drop -d chessdb -c games ./games-ready.mongo
        $ mongoimport --drop -d chessdb -c filtered_blunders ./filtered_blunders-ready.mongo
    Now you have all the data to run the service.

12. You can run server from repository's root directory  
        $ sudo python3.4 ./run.py
    If you want systemd script, we prepared one for you
        $ sudo cp misc/blunders.service /usr/lib/systemd/system/
    Your repository location can be in different location than ours so you can edit this file to set it up.