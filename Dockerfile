FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron sqlite3 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pip --upgrade


ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt ./
COPY ./static /app/staticfiles
#COPY ./media /app/media

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# django-crontab logfile
RUN mkdir /cron
RUN touch /cron/cron.log

EXPOSE 5000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:5000 && tail -f /cron/cron.log"]
