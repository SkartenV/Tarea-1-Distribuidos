FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y software-properties-common vim \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update -y \
    && apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv \
    && pip3 install --upgrade pip
	
WORKDIR /app
COPY . /app
VOLUME /data
CMD ["python3","cliente.py"]