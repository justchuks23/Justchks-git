FROM ubuntu:22.04
ENV PYTHONUNBUFFERED 1

# Install basic utilities and dependencies
RUN apt-get update &&\
    apt-get install -y \
        apt-utils \
        vim \
        curl \
        default-libmysqlclient-dev \
        pkg-config \
        apache2 \
        apache2-utils \
        python3 \
        libapache2-mod-wsgi-py3 \
        software-properties-common \
        libgl1-mesa-glx \
        libglib2.0-0 \
        build-essential \
        python3-dev \
        python3-pip \
        cron \
        sqlite3 &&\
    rm -rf /var/lib/apt/lists/*

# Create symbolic links for python and pip
RUN ln -sf /usr/bin/python3 /usr/bin/python &&\
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Set up the application directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt --no-cache

# Copy application code
COPY . .

# Ensure all necessary directories exist and set permissions
RUN mkdir -p /cron &&\
    touch /cron/cron.log &&\
    mkdir -p django_app &&\
    chown -R :www-data var &&\
    chmod -R 777 var/ &&\
    chmod -R 755 django_app &&\
    chown -R www-data:www-data /cron &&\
    chmod -R 755 /cron

# Set Apache configuration
COPY ./site_conf.conf /etc/apache2/sites-available/000-default.conf

# Set ownership and permissions for the working directory
RUN chown -R www-data:www-data . &&\
    chmod -R 755 .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

EXPOSE 5000

# Use entrypoint script
CMD ["./entrypoint.sh"]
