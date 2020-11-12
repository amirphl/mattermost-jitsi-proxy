FROM python:3.7

RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get -y install tzdata && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime
RUN apt-get install -y git --fix-missing
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install -y netcat --fix-missing
RUN pip install coverage

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
