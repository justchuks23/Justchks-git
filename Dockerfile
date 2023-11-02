FROM python:3.11-slim

# Install additional dependencies including PostgreSQL development libraries
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install pip --upgrade

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt ./

#Added these two lines of COPY below
COPY ./static /app/staticfiles
#COPY ./media /app/media

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# django-crontab logfile
RUN mkdir /cron
RUN touch /cron/cron.log

EXPOSE 5000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:5000 && tail -f /cron/cron.log"]
