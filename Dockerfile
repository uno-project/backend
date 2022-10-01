#Grab the latest alpine image
FROM --platform=linux/amd64 alpine:latest

# Install python and pip
RUN apk add --no-cache --update python3 py3-pip bash build-base python3-dev libffi-dev
ADD requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD rest  /opt/webapp/rest/
ADD uno  /opt/webapp/uno/

WORKDIR /opt/webapp

# Run the image as a non-root user
RUN adduser -D myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
EXPOSE 8080
CMD gunicorn --bind 0.0.0.0:8080 'rest:create_app()'

