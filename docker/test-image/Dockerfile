# Extends prod image
FROM spil_prod_image

MAINTAINER Laurent Morelli laurent.morelli@gmail.com

# Copy tests folder
COPY ./src/tests /src/tests

# Install nose to run tests
RUN pip install nose==1.3.7
