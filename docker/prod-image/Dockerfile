FROM python:3.6

MAINTAINER Laurent Morelli laurent.morelli@gmail.com

# ======
# uWSGI
# ======
RUN pip install --upgrade pip && pip install uwsgi
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./docker/conf/uwsgi.ini /etc/uwsgi/
# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /src/uwsgi.ini


#=======
# NGINX
#=======
RUN apt-key adv --no-tty --keyserver keyserver.ubuntu.com --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ stretch nginx" | tee /etc/apt/sources.list.d/nginx.list \
	&& apt-get update \
	&& apt-get install -y apt-utils \
	&& apt-get install -y ca-certificates nginx gettext-base \
	&& rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
# TODO : should fix this with error_log /dev/stderr info; and access_log /dev/stdout;
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
EXPOSE 80 443
# Finished setting up Nginx

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Copy the modified Nginx conf
COPY ./docker/conf/nginx.conf /etc/nginx/conf.d/

# ===============
# Install MongoDB
# ===============
RUN apt-key adv --no-tty --keyserver keyserver.ubuntu.com --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5 \
	&& echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/3.6 main" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list \
	&& apt-get update && apt-get install -y mongodb-org \
	&& mkdir -p /data/db

#============
# SUPERVISOR
#============
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*
# Custom Supervisord config
COPY ./docker/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#========
# OTHERS
#========

# Install pip modules specified in requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy src files
COPY ./src/app /src/app
COPY ./src/main.py /src/main.py
COPY ./src/uwsgi.ini /src/uwsgi.ini

# Copy the entrypoint
COPY ./docker/conf/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run supervisord
CMD ["/usr/bin/supervisord"]

WORKDIR /src
