FROM laurentpaprika/spilserver:latest
#from https://github.com/laurentmorelli/spilserver

MAINTAINER Laurent Morelli laurent.morelli@gmail.com

#========
# OTHERS
#========

# Copy the modified Nginx conf
COPY ./docker/conf/nginx.conf /etc/nginx/conf.d/

# Install pip modules specified in requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#for the log sake
RUN mkdir /var/log/EloLeft4Dead2-AKA-Spil/
RUN chmod 777 -R /var/log/EloLeft4Dead2-AKA-Spil/


# Copy src files
#API
COPY ./src/app /src/app
COPY ./src/main.py /src/main.py
COPY ./src/uwsgi.ini /src/uwsgi.ini
#FRONT
COPY ./front /front

# Copy the entrypoint
COPY ./docker/conf/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run supervisord
CMD ["/usr/bin/supervisord"]

WORKDIR /src
