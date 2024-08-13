FROM ubuntu:22.04
ENV PYTHONUNBUFFERED 1
RUN apt-get update &&\
    apt-get install -y apt-utils vim curl default-libmysqlclient-dev pkg-config apache2 apache2-utils python3 libapache2-mod-wsgi-py3
RUN apt-get update && apt-get install -y software-properties-common &&\
    add-apt-repository main &&\
    apt-get install -y libgl1-mesa-glx libglib2.0-0 build-essential python3-dev
# Install pip
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN ln /usr/bin/python3 /usr/bin/python
RUN apt-get -y install python3-pip
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
RUN apt-get update && apt-get install -y cron sqlite3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED 1
RUN chown -R :www-data var
RUN mkdir django_app
RUN chmod -R 777 var/
RUN chmod -R 755 django_app
# **Added this line to create the /cron directory**
RUN mkdir -p /cron
RUN touch /cron/cron.log
RUN chown -R www-data:www-data cron/
RUN chmod -R 755 cron/
WORKDIR /django_app
ADD . .
ls -l
COPY site_conf.conf /django_app/site_conf.conf
#COPY ./media /app/media
#RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r ./requirements.txt --no-cache
RUN chown -R www-data:www-data .
RUN chmod -R 755 .
#RUN cd .. && chmod -R 777 var/
# django-crontab logfile
RUN chmod +x entrypoint.sh
EXPOSE 5000
CMD ["./entrypoint.sh"]
#CMD ["sh", "-c", "python (link unavailable) collectstatic --noinput && python (link unavailable) runserver 0.0.0.0:5000 && tail -f /cron/cron.log"]
