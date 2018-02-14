# inspired from  https://github.com/tiangolo/uwsgi-nginx-flask-docker/tree/master/python2.7
FROM python:2.7

MAINTAINER Laurent Morelli laurent.morelli@gmail.com

# ======
# uWSGI
# ======
RUN pip install uwsgi
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./docker/conf/uwsgi.ini /etc/uwsgi/
# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /src/uwsgi.ini

#=======
# NGINX
#=======
ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
	&& rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
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
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6 \
	&& echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" | tee /etc/apt/sources.list.d/mongodb-org-3.4.list \
	&& apt-get update && apt-get install -y mongodb \
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
