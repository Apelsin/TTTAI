FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

# Make Flask happy
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Flask app
ENV FLASK_APP webgame.py

ENTRYPOINT [ "bash", "-c" ]
CMD ["flask run --host=0.0.0.0 --port=80"]
