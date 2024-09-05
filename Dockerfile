FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y apt-utils \
    vim \
    curl \
    default-libmysqlclient-dev \
    pkg-config \
    apache2 \
    apache2-utils \
    python3 \
    libapache2-mod-wsgi-py3

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository main && \
    apt-get install -y libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    python3-dev

# Install pip
RUN apt-get update && \
    apt-get install -y python3-pip

COPY requirements.txt .

RUN pip install --upgrade pip && \
tep 24/31 : COPY ./site_conf.conf /etc/apache2/sites-available/000-default.conf
 ---> 4ac2ec5229b0
Step 25/31 : RUN chown -R www-data:www-data .
 ---> Running in 10b15cf8ddb7
 ---> Removed intermediate container 10b15cf8ddb7
 ---> 3c091c1f89b9
Step 26/31 : RUN chmod 664 db.sqlite3
 ---> Running in 825e2913e896
chmod: cannot access 'db.sqlite3': No such file or directory
The command '/bin/sh -c chmod 664 db.sqlite3' returned a non-zero code: 1
ERROR: Service 'cron-z2y-django' failed to build : Build failedStep 24/31 : COPY ./site_conf.conf /etc/apache2/sites-available/000-default.conf
 ---> 4ac2ec5229b0
Step 25/31 : RUN chown -R www-data:www-data .
 ---> Running in 10b15cf8ddb7
 ---> Removed intermediate container 10b15cf8ddb7
 ---> 3c091c1f89b9
Step 26/31 : RUN chmod 664 db.sqlite3
 ---> Running in 825e2913e896
chmod: cannot access 'db.sqlite3': No such file or directory
The command '/bin/sh -c chmod 664 db.sqlite3' returned a non-zero code: 1
ERROR: Service 'cron-z2y-django' failed to build : Build failed

COPY . .

RUN ln /usr/bin/python3 /usr/bin/python

RUN apt-get -y install python3-pip

RUN ln -sf /usr/bin/pip3 /usr/bin/pip

RUN apt-get update && \
    apt-get install -y cron \
    sqlite3 && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

RUN chown -R :www-data var
RUN mkdir django_app
RUN chmod -R 777 var/

RUN chmod -R 755 django_app
RUN mkdir -p /cron
RUN touch /cron/cron.log

RUN chown -R www-data:www-data cron/
RUN chmod -R 755 cron/

WORKDIR /django_app

ADD . .

COPY ./site_conf.conf /etc/apache2/sites-available/000-default.conf
#COPY ./media /app/media

#RUN pip3 install --no-cache-dir -r requirements.txt

RUN chown -R www-data:www-data .
RUN chmod -R 755 .
#RUN cd .. && chmod -R 777 var/


# django-crontab logfile


# django-crontab logfile


# django-crontab logfile


# django-crontab logfile

RUN chmod +x entrypoint.sh

RUN chmod +x entrypoint.sh
EXPOSE 5000


CMD ["./entrypoint.sh"]
