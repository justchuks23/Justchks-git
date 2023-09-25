FROM python:3.11-alpine

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN python3 -m pip install pip --upgrade

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# django-crontab logfile
RUN mkdir /cron
RUN touch /cron/cron.log

EXPOSE 8000

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 && tail -f /cron/cron.log"]
